import pandas as pd
import matplotlib.pyplot as plt
import datetime
import torch
import torch.nn as nn
import numpy as np
from util import *
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader

class LSTM(nn.Module):
    def __init__(self,input_size,hidden_size=8,output_size=1,num_layers=2):
        super().__init__()
        self.lstm=nn.LSTM(input_size,hidden_size,num_layers)
        self.fc=nn.Linear(hidden_size,output_size)

    def forward(self,_x):
        x, _ = self.lstm(_x)
        s, b, h = x.shape
        x = x.view(s*b, h)
        x = self.fc(x)
        x = x.view(s, b, -1)
        return x


def train_LSTM(model,optimizer,loss_func,train_x,train_y,iter,PATH):
    print("Saved Model Not Found. Training LSTM......")
    train_x = torch.from_numpy(train_x)
    train_y = torch.from_numpy(train_y)
    for _ in range(iter):
        out=model(train_x)
        loss=loss_func(out,train_y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        if(_+1)%100==0 or _==0:
            print('Epoch',_+1,"Loss:",loss.item())
    torch.save(model,PATH)



def eval_LSTM(model,test_x,test_y,n):
    model.eval()
    y_real=test_y[n:].reshape(-1)
    test_x_tensor=torch.from_numpy(test_x[n:])
    test_y_tensor=torch.from_numpy(test_y[n:])
    y_pred=model(test_x_tensor)
    y_pred=y_pred.view(-1).data.numpy()
    plt.plot(y_real)
    plt.plot(y_pred)
    plt.show()

def predict_LSTM(model,data,n):
    x=data[-1].reshape(1,1,-1)
    # print(x.shape)
    x=torch.from_numpy(x)
    y_pred=model(x).data.numpy().reshape(-1)
    return y_pred[0]