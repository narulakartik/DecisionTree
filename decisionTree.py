# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 21:24:21 2020

@author: narul
"""

import numpy as np
import sys


class Node:
    def __init__(self, key, depth, attribute):
        self.left=None
        self.right=None
        self.key=key
        self.depth=depth
        self.attribute=attribute
        self.x=0
        

def gini_impurity(dataset):
     
     if len(dataset.key)==0:
         return 0
     else:
         
         no_of_attr=len(dataset.key[0])-1
         size=len(dataset.key)
    
         a=dataset.key[0][no_of_attr]
     
     
         i=0
         c1=0
         c2=0
         while(i<size):
            if dataset.key[i][no_of_attr]==a:
                c1+=1
            else:
                c2+=1
            i+=1 
         gini=1-(c1*c1)/(size*size)-(c2*c2)/(size*size)
         return gini


def max_gini_gain(dataset):

     no_of_attr=len(dataset.key[0])
     size=len(dataset.key)
     a=dataset.key[0][no_of_attr-1]
     data1=[]
     data2=[]
     gini_gain=[]
     x=[]
     i=0
     j=0
     m=no_of_attr-1
     while i<m:
         j=0
         count1=0
         count2=0
         b=dataset.key[0][i]
         while j<size: 
             if dataset.key[j][i]==b:
                 data1.append(dataset.key[j])
                 count1+=1
             elif dataset.key[j][i]!=b:
                 
                 data2.append(dataset.key[j])
                 count2+=1
             j+=1
         d1=np.asarray(data1)
         d2=np.asarray(data2)    
         D1=Node(d1,1,0)
         D2=Node(d2,1,0)
         gini=(count1/size)*gini_impurity(D1)+(count2/size)*gini_impurity(D2)
         gini_g=gini_impurity(dataset)-gini
         gini_gain.append(gini_g)
         data1.clear()
         data2.clear()
         i=i+1
     
     
         
     return gini_gain


def majoritycount(dataset):
    size=len(dataset.key)
    i=0
    no_of_attr=len(dataset.key[0])-1
    a=dataset.key[0][no_of_attr]
    count1=0
    count2=0
    
    while i<size:
        if dataset.key[i][no_of_attr]==a:
            count1+=1
        else:
            count2+=1
            majority=dataset.key[i][no_of_attr]
            b=dataset.key[i][no_of_attr]
        i+=1
    if count1>count2:
        majority=a
    elif count1==count2:
        if b>a:
            majority=b
        else :
            majority=a
      
        
    return majority    
        
class Attribute:
    def __init__(self, index, key):
        self.index=index
        self.key=key
        
def best_attribute(dataset):
    f=max(max_gini_gain(dataset))
    t=max_gini_gain(dataset).index(f)
    if f>0:
     return Attribute(t, dataset.key[0][t])
    else:
        return None
def data_split(dataset, f):
    data1=[]
    data2=[]
    
    a=dataset.key[0][f]
    i=0
   
    while i<len(dataset.key):
        if dataset.key[i][f]==a:
            data1.append(dataset.key[i])
            
        else:
            data2.append(dataset.key[i])
        i=i+1
    d1=np.asarray(data1)
    d2=np.asarray(data2)
    D1=Node(d1,1,0)
    D2=Node(d2,1,0)    
    return D1, D2
    

def DecisionTree(dataset, maxdepth, depth):
    if maxdepth==0:
        dataset.x=1
    dataset.depth=depth
    depth+=1
   
    
    no_of_attr=len(dataset.key[0])-1
    m=min(no_of_attr, maxdepth)
    f=best_attribute(dataset)
    dataset.attribute=f
    
    if f==None or depth>m:
       
        dataset.x=1
        a=dataset.key[0][no_of_attr]
        i=0
        b=1
        count1=0
        count2=0
        while i<len(dataset.key):
         if dataset.key[i][no_of_attr]==a:
             count1+=1
         else:
             count2+=1
             b=dataset.key[i][no_of_attr]
         i+=1
      #  print(count1, a, count2,b) 
    
        return (dataset)
      
    i=0
    count1=0
    count2=0
    a=dataset.key[0][no_of_attr]
    while i<len(dataset.key):
         if dataset.key[i][no_of_attr]==a:
             count1+=1
         else:
             count2+=1
             b=dataset.key[i][no_of_attr]
         i+=1
    
   
    #print(count1, a, count2, b) 
    
      
     
   
  #  print(f.key)
    D1, D2=data_split(dataset, f.index)
    dataset.left=D1
    dataset.right=D2
    DecisionTree(dataset.left, maxdepth, depth)
    DecisionTree(dataset.right, maxdepth, depth)
  
    return dataset

def predict(tree, dataset):
   if tree.x==1:
       
       return majoritycount(tree)



   
   if dataset[tree.attribute.index]==tree.attribute.key:
               return predict(tree.left, dataset)
   else:
               return predict(tree.right, dataset)
           
    
if __name__ == "__main__" :
    
    
    train_in=open("politicians_train.tsv","r")
    test_in=open("politicians_test.tsv","r")
    train_out=open("train_out.labels", "w")
    test_out=open("test_out.labels", "w")
    metrics=open("metrics.txt", "w")
    maxdepth=3
    train_data = np.genfromtxt(train_in, delimiter='\t', dtype='str', skip_header=1)
    test_data=np.genfromtxt(test_in, delimiter='\t', dtype='str', skip_header=1)
    test=Node(test_data,0,0)
    train=Node(train_data,0,0)
    tree = DecisionTree(train,maxdepth,0)
   
    
    
    #testing
    labels=[]
    i=0
    size=len(test.key)
    while i<size:
         labels.append(predict(tree,test.key[i]))
         test_out.write(predict(tree, test.key[i]))   
         test_out.write("\n")
         i+=1
    i=0
    error=0
    no_of_a=len(test.key[0])-1
    
    while i<len(test.key):
      if test.key[i][no_of_a]!=labels[i]:
          error+=1
      i+=1
      
    meanerror_test=error/len(test.key)

   
    
    
    
    
    #training
    
    
    labels=[]
    i=0
    size=len(train.key)
    while i<size:
         labels.append(predict(tree,train.key[i]))
         train_out.write((predict(tree,train.key[i])))
         train_out.write("\n")
         i+=1
    i=0
    error=0
    no_of_a=len(train.key[0])-1
  
    
    while i<len(train.key):
      if train.key[i][no_of_a]!=labels[i]:
          error+=1
      i+=1
      
    meanerror_train=error/len(train.key)
    print(meanerror_train)
    print(meanerror_test)
  
    
    
    #write error file
    metrics.write("error(train): ")
    metrics.write(str(meanerror_train))
    metrics.write("\n")
    
    metrics.write("error(test): ")
    metrics.write(str(meanerror_test))
    metrics.write("\n")
    
  
    

        