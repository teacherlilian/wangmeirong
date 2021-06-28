# -*- coding: gbk -*
from __future__ import division
from copy import deepcopy
import string
#from math import sqrt
#import numpy as np   #����ʹ�õ�numpyģ���е��������
import os
#��ȡ���Լ��е��û����
def usersId(uid):
    userSet = []    #���Լ��е��û��б�  
    for i in os.listdir("D:\\�Ƽ�\\BGPR-test\\test\\"+uid+".test"):
        userSet.append(i)
    ulist = ''.join(userSet)   #�Կո񣨼�ֱ�����Ӹ���Ԫ�أ���Ϊ�ָ�������userSet���е�Ԫ�غϲ���һ���µ��ַ���
    userSet = ulist.split('.txt')
    del userSet[-1]
    return userSet



def fullUsersRating(uid):                      #�����û���Ӧ���û�����Ŀ������
    W=dict()
    w=dict()
    O=[]
    UIFile=open("D:\\�Ƽ�\\BGPR-test\\base\\"+uid+".base.txt","r+")
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



#���־���ת�� ��ʽΪ��{��Ŀ1:{�û�1:����,�û�2:����,�û�3:����},��Ŀ2:{�û�1:����,�û�2:����,�û�3:����}}
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
    
    
    
#��Ŀ���Ծ���
def ItemsPros():  
    genre={}
    l=[]
    UIFile=open("D:\\�Ƽ�\\BGPR-test\\u.txt","r+",encoding='gb18030',errors='ignore')
    for line in UIFile.readlines():
        tempList=line.split('|')
        #ȡ����Ŀÿ�����Զ�Ӧ��ֵ����Ϊ���һ����\n������Ҫ����
        for g in tempList[-19:-1]:								#�ӵ�����19����������һ��   0��1���ַ���
            l.append(float(g))
        l.append(float(tempList[-1][0]))					#tempList�е�����һ���ַ����ĵ�һ���ַ�(���һ���ַ�)
        item=tempList[0]                         
        genre[item]=deepcopy(l)										#itemΪ��Ŀ���
        l=[]
    UIFile.close()
    
    genreDict=dict()
    temp=dict()
    for gr in genre:
        count=1
        for gl in genre[gr]:
            if gl==1:
                temp[str(count)]=1							#temp[count] =1��   count������20����������ֵΪ1��ʱ���ǵڼ�����
            count=count+1
        genreDict[gr]=deepcopy(temp)						#genreDict[��Ŀ���]={count1��1��count2��1}  ������Ϊ20�������ƶ�Ӧ20�����ֵ࣬Ϊ1����Ŀ�����Ǹ���
        temp.clear()
    return genreDict

#���Լ����û������־���

def testData(uid,testUsers):
    testSet={}
    for u in testUsers:
        tf=open("D:\\�Ƽ�\\BGPR-test\\test\\"+uid+".test\\"+u+".txt","r+")
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

