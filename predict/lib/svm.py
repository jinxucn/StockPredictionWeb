import numpy as np
import matplotlib.pyplot as plt
from util import *
from sklearn.metrics import mean_squared_error
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from scipy import signal


class SVR():
    def __init__(self,data):
        self.M=7
        self.x=data[0]
        self.y=data[1]
        self.N =24*7
        # b, a = signal.butter(8, 0.1, 'lowpass')
        # self.y_filtered = signal.filtfilt(b, a, self.y)  # data为要过滤的信号


    def eval(self):
        y_pred = np.zeros(len(self.x) - 24 * 7)
        svr=svm.SVR()
        for t in range(len(self.x) - 24 * 7):
            svr.fit(self.x[t:t + 24 * 7].reshape(-1,1), self.y[t:t + 24 * 7])
            y_pred[t] = svr.predict(self.x[t + 24 * 7].reshape(1,-1))[0]
        plt.plot(y_pred)
        plt.plot(self.y[24*7:])
        plt.show()
        mse = mean_squared_error(y_pred, self.y[24 * 7:])
        cmat = confusion_matrix(y_pred, self.y[24 * 7:])
        return mse, cmat

    def predict(self):
        # svr = GridSearchCV(svm.SVR(), param_grid={"kernel": ("linear", 'rbf'), "C": np.logspace(-3, 3, 7),
        #                                       "gamma": np.logspace(-3, 3, 7)})
        svr=svm.SVR()
        svr.fit(self.x[-168:-1].reshape(-1, 1),self.y[-168:-1])
        return svr.predict(np.array([self.x[-1]+5]).reshape(1,-1))[0]