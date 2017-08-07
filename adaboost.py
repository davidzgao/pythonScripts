#! /usr/env/bin/python

import sys
import math


class subClassfier(object):
    def __init__(self, pointList, weightList = None):
        self.ptList = pointList
        if weightList != None:
            self.wtList = weightList
        else:
            self.wtList = [1.0/len(pointList) for i in range(len(pointList))]
        self.precise = 0
        self.error = 0
        self.alpha = 0
        self.cutPoint = 0
        self.reverse = False
         
    def train(self):
        minNumError = 1
        minCutPoint = 0
        minReverse = False
        for j in range(-1,len(self.ptList),):
            cutPoint = j + 0.5
            numError = 0
            reverse = False
            for i in range(len(pointList)):
                point = self.ptList[i]
                weight = self.wtList[i]
                if i < cutPoint and point[1] == 1:
                    numError += weight
                elif i > cutPoint and point[1] == -1 :
                    numError += weight
                else:
                    continue
            if numError > 0.5:
                reverse = True
                numError = 1 - numError
            if numError < minNumError:
                minNumError = numError
                minCutPoint = cutPoint
                minReverse = reverse
        self.cutPoint = minCutPoint
        self.error = minNumError
        self.precise = 1 - self.error
        self.reverse = minReverse
        self.alpha = 0.5*math.log(self.precise/self.error)

    def judge(self,point):
        judgeValue = 1 
        if self.cutPoint > point[0]:
            judgeValue = -1
        if self.reverse == True:
            judgeValue = -judgeValue
        return judgeValue


    def show_para(self):
        print "---------Sub Classfier Model---------\nerror: %f\ncutPoint: %f\nalpha:%f\nreverse:%s\n--------------"%(self.error,self.cutPoint, self.alpha, self.reverse)
        


class adaBoost(object):
    def __init__(self, pointList , max_error_rate = 0.1):
        self.ptList = pointList
        self.wtList = []
        self.subClassfierList = []
        self.model_error = 1
        self.max_error_rate = max_error_rate

    def judgePoint(self, point):
        judgeValue = 0
        for i in self.subClassfierList:
            judgeValue += i.alpha * i.judge(point)
        if judgeValue >= 0 :
            return 1
        else:
            return -1

    def calModelError(self):
        errorNum = 0 
        for point in self.ptList:
            if self.judgePoint(point) != point[1]:
                errorNum += 1
        return errorNum * 1.0/len(self.ptList)
    def train(self):
        dataLen = len(self.ptList)
        self.wtList = [1.0/dataLen for i in range(dataLen)]
        import pdb
        pdb.set_trace()
        subClsfier = subClassfier(self.ptList, self.wtList)
        subClsfier.train()
        subClsfier.show_para()
        self.subClassfierList.append(subClsfier)
        print "now model error is:",self.calModelError()
        while self.calModelError() > self.max_error_rate:
            Zm = 0
            alpha = subClsfier.alpha
            for i in range(dataLen):
                point = self.ptList[i]
                weight = self.wtList[i]
                Wm = weight * math.exp(-1 * alpha * point[1] * subClsfier.judge(point))
                self.wtList[i] = Wm
                Zm += Wm
            for i in range(dataLen):
                self.wtList[i] = self.wtList[i]/Zm
            #print self.wtList
            subClsfier = subClassfier(self.ptList, self.wtList)
            subClsfier.train()
            subClsfier.show_para()
            self.subClassfierList.append(subClsfier)
            print "now model error is:",self.calModelError()
        self.model_error = self.calModelError()

    def show_para(self):
        print "ModelError: %f\nmax error rate:%f\n"%(self.model_error,self.max_error_rate)
        


pointList = [(0,1),(1,1),(2,1), (3,-1),(4,-1),(5,-1),(6,1),(7,1),(8,1),(9,-1)]
#simpleClassfier = subClassfier(pointList)
#simpleClassfier.train()
#simpleClassfier.show_para()
ada_boost = adaBoost(pointList)
ada_boost.train()
ada_boost.show_para()
