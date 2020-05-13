import numpy as np
import pmdarima as pm
from util import *
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# csv_file_path = '../BILI.csv'
# data = import_file(csv_file_path)
# data = timestamp2index(data)

class ARIMA():
    def __init__(self,data):
        self.M=3
        self.x=data[0]
        self.y=data[1]
        self.N =24*7

    def eval(self):
        y_pred = np.zeros(len(self.x) - 24 * 7)
        for t in range(len(self.x) - 24 * 7):
            model = pm.auto_arima(self.y[:t + 24 * 7], seasonal=True, m=12)
            y_pred[t]=model.predict(n_periods=1)
        plt.plot(y_pred)
        plt.plot(self.y[24 * 7:])
        plt.show()
        mse = mean_squared_error(y_pred, self.y[24 * 7:])
        cmat = confusion_matrix(y_pred, self.y[24 * 7:])
        return mse,cmat

    def predict(self):
        self.model = pm.auto_arima(self.y, seasonal=True, m=12)
        pred = self.model.predict(n_periods=1)
        return pred[0]
