#! /usr/bin/python
#  -*- coding:utf8 -*-
#  author: gaozhe
#  date: 2017-01-18
import time
import os
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
import socket
import fcntl
import struct
import datetime
import re



def read_cpu_usage():
    fd = open("/proc/stat", 'r')
    lines = fd.readlines()
    fd.close()
    for line in lines:
        line = line.split()
        if len(line) <5:
            continue
        if line[0].startswith('cpu'):
            return line
    return []

def get_cpu_usage():
    cpustr = read_cpu_usage()
    total1 = long(cpustr[1]) + long(cpustr[2]) +long(cpustr[3]) +\
             long(cpustr[4]) +long(cpustr[5]) +long(cpustr[6]) +long(cpustr[7])
    use1 = long(cpustr[1]) + long(cpustr[2]) +long(cpustr[3])
    time.sleep(3)
    cpustr = read_cpu_usage()
    total2 = long(cpustr[1]) + long(cpustr[2]) +long(cpustr[3]) +\
             long(cpustr[4]) +long(cpustr[5]) +long(cpustr[6]) +long(cpustr[7])
    use2 = long(cpustr[1]) + long(cpustr[2]) +long(cpustr[3])
    cpu_usage = float(use2 - use1)/(total2-total1)
    return 100*cpu_usage

def get_mem_usage():
    memFile = os.popen("free -m")
    total = 0
    used = 0
    for line in memFile.readlines():
        line = line.strip()
        if line.startswith("M"):
           total = int(line.strip().split()[1])
        if line.startswith("-"):
           used = int(line.split()[2])
    mem_usage = 100*float(used)/total
    return (mem_usage,used,total)
    
def get_disk_usage():
    diskFile = os.popen("df -h")
    lnum = 0
    lineStr = ""
    max_used = 0
    forward_line = False
    forward_list = None
    for line in diskFile.readlines():
#        lineStr += line
        lnum += 1
        line = line.strip()
        line_list = line.split()
        if len(line_list) < 6: # deal with the division line problem
           if forward_line:
               line_list = forward_list + line_list
               forward_line = False
           else:
               forward_list = line_list
               forward_line = True
               continue
        lineStr += "\t".join(line_list)
        lineStr += "\n"
        if lnum == 1:
            continue
        fname = line_list[0]
        used = int(line_list[4][:-1])
        if used > max_used:
            max_used = used
        mounted_on = line_list[-1]
    return (max_used,lineStr)

def sendMail(subject,content):
    smtpserver = 'smtp.aisino.com'  
    username = 'gaozhe@aisino.com'  
    password = 'gaozhe490'
    msg = MIMEText(content,'html','utf-8')# 
    msg['Subject'] = Header(subject, 'utf-8')  
    msg['From'] = "服务器监控告警"
    msg['To'] = ";".join(mail_list)
    smtp = smtplib.SMTP(smtpserver,"25")  
    smtp.login(username, password)  
    smtp.sendmail(username,msg['To'], msg.as_string())  
    smtp.quit()  

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('258s', ifname[:15])
    )[20:24])


def get_ip_addr(ifname):
    ifconfig = os.popen("ifconfig -a")
    flag = False
    for line in ifconfig.readlines():
        line = line.strip()
        if line.startswith(ifname):
            flag = True
        if flag and line.startswith("inet addr"):
            ip = line.split()[1].split(":")[1]
            return ip

def gen_content(service_type, hostservice, use_info,limit_info):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    content = "<body>"
    if service_type == "cpu":
        content += "<p>[<span style='color:red'>%s</span>]服务器于%s产生<span style='color:red'>CPU</span>告警</p>"%(hostservice,now)
        content += "<p>当前CPU使用率为<span style='color:red'>%d%%</span>, 超过阈值%d%%</p>"%(use_info,limit_info)
    elif service_type == "mem":
        content += "<p>[<span style='color:red'>%s</span>]服务器于%s产生<span style='color:red'>内存</span>告警</p>"%(hostservice,now)
        content += "<p>当前内存使用率为<span style='color:red'>%d%%</span>, 超过阈值%d%%</p>"%(use_info[0],limit_info)
    elif service_type == "disk":
        content += "<p>[<span style='color:red'>%s</span>]服务器于%s产生<span style='color:red'>磁盘</span>告警</p>"%(hostservice,now)
        content += "<p>当前服务器有单块磁盘使用率为<span style='color:red'>%d%%</span>, 超过阈值%d%%</p>"%(use_info[0],limit_info)
        content += "<p>具体磁盘使用情况：</p>"
        content += "<table border='1'>"
        lnum = 0
	for line in use_info[1].strip().split("\n"):
            lnum += 1
            if lnum == 1:
                content += "<tr style='background-color:#d0d0d0;font-weight:bold'>"
#            elif lnum %2:
#                content += "<tr style='background-color:#d0d0d0'>"
            else:
                content += "<tr>"
            for item in re.split("\s+", line, 5):
                content += "<td style='width:100'>%s</td>"%item
            content += "</tr>"
        content += "</table>"
            
    content += "</body>"
    return content
def check_service():
    cpu_limit = 50
    mem_limit = 70
    disk_limit = 5
    cpu_use = get_cpu_usage()
    mem_use = get_mem_usage()
    disk_use = get_disk_usage()
    if debug: print "cpu:%f\nmem:%f\ndisk:%f"%(cpu_use,mem_use[0],disk_use[0])
    alarm_subject_str = "服务器告警[IP: %s]"%hostservice
    alarm_content = ""
    if cpu_use > cpu_limit:
        alarm_subject = alarm_subject_str + "[CPU]"
        alarm_content = gen_content("cpu", hostservice, cpu_use,cpu_limit)
        sendMail(alarm_subject,alarm_content)
    if mem_use[0] > mem_limit:
        alarm_subject = alarm_subject_str +  "[内存]"
        alarm_content = gen_content("mem", hostservice, mem_use,mem_limit)
        sendMail(alarm_subject,alarm_content)
    if disk_use[0] > disk_limit:
        alarm_subject = alarm_subject_str +  "[磁盘]"
        alarm_content = gen_content("disk", hostservice, disk_use,disk_limit)
        sendMail(alarm_subject,alarm_content)
   

if __name__=="__main__":
    mail_list = ["gaozhe@aisino.com","gaozhehere@sina.com"]
    hostservice = get_ip_addr('eth0') 
    debug = False
    check_service()
