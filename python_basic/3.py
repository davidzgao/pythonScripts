# x+ 100 is sqrt, x + 168 is sqrt ,what x
import math
for i in range(-100,168):
    if math.sqrt(i + 100)%1 == 0 and math.sqrt(i+168)%1 == 0:
        print i
