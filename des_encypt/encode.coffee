cfg = require 'cfg'
class Des
  constructor : ->

  _getkey: (key,key_len) ->
    code_key = @_functionCharToA(key,key_len)
    a = ['' for i in [0...16]][0]
    real_len = key_len
    if  key_len%16 != 0
      real_len = parseInt(key_len/16)*16 + 16
    b = ['' for i in [0...parseInt(real_len/16)]][0]
    for i in [0...parseInt(real_len/16)]
      b[i] = a[..]
    num = 0
    trun_len = 4*key_len
    for i in [0...trun_len] by 64
      run_key = code_key[i...(i+64)]
      run_key = @_keyfirstchange(run_key)
      for j in [0...16]
        key_l = run_key[0...28]
        key_r=run_key[28...56]
        key_l=key_l[cfg.d[j]...28]+key_l[0...cfg.d[j]]
        key_r=key_r[cfg.d[j]...28]+key_r[0...cfg.d[j]]
        run_key=key_l+key_r
        key_y = @_functionKeySecondChange(run_key)
        b[num][j] = key_y[..]
      num++
    b

  _codeyihuo: (code, key) ->
    code_len = code.length
    return_list = ""
    for i in [0...code_len]
      if code[i] == key[i]
        return_list += '0'
      else
        return_list += '1'
    return_list

  _codefirstchange: (code) ->
    changed_code = ''
    for i in [0...64]
      changed_code += code[cfg.ip[i]-1]
    changed_code

  _keyfirstchange: (key) ->
    changed_key = ''
    for i in [0...56]
      changed_key += key[cfg.pc1[i]-1]
    changed_key

  _functionCodeChange: (code) ->
    lens = parseInt(code.length/4)
    return_list = ''
    for i in [0...lens]
      tmp_list = ''
      for j in [0...4]
        tmp_list += code[cfg.ip_1[i*4+j]-1]
      return_list += parseInt(tmp_list,2).toString(16)
    return_list 

  _functionE: (code) ->
    return_list = ''
    for i in [0...48]
      return_list += code[cfg.e[i]-1]
    return_list
  _functionP: (code) ->
    return_list = ''
    for i in [0...32]
      return_list += code[cfg.p[i]-1]
    return_list
 
  _functionTos: (o,lens) ->
    return_code = ''
    for i in [0...lens]
      return_code = (o>>i & 1).toString() + return_code
    return_code
 
  _functionS: (key) ->
    return_list = ''
    for i in [0...8]
      row = parseInt(key[i*6].toString() + key[i*6+5].toString(),2)
      raw = parseInt(key[i*6+1].toString() + key[i*6+2] + key[i*6+3] + key[i*6+4],2)
      return_list += @_functionTos(cfg.s[i][row][raw],4)
    return_list

  _functionKeySecondChange: (key) ->
    return_list = ''
    for i in [0...48]
      return_list += key[cfg.pc2[i]-1]
    return_list

  _functionCharToA: (code,lens) ->
    return_code = ''
    lens = lens % 16
    for key in code
      code_ord = parseInt(key,16)
      return_code += @_functionTos(code_ord,4)
    if lens != 0
      return_code += new Array((16-lens)*4+1).join('0')
    return_code

  encode: (code, code_len, key, key_len) ->
    output = ''
    trun_len = 0
    code_string = @_functionCharToA(code, code_len)
    code_key = @_functionCharToA(key,key_len)
    real_len = code_len
    if code_len%16 != 0
      real_len = parseInt(code_len/16)*16+16

    if key_len%16!=0
      key_len = parseInt(key_len/16)*16+16
    trun_len = real_len*4
    for i in [0...trun_len] by 64
      run_code=code_string[i...i+64]
      l = i%key_len
      run_key=code_key[l...(l+64)]

      run_code= @_codefirstchange(run_code)
      run_key = @_keyfirstchange(run_key)
      for j in [0...16]
        code_r=run_code[32...64]
        code_l=run_code[0...32]
        run_code=code_r
        code_r= @_functionE(code_r)
        key_l=run_key[0...28]
        key_r=run_key[28...56]
        key_l=key_l[cfg.d[j]...28]+key_l[0...cfg.d[j]]
        key_r=key_r[cfg.d[j]...28]+key_r[0...cfg.d[j]]
        run_key=key_l+key_r
        key_y=@_functionKeySecondChange(run_key)

        code_r= @_codeyihuo(code_r,key_y)
        code_r= @_functionS(code_r)
        code_r= @_functionP(code_r)
        code_r= @_codeyihuo(code_l,code_r)
        run_code+=code_r
      code_r=run_code[32...64]
      code_l=run_code[0...32]
      run_code=code_r+code_l
      output += @_functionCodeChange(run_code)
    output

  decode: (code, code_len, key, key_len) ->
    output = ''
    trun_len = 0
    num = 0
    code_string = @_functionCharToA(code, code_len)
    code_key = @_getkey(key,key_len)
    real_len = parseInt(key_len/16)
    if key_len%16!=0
      real_len = parseInt(key_len/16)+1
    trun_len = code_len*4
    for i in [0...trun_len] by 64
      run_code=code_string[i...i+64]
      run_key=code_key[num%real_len]

      run_code= @_codefirstchange(run_code)
      for j in [0...16]
        code_r=run_code[32...64]
        code_l=run_code[0...32]
        run_code=code_r
        code_r= @_functionE(code_r)
        key_y=run_key[15-j]
        code_r= @_codeyihuo(code_r,key_y)
        code_r= @_functionS(code_r)
        code_r= @_functionP(code_r)
        code_r= @_codeyihuo(code_l,code_r)
        run_code+=code_r
      num++
      code_r=run_code[32...64]
      code_l=run_code[0...32]
      run_code=code_r+code_l
      output += @_functionCodeChange(run_code)
    output



tohex = (string) ->
  return_string = ''
  for i in string
    return_string += i.charCodeAt().toString(16)
  return_string
  
tounicode = (string) ->
  return_string = ''
  for i in [0...string.length] by 2
    return_string+=String.fromCharCode(parseInt(string[i...i+2],16))
  return_string


desdecode = (from_code,key) ->
  key = tohex(key)
  des = new Des()
  key_len = key.length
  string_len = from_code.length
  if string_len%16!=0
    return -1
  if string_len<1 or key_len<1
    return -1
  key_code= des.decode(from_code,string_len,key,key_len)
  tounicode(key_code)

desencode = (from_code,key) ->
  from_code=tohex(from_code)
  key=tohex(key)
  des = new Des()
  key_len=key.length
  string_len=from_code.length
  if string_len<1 or key_len<1
    return -1
  key_code = des.encode(from_code,string_len,key,key_len)
  key_code

exports.desencode = desencode
exports.desdecode = desdecode

start_time = '20160101'
month_time = '36'
key = "20141110"
console.log "start time, long : ",start_time ,month_time
encode_start = desencode(start_time,key) 
encode_long = desencode(month_time,key)
console.log "encode :",encode_start,"|",encode_long
decode_start = desdecode(encode_start,key)
decode_long = desdecode(encode_long,key)
console.log "decode :",decode_start,"|",decode_long
