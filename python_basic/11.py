month_num = int(raw_input("please input the month:"))
month = month_num
rabbit_num = 1
while month_num >=3:
    rabbit_num *= 2
    month_num -= 3
print rabbit_num


def rabbit_cal(month, rabbit_num = 1):
    if month < 3:
        return rabbit_num
    else:
        return rabbit_cal(month - 3, rabbit_num * 2)
import pdb
pdb.set_trace()
print rabbit_cal(month)

