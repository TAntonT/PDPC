import pandas as pd
import math

class Grad():
    def GetNorm(self,x):
        res = 0
        for i in range(len(x.index)):
            res += math.pow(x.iloc[i], 2)
        res = math.sqrt(res)
        return res

    def GetDelta(self, v1, v2):
        res = pd.Series(index=v1.index)
        for i in range(len(res.index)):
            res.iloc[i] = v1.iloc[i]-v2.iloc[i]
        return res

    def FunctionF1(self, MatrixA, lumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver):
        MultRes3 = 0
        MultRes4 = 0
        for i in range(len(MatrixA.columns)+len(MatrixA.index)):
            MatrixJ.iloc[i] = 1
        X = []
        X.append(lumbda.iloc[0]+lumbda.iloc[1])
        X.append(lumbda.iloc[2]+lumbda.iloc[3]+lumbda.iloc[4])
        X.append(lumbda.iloc[5]+lumbda.iloc[6])

        for i in range(len(MatrixA.index)):
            MultRes1 = 0
            MultRes2 = 0
            for j in range(len(MatrixA.columns)):
                MultRes1 += MatrixA.iloc[i][j]*lumbda.iloc[j]
                MultRes2 += math.pow(lumbda.iloc[j]* MatrixD.iloc[i][j],2)
            if max(0,(-MatrixB.loc[i] + MultRes1 + ver*math.sqrt(MultRes2))) != 0:
                MultRes3 += math.pow((-MatrixB.iloc[i] + MultRes1 + ver * math.sqrt(MultRes2)), p)
        for i in range(len(X)):
            MultRes4 += MatrixC.iloc[i]*X[i]
        MultRes5=0
        for i in range(len(MatrixA.columns)):
            if max(0,-lumbda[i])!=0:
                MultRes5 += math.pow(-lumbda[i], p)
        MultALumbda = MultRes4 - r*(MultRes3+MultRes5)
        return MultALumbda

    def FunctionF2(self, MatrixA, lumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver):
        MultRes3 = 0
        MultRes4 = 0
        for i in range(len(MatrixA.columns)+len(MatrixA.index)):
            MatrixJ.iloc[i] = 1
        X = []
        X.append(lumbda.iloc[0]+lumbda.iloc[1])
        X.append(lumbda.iloc[2]+lumbda.iloc[3]+lumbda.iloc[4])
        X.append(lumbda.iloc[5]+lumbda.iloc[6])

        for i in range(len(MatrixA.index)):
            MultRes1 = 0
            MultRes2 = 0
            for j in range(len(MatrixA.columns)):
                MultRes1 += MatrixA.iloc[i][j]*lumbda.iloc[j]
                MultRes2 += math.pow(lumbda.iloc[j]* MatrixD.iloc[i][j],2)
            if max(0,(-MatrixB.iloc[i] + MultRes1 + ver*math.sqrt(MultRes2))) != 0:
                MultRes3 += math.pow((-MatrixB.iloc[i] + MultRes1 + ver * math.sqrt(MultRes2)), p)
        for i in range(len(X)):
            MultRes4 += MatrixC.iloc[i]*X[i]
        MultRes5=0
        for i in range(len(MatrixA.columns)):
            if max(0,-lumbda[i])!=0:
                MultRes5 += math.pow(lumbda[i], p)
        MultRes5 += math.pow(abs(X[1] - 2 * X[0]), p)
        MultRes5 += math.pow(abs(X[0] - X[2]), p)
        MultALumbda = MultRes4 - r*(MultRes3+MultRes5)
        return MultALumbda

    def GradientMethod1(self, MatrixA, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, X, ver):
        eps = 0.1
        l=0
        PrevLumbda = X.copy()
        CalcLumbda = PrevLumbda.copy()
        CurrF = self.FunctionF1(MatrixA, PrevLumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
        alfa = 100
        h=1
        PrevF = self.FunctionF1(MatrixA, PrevLumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
        AntiGrad = pd.Series(index=range(len(MatrixA.columns)))
        iter = 0

        while True:
            iter+=1
            for i in range(len(CalcLumbda.index)):
                PrevLumbda.iloc[i] = CalcLumbda.iloc[i]
            PrevF=CurrF
            for i in range(len(AntiGrad.index)):
                CurrLumbdaPlusH = pd.Series(index=PrevLumbda.index)
                CurrLumbdaMinusH = pd.Series(index=PrevLumbda.index)
                for q in range(len(CurrLumbdaPlusH.index)):
                    if q == i:
                        CurrLumbdaPlusH.iloc[q]=PrevLumbda.iloc[q]+h
                        CurrLumbdaMinusH.iloc[q]=PrevLumbda.iloc[q]-h
                    else:
                        CurrLumbdaPlusH.iloc[q]=PrevLumbda.iloc[q]
                        CurrLumbdaMinusH.iloc[q]=PrevLumbda.iloc[q]
                plus = self.FunctionF1(MatrixA, CurrLumbdaPlusH, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
                minus = self.FunctionF1(MatrixA, CurrLumbdaMinusH, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
                AntiGrad.iloc[i]=(plus-minus)/(2*h)

            while True:
                alfa = alfa / 2
                for k in range(len(CalcLumbda.index)):
                    CalcLumbda.iloc[k] = PrevLumbda.iloc[k] + alfa*AntiGrad.iloc[k]
                CurrF = self.FunctionF1(MatrixA, CalcLumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
                if CurrF >= PrevF:
                    break
            alfa = 100
            print((self.GetNorm(self.GetDelta(CalcLumbda, PrevLumbda))))
            CalcLumbda=CalcLumbda.apply(lambda x: round(x))
            print(CalcLumbda)
            if (self.GetNorm(self.GetDelta(CalcLumbda, PrevLumbda)) <= eps):
                break
        return CalcLumbda

    def GradientMethod2(self, MatrixA, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, X, ver):
        eps = 0.2
        PrevLumbda = X.copy()
        CalcLumbda = PrevLumbda.copy()
        CurrF = self.FunctionF2(MatrixA, PrevLumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
        alfa = 100
        h=1
        PrevF = self.FunctionF2(MatrixA, PrevLumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
        AntiGrad = pd.Series(index=range(len(MatrixA.columns)))
        iter = 0

        while True:
            iter+=1
            for i in range(len(CalcLumbda.index)):
                PrevLumbda.iloc[i] = CalcLumbda.iloc[i]
            PrevF=CurrF
            for i in range(len(AntiGrad.index)):
                CurrLumbdaPlusH = pd.Series(index=PrevLumbda.index)
                CurrLumbdaMinusH = pd.Series(index=PrevLumbda.index)
                for q in range(len(CurrLumbdaPlusH.index)):
                    if q == i:
                        CurrLumbdaPlusH.iloc[q]=PrevLumbda.iloc[q]+h
                        CurrLumbdaMinusH.iloc[q]=PrevLumbda.iloc[q]-h
                    else:
                        CurrLumbdaPlusH.iloc[q]=PrevLumbda.iloc[q]
                        CurrLumbdaMinusH.iloc[q]=PrevLumbda.iloc[q]
                plus = self.FunctionF2(MatrixA, CurrLumbdaPlusH, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
                minus = self.FunctionF2(MatrixA, CurrLumbdaMinusH, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
                AntiGrad.iloc[i]=(plus-minus)/(2*h)

            while True:
                alfa = alfa / 2
                for k in range(len(CalcLumbda.index)):
                    CalcLumbda.iloc[k] = PrevLumbda.iloc[k] + alfa*AntiGrad.iloc[k]
                CurrF = self.FunctionF2(MatrixA, CalcLumbda, MatrixB, MatrixC, MatrixD, MatrixJ, r, p, ver)
                if CurrF >= PrevF:
                    break
            alfa = 100
            print(self.GetNorm(self.GetDelta(CalcLumbda, PrevLumbda)))
            if (self.GetNorm(self.GetDelta(CalcLumbda, PrevLumbda)) <= eps):
                break
        return CalcLumbda


