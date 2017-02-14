import pandas as pd
import math
import Grad

def somefunc(MatrixA, MatrixB, MatrixD, X, i, ver):
    MultRes1, MultRes2 = 0,0
    for j in range(len(MatrixA.columns)):
        MultRes1 += MatrixA.iloc[i][j] * X.iloc[j]
        MultRes2 += math.pow(X.iloc[j]*MatrixD.iloc[i][j],2)

    return -MatrixB.iloc[i] + MultRes1 + ver*math.sqrt(MultRes2)

def func1(MatrixC, MatrixA, MatrixB, MatrixD, r, b, p, ver):
    X = pd.Series(index=range(len(MatrixA.columns)))
    J = pd.Series(index=range(len(MatrixA.columns)+len(MatrixA.index)))
    a = 0
    l=0
    g = Grad.Grad()

    for i in range(len(MatrixA.columns)):
        X.iloc[i] = 100
    while True:
        r= b*r
        a = 0
        l+=1

        X=g.GradientMethod1(MatrixA,MatrixB,MatrixC,MatrixD,J,r,p,X,ver)
        for i in range(len(MatrixA.index)):
            if 0>somefunc(MatrixA, MatrixB, MatrixD, X, i, ver):
                J.iloc[i]=0
            else:
                J.iloc[i]=1
        for i in range(len(X.index)):
            if 0>(-X.iloc[i]):
                J.iloc[len(MatrixA.index)+i]=0
            else:
                J.iloc[len(MatrixA.index)+i]=1
        MultRes3, MultRes4 = 0,0
        for i in range(len(MatrixA.index)):
            MultRes3 += J.iloc[i]*math.pow(somefunc(MatrixA, MatrixB, MatrixD, X, i,ver),p)
        MultRes5 = 0
        for i in range(len(MatrixA.columns)):
            MultRes5 += J.iloc[len(MatrixA.index)+i]*math.pow((X.iloc[i]),p)
        a = MultRes5 + MultRes3
        print(a)
        if a*r < 0.1 or l >=10:
            break
    return X

def func2(MatrixC, MatrixA, MatrixB, MatrixD, r, b, p, ver):
    X = pd.Series(index=range(len(MatrixA.columns)))
    J = pd.Series(index=range(len(MatrixA.columns)+len(MatrixA.index)))
    a = 0
    mul=0
    l = 0
    m = Grad.Grad()

    for i in range(len(MatrixA.columns)):
        X.iloc[i] = 100
    while True:
        r=b*r
        a=0
        l+=1
        X = m.GradientMethod2(MatrixA,MatrixB,MatrixC,MatrixD,J,r,p,X,ver)
        for i in range(len(X.index)):
            X.iloc[i] = int(X.iloc[i])
        for i in range(len(MatrixA.index)):
            if 0>somefunc(MatrixA, MatrixB, MatrixD, X, i, ver):
                J.iloc[i]=0
            else:
                J.iloc[i]=1
        for i in range(len(X.index)):
            if 0>(-X.iloc[i]):
                J.iloc[len(MatrixA.index)+i]=0
            else:
                J.iloc[len(MatrixA.index)+i]=1
        MultRes3, MultRes4 = 0,0
        for i in range(len(MatrixA.index)):
            MultRes3 += J.iloc[i]*math.pow(somefunc(MatrixA, MatrixB, MatrixD, X, i,ver),p)
        MultRes5 = 0
        for i in range(len(MatrixA.columns)):
            MultRes5 += J.iloc[len(MatrixA.index)+i]*math.pow((X.iloc[i]),p)
        a = MultRes5 + MultRes3
        print('h'+str(a))
        if a*r < 0.1 or l>=10:
            break
    return X