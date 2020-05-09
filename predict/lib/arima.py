import numpy as np
import pmdarima as pm
from util import *
from sklearn.metrics import mean_squared_error

# csv_file_path = '../BILI.csv'
# data = import_file(csv_file_path)
# data = timestamp2index(data)

class ARIMA():
    def __init__(self,data):
        self.M=3
        self.x=data[0]
        self.y=data[1]
        self.N =24*7
        self.model = pm.auto_arima(self.y, seasonal=True, m=12)

    def predict(self):
        pred = self.model.predict(n_periods=1)
        return pred[0]

# BCF=BayesianCF(data)
# BCF.autoadjust()
# y_pred=BCF.predict()
# print(y_pred)
# for t in range(10):
#     start = t*100  # Change this value to set start point. Training set will be 100 data points starts from this index
#     end = start + N
#
#     trainX=data[0,start:end]
#     trainT=data[1,start:end]
#
#     latest_close=trainT[-1]
#
#     testX=data[0,end]
#     testT=float(data[1,end])
#
#     # Determine S
#     Ssum = np.zeros((M+1,M+1))
#     for i in range(N):
#         Ssum = np.add(Ssum,phi(trainX[i]).dot(phi(testX).transpose()))
#     Sinv = alpha*np.identity(M+1)+beta*Ssum
#     S=np.linalg.inv(Sinv)
#
#     # Determine variance
#     var=1/beta+phi(testX)*phi(testX).transpose()
#
#     # Determine mean
#     Msum = np.zeros((M+1,1))
#     for i in range(N):
#         Msum = np.add(Msum,phi(trainX[i])*trainT[i])
#     mean=beta*phi(testX).transpose().dot(S.dot(Msum))
#
#     if t==9:
#         w = np.polyfit(trainX, trainT, M)
#         print("w=", w)
#
#     if testT>latest_close:
#         if mean>latest_close:
#             TP+=1
#         else:
#             FN+=1
#     else:
#         if mean<latest_close:
#             TN+=1
#         else:
#             FP+=1
#
#     l2loss+=(testT-mean)**2
#
# confusion_matrix = np.array([[TP, FP], [TN, FN]])
# precision = TP / (TP + FP)
# recall = TP / (TP + FN)
# print("confusion matrix: \n", confusion_matrix)
# print("precision=", precision)
# print("recall:", recall)
# print("l2loss:", l2loss)