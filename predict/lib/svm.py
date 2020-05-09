import numpy as np
import matplotlib.pyplot as plt
from util import *
from sklearn.metrics import mean_squared_error
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from scipy import signal

# csv_file_path = '../BILI.csv'
# data = import_file(csv_file_path)
# data = timestamp2index(data)

class SVR():
    def __init__(self,data):
        self.M=7
        self.x=data[0]
        self.y=data[1]
        self.N =24*7
        # b, a = signal.butter(8, 0.1, 'lowpass')
        # self.y_filtered = signal.filtfilt(b, a, self.y)  # data为要过滤的信号

    # def autoadjust(self):
    #     mse=[0 for i in range(20)]
    #     for i in range(10):
    #         y_fit=np.zeros(len(self.x)-24*7)
    #         for t in range(len(self.x)-24*7):
    #             w = np.polyfit(self.x[t:t+24*7],self.y[t:t+24*7],i)
    #             y_fit[t] = np.polyval(w,self.x[t+24*7])
    #         # plt.plot(self.x[24*7:],self.y[24*7:])
    #         # plt.plot(self.x[24*7:],y_fit)
    #         # plt.show()
    #         mse[i]=mean_squared_error(y_fit,self.y[24*7:])
    #         # self.w = np.polyfit(self.x, self.y, i)
    #         # fit = np.polyval(self.w, self.x)
    #     self.M=np.argmin(mse)
    #     # print(mse)
    #     print("Auto adjustment: Degree = ",self.M)
    # # def pred(self):

    def predict(self):
        # svr = GridSearchCV(svm.SVR(), param_grid={"kernel": ("linear", 'rbf'), "C": np.logspace(-3, 3, 7),
        #                                       "gamma": np.logspace(-3, 3, 7)})
        svr=svm.SVR()
        svr.fit(self.x[-24*7-1:-1].reshape(-1, 1),self.y[-24*7-1:-1])
        return svr.predict(np.array([self.x[-1]+60]).reshape(1,-1))[0]