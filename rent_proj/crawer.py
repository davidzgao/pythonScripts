#! -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
import time

url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=3000_5000"

page = 1
csv_file = open("rent.csv","wb")
csv_writer = csv.writer(csv_file, delimiter = ",")

while True:
    print "fetch:", url.format(page = page)
    responce = requests.get(url.format(page = page))
    html = BeautifulSoup(responce.text)
    house_list = html.select(".list > li")
    if not house_list:
        break
    
    
    for house in house_list:
        #print house
        #f.write(house.string+"\n")
        house_title = house.select("h2")[0].string.encode("utf8")
        #print house_title 
        house_url = urljoin(url, house.select("a")[0]["href"])
        house_info_list = house_title.split()
        # 如果第二列是公寓名则取第一列作为地址
        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]
        #house_location = house_info_list[1]
        house_money = house.select(".money > span > b")[0].string.encode("utf8")
        print house_money
        csv_writer.writerow([house_title, house_location, house_money, house_url])
    time.sleep(1)
    page += 1
csv_file.close()






















































    
