import pandas as pd
import numpy as np
from scipy.special import gamma
from scipy.optimize import minimize, LinearConstraint


def prepare_data(path):
    df = pd.read_csv(path)
    df.columns = ['Date_vix']
    df['Date'] = df['Date_vix'].apply(lambda x: x[0:8])
    df['vix'] = df['Date_vix'].apply(lambda x: x[9:])
    df['vix'] = df['vix'].apply(lambda x: str.replace(x, ' ', ''))
    df['vix'] = df['vix'].apply(lambda x: 0.0 if x == '.' else x)
    df['vix'] = df['vix'].astype(float)
    df['log_vix'] = np.log(df['vix'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def obtain_train(df, n, date):
    df_ori = df[df['Date'] >= date][0:n].reset_index(drop=True)
    value_first = df_ori['log_vix'].values[0]
    df_ori['log_vix'] = df_ori['log_vix'] - value_first
    df_ori['lr'] = 2 * np.linspace(0, 1, 500) * df_ori['log_vix'].mean()
    df_ori['x'] = df_ori['log_vix'] - df_ori['lr']
    df_ori['y'] = df_ori['x'].diff()
    return df_ori


def obtain_gamma(value):
    value_ = np.power(gamma((value + 1) / 2), 2) / gamma(value + 0.5)
    return value_ / np.sqrt(np.pi)


def obtain_lambda(target):
    left = 0
    right = 3
    mid = (left + right) / 2
    while abs(obtain_gamma(mid) - target) > 10 ** -8:
        if obtain_gamma(mid) > target:
            left = mid
            mid = (left + right) / 2
        elif obtain_gamma(mid) < target:
            right = mid
            mid = (left + right) / 2
        else:
            return mid
    return mid

def objective_function(x, a,b):
    err = []
    for i in range(len(a)-1):
        err.append(np.power(a[i+1]-x[0]*a[i]-x[1]*b[i+1]-x[2],2))
#     print(err)
    return np.sum(err) #np.sqrt(np.sum(err))
