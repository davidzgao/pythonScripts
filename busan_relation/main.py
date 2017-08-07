# -*- coding: utf-8-*-

import jieba
import os
#jieba.load_userdict("dict.txt")
import codecs
from jieba import posseg


class BusanAnalyzer(object):
    def __init__(self,file_dir,dict_dir = None):
        self.names = {}
        self.relations = {}
        self.para_rela_list = []
        self.file_dir = file_dir
        self.userdict_dir = dict_dir
        if self.userdict_dir is not None:
            jieba.load_userdict(self.userdict_dir)

    def read_file(self):
        with codecs.open(self.file_dir,'r','utf8') as f:
            for line in f.readlines():
                self.para_rela_list.append([])
                for w in posseg.cut(line):
               #     print w
                    if w.flag != 'nr' or len(w.word) <2:
                        continue
                    if w.word not in self.names:
                        self.names[w.word] = 1
                        
                    else:
                        self.names[w.word] += 1
                    self.para_rela_list[-1].append(w.word)

    def show_names(self):
        list_sorted = sorted(self.names.items(),key = lambda x:x[1],reverse = True)
        for ituple in list_sorted:
            print ituple[0],ituple[1]
   
    def static_relation(self):
        for ilist in self.para_rela_list:
            for name1 in ilist:
                for name2 in ilist:
                    if name1 != name2:
                        if name1 not in self.relations:
                            self.relations[name1] = {}
                        if name2 not in self.relations[name1]:
                            self.relations[name1][name2] = 1
                        else:
                            self.relations[name1][name2] += 1


    def show_relations(self):
        for name1,name1_dic in self.relations.items():
            print "--------\n",name1
            for name2,times in name1_dic.items():
                print "     ",name2,times

    def out2file(self):
        with codecs.open("node_out.txt","w","gbk") as f_node:
            f_node.write("Id Label Weight\r\n")
            for name,times in self.names.items():
                f_node.write("%s %s %d\n"%(name,name,times))
        with codecs.open("edge_out.txt","w", "gbk") as f_edge:
            f_edge.write("Source Target Weight\r\n")
            for name1 , name1_dic in self.relations.items():
                for name2,values in name1_dic.items():
                    #print name1,name2,values
                    f_edge.writelines("%s %s %d\r\n"%(name1, name2 ,values))

        f_node.close()
        f_edge.close()
            



if __name__=="__main__":
    analyzer = BusanAnalyzer("1988.txt" , "1988_user.txt")
    #analyzer = BusanAnalyzer("busan.txt", "dict.txt")
    analyzer.read_file()
    analyzer.show_names()
    analyzer.static_relation()
    analyzer.show_relations()
    analyzer.out2file()
