import numpy as np
import pandas as pd
import os


def import_file(path):
    df = pd.read_csv(path)
    df = df.iloc[:, [0, 2,4,5]]
    data_np = df.to_numpy().transpose()
    data_np[data_np == " None"] = "0"
    return data_np.astype(float)

def load_df():
    if os.path.exists('./result/indicator.csv'):
        df_indicator = pd.read_csv('./result/indicator.csv')
    else:
        df_indicator = pd.DataFrame(
            columns={'OperationTime', 'StockID', 'TargetTime', 'MACD_hist', 'BBupper', 'BBmiddle', 'BBlower', 'slowK',
                     'slowD'})
    if os.path.exists('./result/bayesian.csv'):
        df_bayesian = pd.read_csv('./result/bayesian.csv')
    else:
        df_bayesian = pd.DataFrame(columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})

    if os.path.exists('./result/arima.csv'):
        df_arima = pd.read_csv('./result/arima.csv')
    else:
        df_arima = pd.DataFrame(columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})

    if os.path.exists('./result/svm.csv'):
        df_svm = pd.read_csv('./result/svm.csv')
    else:
        df_svm = pd.DataFrame(columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})

    if os.path.exists('./result/lstm.csv'):
        df_lstm = pd.read_csv('./result/lstm.csv')
    else:
        df_lstm = pd.DataFrame(columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})
    return df_indicator,df_bayesian,df_arima,df_svm,df_lstm

def save_df(df_indicator,df_bayesian,df_arima,df_svm,df_lstm):
    df_indicator.to_csv('./result/indicator.csv',index=False)
    df_bayesian.to_csv('./result/bayesian.csv')
    df_arima.to_csv('./result/arima.csv')
    df_svm .to_csv('./result/svm.csv')
    df_lstm.to_csv('./result/lstm.csv')
    print("Result saved.")

def timestamp2index(data):
    h,w=data.shape
    data_temp=np.zeros((h,w))
    data_temp[0] = (data[0]-data[0,0])/60
    data_temp[1:]=data[1:]
    return data_temp


# def index2timestamp(data):
#     data_temp=data
#     data_temp[0] = data[0]*60+data[0,0]
#     return data_temp


def normalize(data):
    h,w=data.shape
    data_norm=np.zeros((h,w))
    for i in range(len(data)):
        max=np.max(data[i])
        min=np.min(data[i])
        data_norm[i]=np.subtract(data[i],min)/(max-min)
    return data_norm

def recover(data,y):
    max=np.max(data)
    min=np.min(data)
    y_recover=y*(max-min)+min
    return y_recover

def generate_dataset(data,n=30):
    price=normalize(data)[1]
    x=[]
    y=[]
    for i in range(len(price)-n):
        x.append(price[i:i+n])
        y.append(price[i+n])
        train_size=int(len(x)*0.7)
        train_x=np.array(x[:train_size],dtype=np.float32).reshape(-1,1,n)
        train_y=np.array(y[:train_size],dtype=np.float32).reshape(-1,1,1)
        test_x=np.array(x[train_size:],dtype=np.float32).reshape(-1,1,n)
        test_y=np.array(y[train_size:],dtype=np.float32).reshape(-1,1,1)
    return train_x,train_y,test_x,test_y


def phi(x,M):
    phiX=np.zeros(M+1)
    for i in range(M+1):
        phiX[i]=x**i
    return phiX.reshape((M+1,1))