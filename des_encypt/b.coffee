a = require 'a'
#console.log a.square(5)
fs = require 'fs'
func1 = (err,files) ->
  console.log files
fs.readdir '.',func1
console.log "this happen first"
