#import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import random as rd
from sklearn.neighbors import KNeighborsRegressor as nnr
import random
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import copy
from sklearn.metrics import max_error

EPSILON = 1e-10

def mape(y,yp):
    #z=np.array([v!=0 and v or vt for v,vt in zip(y,yp)])
    r=np.abs((y-yp)/(y))
    r=r/len(r)
    return r.sum()

def smape(y,yp):
    c=(np.abs(y)+np.abs(yp))/2
    r= np.abs(y-yp)/c
    #print(y.shape,yp.shape)
    return np.mean(r)


def rmse(y,yp):
    r= mean_squared_error(y,yp)
    return np.sqrt(r)

def wsplit(data, m, tau):
    l,i=len(data),0
    n=l-m*tau
    x,y=[[] for k in range(n)],[0 for k in range(n)]
    while i+m*tau<l:
        ind=[0 for k in range(m)]
        for j in range(m):
            val= i+j*tau
            ind[j]=val
        x[i]=data[ind]
        y[i]=data[ind[-1]+tau]
        i+=1
    data=np.array(x)
    target=np.array(y)
    return data, target


class KNNR:
    def __init__(self, m=3, tau=1, k=5, prediction_size=24, w='uniform',
                 d='minkowski'):
        self.m=m
        self.tau=tau
        self.w=w
        self.k=k
        self.w=w
        self.d=d
        self.prediction_size=prediction_size
        

    def fit(self,data,target):
        self.data,self.target=data,target
        #a = self.d in ['cosine' and 'brute' or 'auto'
        self.regressor=nnr(n_neighbors=self.k, weights=self.w, algorithm='auto', metric=self.d)
        self.regressor.fit(self.data,self.target)
        return self
    
    def _forecast(self,n,s):
        pred=[]
        m,tau,nn,d,w=self.m,self.tau,self.k,self.d,self.w
        ind=[-i for i in range(m*tau,0,-tau)]
        while len(pred)<n:
            window=list(np.nan_to_num(s[ind],np.mean(s[ind])))
            val=self.regressor.predict([window])
            pred.append(val[0])
            s=np.append(s,val[0])
        return np.array(pred)

    def predict(self,n=None):
        if n is None:
            n=self.prediction_size
        return self._forecast(n,self.target)

