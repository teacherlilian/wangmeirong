# -*- coding: gbk -*

from __future__ import division
from copy import deepcopy
#from pyExcelerator import *
import string
#from math import sqrt
import os
#import numpy as np  
from random import choice
import ReadDataSet

#����ÿ���û�����Ŀ�Ķȣ�����һ���û���5����Ŀ����Ϊ5
def getDigree(trainRatings):
    ItemDegree=dict()
    for i1 in trainRatings.keys():
        n=0
        for i2,d2 in trainRatings[i1].items():
            n+=d2
        ItemDegree[i1]=n
    return ItemDegree	   

def getItem(uid):
    O = []#��Ŀ�б�
    text = open("D:\\�Ƽ�\\BGPR-test\\base\\"+uid+".base.txt",'r+')
    for line in text.readlines():
        o = line.split('\t')[1]
        if o not in O:
           O.append(o)
    text.close()
    return O
#G:ѵ�����û������־��� trainG:�û�������ת�ƾ��� genreDict��ѵ������Ŀ�����Ծ��� ItemDgree���û���Ŀ���־�������Ŀ�ĶȾ��󣨷Ǽ�Ȩ��genreItemDgree����Ŀ���Ծ�������Ŀ�Ķ� traingenreDict����Ŀ������ת�ƾ���
def PersonalRank(G,trainG,genreDict,traingenreDict,root,max_step):
    UserGenreSim=dict()   #�û���Ŀ����֮������ƶ�
    T=dict()
    for i,d in G[root].items():
        if(trainG[i].keys())==1:
            continue
        T[i]=d/len(trainG[i].keys())      #ItemDgree[i] :�������û����� ����Tֵ
    T=dict(sorted(T.items(), key=lambda asd:asd[1], reverse = True))
    for step in  range(max_step):
        First=dict()
        Next=dict()
        Final=dict()
        #��һ��
        nn = T[list(T.keys())[0]]
        for i in T.keys():
            if len(T) == 1L][
                
            ]:
                First[i] = G[root][i]
            else:
                if  nn==T[i]:
                    First[i] = G[root][i]
                    nn = T[i]
                else:
                    break 
        #�ڶ���
        First=dict(sorted(First.items(), key=lambda asd:asd[1], reverse = True))
        Ft = list(First.keys())[0]
        if len(First)==0:
            continue
        if len(First)==1:
            Next[Ft]= G[root][Ft]
        else:
            Next[Ft]= G[root][Ft]
            for i,d in First.items():
                try:
                    if Next[Ft]>d:
                        Ft = Ft
                        break
                    else:
                        Ft = i
                        Next[Ft]=d
                except KeyError:
                    continue
        if len(Next)==0:
            continue
        for i in Next.keys():
            Next[i]=len(trainG[i].keys())
        Next=dict(sorted(Next.items(), key=lambda asd:asd[1], reverse = False))
        posion=list(Next.keys())[0]
        
        Final[posion]=Next[posion]
        for i,d in Next.items():
            if Final[posion]<d:
                break
            else:
                posion=i
                Final[posion]=d
        #������  �����ϲ��ĵ��Ӧ�����ԣ�����Ŀ���û������ƶ�ȫ��һ
        if len(Final)==0:
            continue
        Ft=choice(list(Final.keys()))
        if len(genreDict[Ft])==0:
            continue
        if len(genreDict[Ft])==1:
            if list(genreDict[Ft].keys())[0] in UserGenreSim.keys():
                UserGenreSim[list(genreDict[Ft].keys())[0]]+=1
            else:
                UserGenreSim[list(genreDict[Ft].keys())[0]]=1
        else:
            for i in genreDict[Ft].keys():
                if i in UserGenreSim.keys():
                    UserGenreSim[i]+=1
                else:
                    UserGenreSim[i]=1 
            
    UserGenreSim=dict(sorted(UserGenreSim.items(), key=lambda asd:asd[1], reverse = True))
    return UserGenreSim   
    #��ÿ�������е���Ŀ����ȴӸߵ�������                      
def getsortedgenreDict(trainG,traingenreDict):
    sortedgenre=dict()
    sg=dict()
    for genre in traingenreDict.keys():
        for i in traingenreDict[genre].keys():
            try:
                
                sg[i]=len(trainG[i].keys())
            except KeyError:
                continue
            if  genre in sortedgenre.keys():
                sortedgenre[genre].update(deepcopy(sg))  
            else:
                sortedgenre[genre]=deepcopy(sg) 
            sg.clear()
    for g in sortedgenre.keys():
        sortedgenre[g]=dict(sorted(sortedgenre[g].items(), key=lambda asd:asd[1], reverse = True))
    return sortedgenre     
def getRecommend(UserGenreSim,leng,u,G,sortedgenre,trainG):
    sumSim=0
    Recommend=[]
    
    for i,d in UserGenreSim.items():
         sumSim+=d
    for g,sim in UserGenreSim.items():
        num=0
        for item in sortedgenre[g].keys():
            if item in G[u].keys():
                continue
            if item in Recommend:
                continue
            else:
                if num==round((sim/sumSim)*leng):
                    break
                else:
                    Recommend.append(item)
                    num+=1
                
    return Recommend

def getGenreDictSim(genreDict,TransgenreDict,O):
    itemsimGenreDict={}
    sim={}
    for i in O:
        for j in O:
            if i==j:
                continue
            else:
                sim[j] = 0
                if i in itemsimGenreDict.keys():
                    itemsimGenreDict[i].update(deepcopy(sim))
                else:
                    itemsimGenreDict[i]=deepcopy(sim)
                for g in set(genreDict[i].keys()).intersection(set(genreDict[j].keys())):
                    try:
                        itemsimGenreDict[i][j]=itemsimGenreDict[i][j]+1/(len(TransgenreDict[g].keys())*len(genreDict[j].keys()))
                    except KeyError:
                        itemsimGenreDict[i][j]=itemsimGenreDict[i][j]  
    return itemsimGenreDict
    
def getItemSim(ItemDigree,UserDigree,W,O,T): 
    ItemSim={}
    itemsim={}
    for i in O:
        for j in O:
            if i == j:
                continue
            else:
                itemsim[j] = 0
                if i in ItemSim.keys():
                    ItemSim[i].update(deepcopy(itemsim))
                else:
                    ItemSim[i]=deepcopy(itemsim) 
                for u in set(T[i].keys()).intersection(set(T[j].keys())):
                    ItemSim[i][j] = ItemSim[i][j]+W[u][i]*W[u][j]/(ItemDigree[j]*UserDigree[u])
     
    return ItemSim 

def getSim(ItemSim,genreSim,O,alg):  
    sim={} 
    itemSim={}   
    for i1 in O:
        for i2 in O:
            if i1==i2:
                continue
            sim[i2]=0
            if i1 in itemSim.keys():
                itemSim[i1].update(deepcopy(sim))
            else:
                itemSim[i1]=deepcopy(sim)
            try:
                itemSim[i1][i2]=ItemSim[i1][i2]*alg+genreSim[i1][i2]*(1-alg)
            except KeyError:
                continue
            sim.clear()
    for i1 in O:
        itemSim[i1]=dict(sorted(itemSim[i1].items(), key=lambda asd:asd[1], reverse = True))
    return itemSim

#�����û�ƽ������
def avgUserF(G):
    avgUser=dict()
    for u,i in G.items():
        Sum=0
        for i,d in G[u].items():
            Sum+=d
        avgUser[u]=Sum/len(G[u].keys())
    return avgUser
"""
def getRecal(recommend,u,testSet):
    num=0
    for item in recommend:
        if item in testSet[u]:
            num+=1
    
    if len(testSet[u].keys())==0:
        return 0
    return num/len(testSet[u].keys())
    
def getCoverage(Recommend,O):
    cover=[]
    for u in Recommend.keys():
        for i in Recommend[u].keys():
            if i not in cover:
                cover.append(i)
            else:
                continue
    if len(O)==0:
        return 0
    return len(cover)/len(O)
"""
if __name__ == '__main__' :
    user=ReadDataSet.usersId("u1")
    length=[20,40,60,80,100]
    alge=[0.5]
    G=ReadDataSet.fullUsersRating("u1")
    trainG=ReadDataSet.transpose(G)
    genreDict=ReadDataSet.ItemsPros()
    traingenreDict=ReadDataSet.transpose(genreDict)
    sortedgenre=getsortedgenreDict(trainG,traingenreDict)
    ItemDigree = getDigree(trainG)
    UserDigree = getDigree(G)
    O=getItem("u1")
    genreSim=getGenreDictSim(genreDict,traingenreDict,O)  
    ItemSim=getItemSim(ItemDigree,UserDigree,G,O,trainG)
    avgUserPF=avgUserF(G)
    ff=open("���100.txt",'a+')
    for alg in alge:
        itemSim=getSim(ItemSim,genreSim,O,alg)
        for leng in length:
            #Sum=0
            summae=0
            #sumRecal=0
            #Rd={}
            ff.writelines("�Ƽ��б���Ϊ"+str(leng)+'\n')
            for u in user:
                UserGenreSim= PersonalRank(G,trainG,genreDict,traingenreDict,u,100)
                Recom=getRecommend(UserGenreSim,leng,u,G,sortedgenre,trainG) #����һ����20�����ԣ�����ȡ������Ŀ���û����Ƶ�����
                #����Ԥ������
                Predict=dict()
                testSet = ReadDataSet.testData("u1",user)      #���Լ��û����־���
                for i1 in Recom:
                    num=0
                    sumnum=0
                    sumsim=0
                    try:
                    
                        for i2,d in itemSim[i1].items():
                            if num ==20:       
                                break
                            if i1 == i2:
                                continue
                            if i2 not in G[u].keys():
                                continue
                            else:
                                if G[u][i2]==0:
                                    sumnum+=0
                                    sumsim+=abs(itemSim[i1][i2])
                                    num+=1
                                else:
                                    sumnum+=itemSim[i1][i2]*(G[u][i2]-avgUserPF[u])
                                    sumsim+=abs(itemSim[i1][i2])
                                    num+=1
                    except KeyError:
                        Predict[i1]=0
                        continue
                    if sumsim==0:
                        sumnum=0
                    else:
                        sumnum/=sumsim
                    Predict[i1]=sumnum+avgUserPF[u]
                Predict = dict(sorted(Predict.items(),key=lambda asd:asd[1], reverse = True))
                mae=0
                n=0
                for i in testSet[u].keys():
                    if i  in Recom:
                        mae+=abs(Predict[i]-testSet[u][i])
                        n=n+1
                    else:
                        continue
                
                if n == 0:
                    mae=0
                else:
                    mae=mae/n
                summae=summae+mae
                """
                #����׼ȷ��    
                qq=[]
                for i in Recom:
                    if i in testSet[u].keys():
                        qq.append(i)  
                allmovies=len(Recom)
                factmovies=len(qq)
                if allmovies==0:
                    p=0           #�����Ƽ��б�Ϊ�յ����
                else:
                    p=factmovies/allmovies
            
                recal=getRecal(Recom,u,testSet)
                sumRecal+=recal
                Sum = Sum+p
                summae=summae+mae
                r={}	
                for i in Recom:
                    r[i]=0      #ֵ��������ν
                    if u in Rd.keys():
                        Rd[u].update(deepcopy(r))
                    else:
                        Rd[u]=deepcopy(r)
                    r.clear()
            Coverage=getCoverage(Rd,trainG.keys())
            """
            ff.writelines("alg:"+str(alg)+"ƽ��maeΪ��"+str(summae/len(user))+'\n') 
    ff.close()
            
