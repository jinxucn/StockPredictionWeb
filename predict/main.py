import numpy as np
from lib.util import *
from lib.bayesian import *
from lib.svm import *
from lib.arima import *
from lib.lstm import *
from lib.indicator import *
import torch
import time
import os
import pandas as pd
import sqlalchemy

time = int(time.time())
print("Operation Timestamp:", time)

# algorithm selection: 1 - Bayesian Curve Fitting;  2 - ARIMA;3 - SVM; 4 - LSTM;
stockSymbols = ['NVDA', 'AMD', 'BABA', 'KO', 'DIS',
                'AMZN', 'BILI', 'NTES', 'GOOG', 'INTC']

df_indicator,df_bayesian,df_arima,df_svm,df_lstm=load_df()
# engine = sqlalchemy.create_engine('mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks')
# df_indicator.to_sql(indicator,)

for stockID in stockSymbols:
    print("--------------------",stockID,"--------------------")
    csv_file_path_1h = '../spiders/data/1h/' + stockID + '.csv'
    data_1h_raw = import_file(csv_file_path_1h)
    data_1h = timestamp2index(data_1h_raw)

    csv_file_path_1d = '../spiders/data/1d/' + stockID + '.csv'
    data_1d_raw = import_file(csv_file_path_1d)
    data_1d = timestamp2index(data_1d_raw)
    n = 30
    train_x, train_y, test_x, test_y = generate_dataset(data_1d, n)

    MACD_hist_30d = MACD(data_1d[1])
    tp = 16
    upper, middle, lower = Bollinger_Bands(data_1d[1], tp)
    slowk, slowd = KDJ(data_1d[3, -27:], data_1d[2, -27:], data_1d[1, -27:])
    for i in range(15):
        df_indicator.loc[df_indicator.shape[0] + 1] = {'OperationTime': time,
                                                       'StockID': stockID,
                                                       'TargetTime': data_1d_raw[0, -i - 1],
                                                       'MACD_hist': MACD_hist_30d[i],
                                                       'BBupper': upper[i],
                                                       'BBmiddle': middle[i],
                                                       'BBlower': lower[i],
                                                       'slowK': slowk[i],
                                                       'slowD': slowd[i]}

    # Bayesian
    print("Algorithm: Bayesian Curve Fitting")
    bcf = BayesianCF(data_1h)
    # bcf.autoadjust()
    y_bayesian = bcf.predict(bcf.x[-24 * 7 - 1:-1], bcf.y[-24 * 7 - 1:-1], bcf.x[-1] + 60)
    df_bayesian.loc[df_bayesian.shape[0] + 1] = {'OperationTime': time,
                                                     'StockID': stockID,
                                                     'Algorithm': 'Bayesian',
                                                     'TargetTime': data_1h_raw[0, -i]+3600,
                                                     'value': y_bayesian}
    print("Price after 1h:", y_bayesian)

    # SVM
    print("Algorithm: Support Vector Regression")
    svr = SVR(data_1h)
    y_svr = svr.predict()
    df_svm.loc[df_svm.shape[0] + 1] = {'OperationTime': time,
                                                     'StockID': stockID,
                                                     'Algorithm': 'SVM',
                                                     'TargetTime': data_1h_raw[0, -i]+3600,
                                                     'value': y_svr}
    print("Price after 1h:", y_svr)

    # ARIMA
    print("Algorithm: ARIMA")
    arima = ARIMA(data_1h)
    y_arima = arima.predict()
    df_arima.loc[df_arima.shape[0] + 1] = {'OperationTime': time,
                                                     'StockID': stockID,
                                                     'Algorithm': 'ARIMA',
                                                     'TargetTime': data_1h_raw[0, -i]+3600,
                                                     'value': y_arima}
    print("Price after 1h:", y_arima)

    # LSTM
    print("Algorithm: LSTM-RNN")
    model_path = './models/model_' + stockID + '.pkl'
    if os.path.exists(model_path):
        lstm = torch.load(model_path)
    else:
        lstm = LSTM(input_size=n)
        loss_func = nn.MSELoss()
        optimizer = torch.optim.Adam(lstm.parameters(), lr=0.001)
        train_LSTM(lstm, optimizer, loss_func, train_x, train_y, 1000,model_path)
        # eval_LSTM(lstm,test_x,test_y,n)
    y_lstm = predict_LSTM(lstm, test_x, 30)
    y_lstm = recover(data_1d[1], y_lstm)
    df_lstm.loc[df_lstm.shape[0] + 1] = {'OperationTime': time,
                                                     'StockID': stockID,
                                                     'Algorithm': 'LSTM',
                                                     'TargetTime': data_1d_raw[0, -i]+3600*24,
                                                     'value': y_lstm}
    print("Price after 1d:", y_lstm)

save_df(df_indicator,df_bayesian,df_arima,df_svm,df_lstm)