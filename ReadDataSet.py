# -*- coding: gbk -*
from __future__ import division
from copy import deepcopy
import string
#from math import sqrt
#import numpy as np   #这是使用的numpy模块中的随机函数
import os
#获取测试集中的用户编号
def usersId(uid):
    userSet = []    #测试集中的用户列表  
    for i in os.listdir("D:\\推荐\\BGPR-test\\test\\"+uid+".test"):
        userSet.append(i)
    ulist = ''.join(userSet)   #以空格（及直接连接各个元素）作为分隔符，将userSet所有的元素合并成一个新的字符串
    userSet = ulist.split('.txt')
    del userSet[-1]
    return userSet



def fullUsersRating(uid):                      #所有用户对应的用户对项目的评分
    W=dict()
    w=dict()
    O=[]
    UIFile=open("D:\\推荐\\BGPR-test\\base\\"+uid+".base.txt","r+")
    for line in UIFile.readlines():
        u=line.split('\t')[0]
        o=line.split('\t')[1]
        rating=line.split('\t')[2]
        if o not in O:
            O.append(line.split('\t')[1])
        w[o]=int(rating)
        if u in W.keys():
            W[u].update(deepcopy(w))
        else:
            W[u]=deepcopy(w)
        w.clear()
    UIFile.close()  
    return W



#评分矩阵转置 格式为：{项目1:{用户1:评分,用户2:评分,用户3:评分},项目2:{用户1:评分,用户2:评分,用户3:评分}}
def transpose(matrix):
    I=dict()
    i=dict()
    for user in matrix:
        for item,rating in matrix[user].items():
            i[user]=rating
            if item not in I:
                I[item]=deepcopy(i)
            else:
                I[item].update(deepcopy(i))
            i.clear()
    return I
    
    
    
#项目属性矩阵
def ItemsPros():  
    genre={}
    l=[]
    UIFile=open("D:\\推荐\\BGPR-test\\u.txt","r+",encoding='gb18030',errors='ignore')
    for line in UIFile.readlines():
        tempList=line.split('|')
        #取出项目每个属性对应的值，因为最后一个带\n，故需要处理
        for g in tempList[-19:-1]:								#从倒数第19个到倒数第一个   0和1的字符串
            l.append(float(g))
        l.append(float(tempList[-1][0]))					#tempList中倒数第一个字符串的第一个字符(最后一个字符)
        item=tempList[0]                         
        genre[item]=deepcopy(l)										#item为项目编号
        l=[]
    UIFile.close()
    
    genreDict=dict()
    temp=dict()
    for gr in genre:
        count=1
        for gl in genre[gr]:
            if gl==1:
                temp[str(count)]=1							#temp[count] =1，   count：遍历20个二进制中值为1此时它是第几个数
            count=count+1
        genreDict[gr]=deepcopy(temp)						#genreDict[项目编号]={count1：1，count2：1}  各人认为20个二进制对应20个分类，值为1的项目属于那个类
        temp.clear()
    return genreDict

#测试集中用户的评分矩阵

def testData(uid,testUsers):
    testSet={}
    for u in testUsers:
        tf=open("D:\\推荐\\BGPR-test\\test\\"+uid+".test\\"+u+".txt","r+")
        ti=dict()
        for line in tf.readlines():
            splitLine=line.split(',')
            ii=splitLine[1]
            rr=int(splitLine[2])
            ti[ii]=rr
        if u in testSet:
            testSet[u].update(deepcopy(ti))
        else:
            testSet[u]=deepcopy(ti)
        ti.clear()
        tf.close()
    return testSet

