console.log "add a.coffee"
exports.square = (x) ->  x * x
class aaa
  constructor: ->
    @count++
  count: 0
  print_info: ->  console.log "count:",@count
a1 = new aaa()
console.log a1.count
a1.print_info()
  
