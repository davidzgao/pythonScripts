#! /usr/bin/python
class Derivative(object):
    def __init__(self, e = 0.0001, *argvs):
        self.e = e
        self.argvs = []
        for i in argvs:
            self.argvs.append(i)
        print self.argvs
    
    def calculate_mi(self, x, time):
        y = 1
        for i in range(time):
            y = x * y
        return y

    def calculate_multifunc(self, x):
        #import pdb 
        #pdb.set_trace()
        max_mi = len(self.argvs) - 1
        result_value = 0
        for i in range(max_mi):
            result_value += self.argvs[i] * self.calculate_mi(x, max_mi - i)
        return result_value

    def calculate_derivate(self, x):
        print (self.calculate_multifunc(x + self.e) - self.calculate_multifunc(x - self.e)) / (2* self.e)

        
der1 = Derivative(0.0001 , 5, 3 , 1 , 0) 
der1.calculate_derivate(2)



