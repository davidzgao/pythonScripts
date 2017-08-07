tmp_list = []
for num in range(101,200):
    not_su = False
    for i in range(2,num):
        if num%i == 0:
            not_su = True
            break
    if not not_su:
        tmp_list.append(num)

print len(tmp_list),tmp_list
