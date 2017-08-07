#! /usr/bin/python
# 1,2,3,4 four number, how many three_number can they make

cnt = 0
num_list = []
for i in range(1,5):
    for j in range(1,5):
        if j != i:
            for k in range(1,5):
                if k != i and k != j:
                    cnt +=1 
                    num_list.append(i*100 + j * 10 +k)

print cnt
print num_list
