import numpy as np
from util import *
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

class BayesianCF():
    def __init__(self,data):
        self.M=19
        self.x=data[0]
        self.y=data[1]
        self.alpha = 0.01
        self.beta = 10
        self.N = 24*7
        # b, a = signal.butter(8, 0.1, 'lowpass')
        # self.y_filtered = signal.filtfilt(b, a, self.y)

    def predict(self,trainX,trainT,X_pred):
        # Determine S
        Ssum = np.zeros((self.M+1,self.M+1))
        for i in range(self.N):
            Ssum = np.add(Ssum,phi(trainX[i],self.M).dot(phi(X_pred,self.M).transpose()))
        Sinv = self.alpha*np.identity(self.M+1)+self.beta*Ssum
        S=np.linalg.pinv(Sinv)

        # Determine variance
        var=1/self.beta+phi(X_pred,self.M)*phi(X_pred,self.M).transpose()

        # Determine mean
        Msum = np.zeros((self.M+1,1))
        for i in range(self.N):
            Msum = np.add(Msum,phi(trainX[i],self.M)*trainT[i])
        mean=self.beta*phi(X_pred,self.M).transpose().dot(S.dot(Msum))
        return mean[0,0]

    def eval(self):
        y_fit = np.zeros(len(self.x) - 24 * 7)
        for t in range(len(self.x) - 24 * 7):
            y_fit[t] = self.predict(self.x[t:t + 24 * 7], self.y[t:t + 24 * 7], self.x[t + 24 * 7])
        plt.plot(self.x[24*7:],self.y[24*7:])
        plt.plot(self.x[24*7:],y_fit)
        plt.show()
        mse = mean_squared_error(y_fit, self.y[24 * 7:])
        cmat=confusion_matrix(y_fit,self.y[24*7:])
        return mse,cmat

    def autoadjust(self):
        mse = [0 for i in range(20)]
        for self.M in range(20):
            y_fit = np.zeros(len(self.x) - 24 * 7)
            for t in range(len(self.x) - 24 * 7):
                y_fit[t] = self.predict(self.x[t:t+24*7],self.y[t:t+24*7],self.x[t+24*7-1]+60)
            # plt.plot(self.x[24*7:],self.y[24*7:])
            # plt.plot(self.x[24*7:],y_fit)
            # plt.show()
            mse[self.M] = mean_squared_error(y_fit, self.y[24 * 7:])
            print("MSE for M=",self.M,": ", mse[self.M])
            # self.w = np.polyfit(self.x, self.y, i)
            # fit = np.polyval(self.w, self.x)
        self.M = np.argmin(mse)
        # print(mse)
        print("Auto adjustment: Degree = ", self.M)