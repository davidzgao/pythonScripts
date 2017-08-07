import datetime
print "please input a date like \"2015-01-01\" "
date_str = raw_input()
format = "%Y-%m-%d"
date = datetime.datetime.strptime(date_str, format)
year = date.year
date_begin = datetime.datetime.strptime("%s-01-01"%year, format)
oneday = datetime.timedelta(days = 1)
cnt = 1 
while date != date_begin:
    date = date - oneday
    cnt += 1 

print "today is the %s day of %s year"%(cnt,year)


