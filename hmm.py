#! /usr/env/bin python
import math
import numpy as np

class forwardAlg(object):
    def __init__(self, A, B, pi):
        self.pi = pi
        self.A = A
        self.B = B
        self.alpha = [0 for i in range(len(self.A))]
        self.popularity = 0
    def cal_output_popularity(self,output_list):
        for i in range(len(self.A)):
            self.alpha[i] = self.pi[i] * self.B[i][output_list[0]]
        for i in range(1,len(output_list)):
            tmp_array = np.dot(self.alpha , self.A)
            for j in range(len(tmp_array)):
                tmp_array[j] = tmp_array[j] * self.B[j][output_list[i]]
            self.alpha = tmp_array
        p_value = 0
        for i in self.alpha:
            p_value += i
        self.popularity = p_value
    def print_output(self):
        print "the forwardAlg calculate result is "
        print self.popularity

class backwardAlg(object):
    def __init__(self, A, B, pi):
        self.pi = pi
        self.A = A
        self.B = B
        self.beta = [ 0 for i in range(len(self.A))]
        self.popularity = 0
    def cal_output_popularity(self, output_list):
        length_out = len(output_list)
        for i in range(len(self.A)):
            self.beta[i] = 1
        for i in range(length_out-2, -1, -1):
            tmp_array = [ 0 for w in range(len(self.A))]
            for j in range(len(self.A)):
                for k in range(len(self.A)):
                    tmp_array[j] += self.A[j][k]* self.B[k][output_list[i+1]] * self.beta[k] 
            self.beta = tmp_array
        p_value = 0
        for i in range(len(self.A)):
            p_value += self.pi[i] * self.B[i][output_list[0]] * self.beta[i]
        self.popularity = p_value

    def print_output(self):
        print "the backwardAlg calculate result is "
        print self.popularity


class veterbiAlg(object):
    def __init__(self, A, B, pi, output_list):
        self.A = A
        self.B = B
        self.pi = pi
        self.output_list = output_list
        self.delta_list = [ [0 for j in range(len(self.A))] for i in range(len(self.output_list))]
        self.input_list = [0 for i in range(len(self.output_list))]

    def find_inputlist(self):
        print self.delta_list
        for i in range(len(self.A)):
            self.delta_list[0][i] = self.pi[i] * self.B[i][self.output_list[0]]
        for j in range(1, len(self.output_list)):
            tmp_list = [0 for w in range(len(self.A))]
            for i in range(len(self.A)):
                for k in range(len(self.A)):
                    if self.delta_list[j-1][k] * self.A[k][i] > tmp_list[i]:
                        tmp_list[i] = self.delta_list[j-1][k] * self.A[k][i]
                tmp_list[i] = tmp_list[i] * self.B[i][self.output_list[j]]
            self.delta_list[j] = tmp_list
        print self.delta_list
        #import pdb
        #pdb.set_trace()
        tmp_value = 0
        for i in range(len(self.delta_list[-1])):
            if self.delta_list[-1][i] > tmp_value:
                self.input_list[-1] = i
                tmp_value = self.delta_list[-1][i]
        for i in range(len(self.delta_list)-2, -1 ,-1):
            tmp_value = 0
            next_i = self.input_list[i+1]
            for j in range(len(self.A)):
                if self.delta_list[i][j] * self.A[j][next_i] > tmp_value:
                    tmp_value = self.delta_list[i][j] * self.A[j][next_i]
                    self.input_list[i] = j
        print "most valuable route:",self.input_list


pi = np.array([0.2,0.4,0.4])
A = np.array([[0.5,0.2,0.3],[0.3,0.5,0.2],[0.2,0.3,0.5]])
B = np.array([[0.5,0.5],[0.4,0.6],[0.7,0.3]])
output_list = [0,1,0]
print "pi:\n %s \nA:\n %s\nB:\n %s"%(pi, A, B)

f1 = forwardAlg(A, B , pi)
f1.cal_output_popularity(output_list)
f1.print_output()

b1 = backwardAlg(A, B, pi)
b1.cal_output_popularity(output_list)
b1.print_output()


v1 = veterbiAlg(A, B, pi, output_list)
v1.find_inputlist()








        
        


