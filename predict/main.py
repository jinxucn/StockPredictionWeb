import numpy as np
from lib.util import *
from lib.bayesian import *
from lib.svm import *
from lib.arima import *
from lib.lstm import *
from lib.indicator import *
import torch
import time as t
import os
import pandas as pd

# algorithm selection: 1 - Bayesian Curve Fitting;  2 - ARIMA;3 - SVM; 4 - LSTM;
stockSymbols = ['NVDA', 'AMD', 'BABA', 'KO', 'DIS',
                'AMZN', 'BILI', 'NTES', 'GOOG', 'INTC']
# stockSymbols=['NVDA']

df_indicator, df_bayesian, df_arima, df_svm, df_lstm = init_df()
stockIDs = {}
for i in range(len(stockSymbols)):
    stockIDs[stockSymbols[i]] = i+1


def long():
    print("-------------------Long Term-----------------------")
    time = t.time()
    # mse=[0 for i in range(10)]
    # cmat=np.zeros((2,2))

    for stockName in stockSymbols:
    # for i in range(10):
    #     stockName=stockSymbols[i]
        print(stockName)
        data_1d_raw = import_file(stockIDs[stockName], '1d')
        data_1d = timestamp2index(data_1d_raw)
        n = 30
        train_x, train_y, test_x, test_y = generate_dataset(data_1d, n)

        MACD_hist_30d = MACD(data_1d[1])
        # plt.plot(MACD_hist_30d)
        # plt.title("MACD HIST")
        # plt.show()

        tp = 16
        upper, middle, lower = Bollinger_Bands(data_1d[1], tp)
        # plt.plot(upper)
        # plt.plot(lower)
        # plt.plot(middle)
        # plt.plot(data_1d[1,-15:])
        # plt.title("BOLLINGER BAND")
        # plt.show()

        slowk, slowd = KDJ(
            data_1d[3, -27:], data_1d[2, -27:], data_1d[1, -27:])
        # plt.plot(slowk)
        # plt.plot(slowd)
        # plt.title("KDJ")
        # plt.show()
        for i in range(15):
            df_indicator.loc[df_indicator.shape[0] + 1] = {'OperationTime': time,
                                                           'StockID': stockName,
                                                           'TargetTime': data_1d_raw[0, -i - 1],
                                                           'MACD_hist': MACD_hist_30d[i],
                                                           'BBupper': upper[i],
                                                           'BBmiddle': middle[i],
                                                           'BBlower': lower[i],
                                                           'slowK': slowk[i],
                                                           'slowD': slowd[i]}

        print("Algorithm: LSTM-RNN")
        model_path = './models/model_' + stockName + '.pkl'
        if os.path.exists(model_path):
            lstm = torch.load(model_path)
        else:
            lstm = LSTM(input_size=n)
            loss_func = nn.MSELoss()
            optimizer = torch.optim.Adam(lstm.parameters(), lr=0.001)
            train_LSTM(lstm, optimizer, loss_func,
                       train_x, train_y, 1000, model_path)

        # eval_LSTM(lstm, test_x, test_y, n)
        # mse[i],cmat_temp=eval_LSTM(lstm,test_x,test_y,n)
        # cmat=np.add(cmat,cmat_temp)
        # print(cmat_temp)

        y_lstm = predict_LSTM(lstm, test_x, n)
        y_lstm = recover(data_1d[1], y_lstm)
        df_lstm.loc[df_lstm.shape[0] + 1] = {'OperationTime': time,
                                             'StockID': stockName,
                                             'Algorithm': 'LSTM',
                                             'TargetTime': data_1d_raw[0, -1]+3600*24,
                                             'value': y_lstm}
        print("Price after 1d:", y_lstm)

    save_df(df_indicator, 'indicator', 'replace')
    save_df(df_lstm, 'predict_long', 'replace')
    print("-----------------Result Uploaded---------------------")


def short():
    print("-------------------Short Term------------------------")
    time = int(t.time())

    # mse_bcf=[0 for i in range(10)]
    # mse_svr=[0 for i in range(10)]
    # cmat_bcf = np.zeros((2, 2))
    # cmat_svr = np.zeros((2, 2))


    # for i in range(10):
    #     stockName=stockSymbols[i]

    for stockName in stockSymbols:

        data_1m_raw = import_file(stockIDs[stockName], '1m')
        data_1m = timestamp2index(data_1m_raw)
        print(stockName)
        print("Algorithm: Bayesian Curve Fitting")
        bcf = BayesianCF(data_1m)

        # bcf.eval()
        # mse_bcf[i],cmat_temp=bcf.eval()
        # cmat_bcf=np.add(cmat_bcf,cmat_temp)
        # print(cmat_temp)

        # bcf.autoadjust()

        y_bayesian = bcf.predict(
            bcf.x[-300:], bcf.y[-300 - 1:], bcf.x[-1] + 5)
        df_bayesian.loc[df_bayesian.shape[0] + 1] = {'OperationTime': time,
                                                     'StockID': stockName,
                                                     'Algorithm': 'Bayesian',
                                                     'TargetTime': data_1m_raw[0, -1]+300,
                                                     'value': y_bayesian}
        print("Price after 1m:", y_bayesian)

        # SVM
        print("Algorithm: Support Vector Regression")
        svr = SVR(data_1m)

        # svr.eval()
        # mse_svr[i],cmat_temp=svr.eval()
        # cmat_svr=np.add(cmat_svr,cmat_temp)
        # print(cmat_temp)

        y_svr = svr.predict()
        df_svm.loc[df_svm.shape[0] + 1] = {'OperationTime': time,
                                           'StockID': stockName,
                                           'Algorithm': 'SVM',
                                           'TargetTime': data_1m_raw[0, -1]+300,
                                           'value': y_svr}
        print("Price after 1m:", y_svr)

    # print(mse_bcf)
    # print(mse_svr)
    # print(cmat_bcf)
    # print(cmat_svr)

    save_df(df_bayesian, 'predict_short', 'replace')
    save_df(df_svm, 'predict_short', 'append')
    print("-----------------Result Uploaded---------------------")

def main():
    # long()
    # short()

    count = 1441
    while count:
        if count == 1441:
            long()
            count = 1
        else:
            short()
            t.sleep(60)
            count+=1

if __name__ == "__main__":
    main()

# df_indicator, df_bayesian, df_arima, df_svm, df_lstm = load_df()
# # engine = sqlalchemy.create_engine('mysql+pymysql://stockpredictor:buyer@jindb.c8ojtshzefs1.us-east-2.rds.amazonaws.com:3306/stocks')
# # df_indicator.to_sql(indicator,)

# for stockName in stockSymbols:
#     print("--------------------", stockName, "--------------------")
#     csv_file_path_1h = '../spiders/data/1h/' + stockName + '.csv'
#     data_1m_raw = import_file(stockIDs[stockName], '1m')
#     data_1m = timestamp2index(data_1m_raw)

#     csv_file_path_1d = '../spiders/data/1d/' + stockName + '.csv'
#     data_1d_raw = import_file(stockIDs[stockName], '1d')
#     data_1d = timestamp2index(data_1d_raw)
#     n = 30
#     train_x, train_y, test_x, test_y = generate_dataset(data_1d, n)

#     MACD_hist_30d = MACD(data_1d[1])
#     tp = 16
#     upper, middle, lower = Bollinger_Bands(data_1d[1], tp)
#     slowk, slowd = KDJ(data_1d[3, -27:], data_1d[2, -27:], data_1d[1, -27:])
#     for i in range(15):
#         df_indicator.loc[df_indicator.shape[0] + 1] = {'OperationTime': time,
#                                                        'StockID': stockName,
#                                                        'TargetTime': data_1d_raw[0, -i - 1],
#                                                        'MACD_hist': MACD_hist_30d[i],
#                                                        'BBupper': upper[i],
#                                                        'BBmiddle': middle[i],
#                                                        'BBlower': lower[i],
#                                                        'slowK': slowk[i],
#                                                        'slowD': slowd[i]}

#     # Bayesian
#     print("Algorithm: Bayesian Curve Fitting")
#     bcf = BayesianCF(data_1m)
#     # bcf.autoadjust()
#     y_bayesian = bcf.predict(
#         bcf.x[-24 * 7 - 1:-1], bcf.y[-24 * 7 - 1:-1], bcf.x[-1] + 5)
#     df_bayesian.loc[df_bayesian.shape[0] + 1] = {'OperationTime': time,
#                                                  'StockID': stockName,
#                                                  'Algorithm': 'Bayesian',
#                                                  'TargetTime': data_1m_raw[0, -i]+3600,
#                                                  'value': y_bayesian}
#     print("Price after 1h:", y_bayesian)

#     # SVM
#     print("Algorithm: Support Vector Regression")
#     svr = SVR(data_1m)
#     y_svr = svr.predict()
#     df_svm.loc[df_svm.shape[0] + 1] = {'OperationTime': time,
#                                        'StockID': stockName,
#                                        'Algorithm': 'SVM',
#                                        'TargetTime': data_1m_raw[0, -i]+3600,
#                                        'value': y_svr}
#     print("Price after 1h:", y_svr)

#     # ARIMA
#     # print("Algorithm: ARIMA")
#     # arima = ARIMA(data_1h)
#     # y_arima = arima.predict()
#     # df_arima.loc[df_arima.shape[0] + 1] = {'OperationTime': time,
#     #                                                  'StockID': stockID,
#     #                                                  'Algorithm': 'ARIMA',
#     #                                                  'TargetTime': data_1h_raw[0, -i]+3600,
#     #                                                  'value': y_arima}
#     # print("Price after 1h:", y_arima)

#     # LSTM
#     print("Algorithm: LSTM-RNN")
#     model_path = './models/model_' + stockName + '.pkl'
#     if os.path.exists(model_path):
#         lstm = torch.load(model_path)
#     else:
#         lstm = LSTM(input_size=n)
#         loss_func = nn.MSELoss()
#         optimizer = torch.optim.Adam(lstm.parameters(), lr=0.001)
#         train_LSTM(lstm, optimizer, loss_func,
#                    train_x, train_y, 1000, model_path)
#         # eval_LSTM(lstm,test_x,test_y,n)
#     y_lstm = predict_LSTM(lstm, test_x, 30)
#     y_lstm = recover(data_1d[1], y_lstm)
#     df_lstm.loc[df_lstm.shape[0] + 1] = {'OperationTime': time,
#                                          'StockID': stockName,
#                                          'Algorithm': 'LSTM',
#                                          'TargetTime': data_1d_raw[0, -i]+3600*24,
#                                          'value': y_lstm}
#     print("Price after 1d:", y_lstm)


# save_df(df_indicator, df_bayesian, df_arima, df_svm, df_lstm)

