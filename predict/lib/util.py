import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os


def import_file(stock_id, type):
    db = 'mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks'
    engine = create_engine(db)
    if type == '1d':
        sql = 'select day,close,low,high from history_day where close is not null and low is not null and high is not null and stock_id=' + \
            str(stock_id)
    elif type == '1m':
        sql = 'select minute,close,low,high from real_time where close is not null and low is not null and high is not null and stock_id=' + \
            str(stock_id)
    df = pd.read_sql_query(sql, engine)
    df.dropna()
    print(df.head(5))
    data_np = df.to_numpy().transpose()
    # data_np[data_np == None] = "0"
    return data_np.astype(float)


def init_df():
    df_indicator = pd.DataFrame(
            columns={'OperationTime', 'StockID', 'TargetTime', 'MACD_hist', 'BBupper', 'BBmiddle', 'BBlower', 'slowK',
                     'slowD'})

    df_bayesian = pd.DataFrame(
            columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})


    df_arima = pd.DataFrame(
        columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})


    df_svm = pd.DataFrame(
        columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})

    df_lstm=pd.DataFrame(
            columns={'OperationTime', 'StockID', 'Algorithm', 'TargetTime', 'value'})
    return df_indicator, df_bayesian, df_arima, df_svm, df_lstm


def save_df(df, dbname, exists):
    db = 'mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks'
    engine = create_engine(db)
    pd.io.sql.to_sql(df, dbname, con=engine,
                     index=False, if_exists=exists)

    # df_indicator.to_csv('./result/indicator.csv', index=False)
    # df_bayesian.to_csv('./result/bayesian.csv')
    # df_arima.to_csv('./result/arima.csv')
    # df_svm .to_csv('./result/svm.csv')
    # df_lstm.to_csv('./result/lstm.csv')
    # print("Result saved.")

def timestamp2index(data):
    h, w = data.shape
    data_temp = np.zeros((h, w))
    data_temp[0] = (data[0]-data[0, 0])/60
    data_temp[1:] = data[1:]
    return data_temp


def normalize(data):
    h, w = data.shape
    data_norm = np.zeros((h, w))
    for i in range(len(data)):
        max = np.max(data[i])
        min = np.min(data[i])
        data_norm[i] = np.subtract(data[i], min)/(max-min)
    return data_norm


def recover(data, y):
    max = np.max(data)
    min = np.min(data)
    y_recover = y*(max-min)+min
    return y_recover


def generate_dataset(data, n=30):
    price = normalize(data)[1]
    x = []
    y = []
    for i in range(len(price)-n):
        x.append(price[i:i+n])
        y.append(price[i+n])
        train_size = int(len(x)*0.7)
        train_x = np.array(x[:train_size], dtype=np.float32).reshape(-1, 1, n)
        train_y = np.array(y[:train_size], dtype=np.float32).reshape(-1, 1, 1)
        test_x = np.array(x[train_size:], dtype=np.float32).reshape(-1, 1, n)
        test_y = np.array(y[train_size:], dtype=np.float32).reshape(-1, 1, 1)
    return train_x, train_y, test_x, test_y


def phi(x, M):
    phiX = np.zeros(M+1)
    for i in range(M+1):
        phiX[i] = x**i
    return phiX.reshape((M+1, 1))

def confusion_matrix(y_pred,y):
    mat=np.zeros((2,2))
    dy=[y[i+1]<y[i] for i in range(len(y)-1)]
    dy_pred=[y_pred[i+1]<y[i] for i in range(len(y_pred)-1)]
    dy=[int(x) for x in dy]
    dy_pred=[int(x) for x in dy_pred]
    for i in range(len(dy)):
        mat[dy[i],dy_pred[i]]+=1
    return mat