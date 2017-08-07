des = require "./encode"

start_time = '20170101'
month_time = '66'
key = "20141110"
aaa = des.desencode(start_time,key)
bbb = des.desdecode(aaa,key)
console.log bbb
###
today = new Date()
start_time = "20160810"
long_time = "3"
end_time = new Date()
year = start_time[0..3]
month = start_time[4..5] 
day = start_time[6..8]
end_time.setFullYear(year, parseInt(month)-1+parseInt(long_time), day)
console.log end_time,year, month-1+long_time, day
end_time.setDate(end_time.getDate()+"1")
console.log end_time
console.log today, end_time
if today < end_time
  console.log "valid"
else
  console.log "invalid"
###
