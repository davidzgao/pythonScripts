#! /usr/bin/python
# -*- coding:utf-8 -*-
import re
import jieba
import random
import codecs

class Markov(object):
    def __init__(self, filepath = None, mode = 0, coding = 'utf-8'):
        self.dictLen = 0
        self.Cap = set()
        self.mode = mode
        self.coding = coding
        self.dic = {}
        self.filepath = filepath
        
    def get_dic(self):
        print self.dic


    def train(self):
        if self.filepath is None :
            return
        eg_puncmark = re.compile("[\,\.\!\;\?\~\`\#\$\%\@\^&\*\(\)\]\[]")
        ch_puncmark = re.compile("[，。！；]")
        ch_puncstr = u"，。！；"
        fopen = codecs.open(self.filepath, 'r', self.coding)
        mode = self.mode
        for line in fopen.readlines():
            line = line.strip()
            if mode == 0:
                sentences = eg_puncmark.split(line)
                for sentence in sentences:
                    words = filter(lambda x:x != "",sentence.split(" "))
                    for i in range(len(words) - 2):
                        keypair = words[i] + " " + words[i+1]
                        if i == 0 and keypair[0].upper() == keypair[0]:
                            self.Cap.add(keypair)
                        if keypair not in self.dic:
                            self.dic[keypair] = [words[i+2]]
                        else:
                            self.dic[keypair].append(words[i+2])
            elif mode == 1:
                sentences = ch_puncmark.split(line)
                for sentence in sentences:
                    #print sentence
                    words = jieba.cut(sentence)
#                    words = filter(lambda x:x != "" and re.search(x,ch_puncstr) == None ,list(words))
                    words = filter(lambda x:x != "",list(words))
                    for i in range(len(words) - 2):
                        keypair = words[i] + " " + words[i+1]
                        if i == 0:
                            self.Cap.add(keypair)
                        if keypair not in self.dic:
                            self.dic[keypair] = [words[i+2]]
                        else:
                            self.dic[keypair].append(words[i+2])
        self.dictLen = len(self.dic)
    def say(self, len_sent):
        if self.dictLen <=2 :
            print("i feel tired and i need food to say something")
        else:
            self.Cap_list = list(self.Cap) 
            keypair = self.Cap_list[random.randint(0,len(self.Cap_list))]
            first,second = keypair.split(" ")
            if self.mode == 0:
                sentence_new = first + " " + second
            else:
                sentence_new = first + second
            for i in range(2, len_sent):
                if keypair in self.dic:
                    first = second
                    int_tmp = random.randint(0,len(self.dic[keypair]) - 1)
                    second = self.dic[keypair][int_tmp]
                    keypair = first + " " + second
                    if self.mode == 0:
                        sentence_new +=  " " + second
                    elif self.mode == 1:
                        sentence_new +=  second   
                else:
                    break
            if self.mode == 0:
                sentence_new += "."
            else:
                sentence_new += u"。"
            print sentence_new
    def test(self):
        print u'\u6b63\u662f \u585e\u5317'
        if u'\u6b63\u662f \u585e\u5317' in self.dic:

            print self.dic[u'\u6b63\u662f \u585e\u5317']

           
if __name__ == "__main__":
    markov = Markov("The_Standard_Bearer.txt")
    #markov = Markov("swords.txt", 1)
    markov.train()
    #markov.test()
    #markov.get_dic()
    markov.say(20)
    markov.say(20)
    markov.say(20)
                    
            
    
                
                    
              


