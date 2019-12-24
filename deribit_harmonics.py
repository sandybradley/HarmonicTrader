from deribit import *
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from harmonic_functions import *
import threading
from apscheduler.schedulers.blocking import BlockingScheduler

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

interval = 3600 # interval time in seconds
err_allowed = 7.0/100

# data = pd.read_csv('candleminutely.csv') # 15 mins
data = pd.read_csv('c:/q/w32/rl/experiment/trade/candlehourly.csv') # 4 hr
# data = pd.read_csv('candledaily.csv')
# data = pd.read_csv('candleweekly.csv')

data.time = pd.to_datetime(data.time,format='%Y-%m-%dD%H:%M:%S.%f')
data.index = data['time']
# data = data.drop_duplicates(keep=False)

prices = data.close.copy()

print(prices)

getaccSum()

trade_dates=[]
correct_pats=0
pats=0
sign=0

i = len(prices) - 1

current_idx,current_pat,start,end = peak_detect(prices.values[:i],order=7)

XA = current_pat[1] - current_pat[0]
AB = current_pat[2] - current_pat[1]
BC = current_pat[3] - current_pat[2]
CD = current_pat[4] - current_pat[3]

moves = [ XA , AB , BC , CD ]

# gart = is_gartley(moves,err_allowed)
# butt = is_butterfly(moves,err_allowed)
# bat = is_bat(moves,err_allowed)
# crab = is_crab(moves,err_allowed)
shark = is_shark(moves,err_allowed)
trio = is_trio(moves,err_allowed)

harmonics = np.array([shark,trio])
labels = ['Shark','Trio']
# harmonics = np.array([shark])
# labels = ['Shark']

start = np.array(current_idx).min()
end = np.array(current_idx).max()
price = prices.values[end]

if delta == 0.0:
    if np.any(harmonics == 1) or np.any(harmonics == -1):
        for j in range (0,len(harmonics)):
            if harmonics[j] == 1 or harmonics[j]==-1:
                sense = 'Bearish ' if harmonics[j]==-1 else 'Bullish '
                label = sense + labels[j] 
                print(label)

                sign = harmonics[j]
                
                date = data.iloc[end].name
                trade_dates = np.append(trade_dates,date)                

                if harmonics[j]==-1:
                    sell_limit(price)
                else:
                    buy_limit(price)
else:
    if delta < 0.0:
        sign = -1
    else:
        sign = 1

    walk(price,sign)

def walk(price,sign,stop=150.0):
    global stops
    if sign == 1:
        initial_stop_loss = price - stop
        stop_loss = initial_stop_loss
        if len(stops) == 0:
            sell_stop(stop_loss)
        else:
            initial_stop_loss = stops[0]
            stop_loss = initial_stop_loss
 
        if ( price - stop ) > initial_stop_loss:
            stop_loss = price - stop
            edit_stop(stop_loss)
            stops[0] = stop_loss
      
    elif sign == -1:
        initial_stop_loss = price + stop
        stop_loss = initial_stop_loss
        if len(stops) == 0:
            buy_stop(stop_loss)
        else:
            initial_stop_loss = stops[0]
            stop_loss = initial_stop_loss
    
        if ( price + stop ) < initial_stop_loss:
            stop_loss = price + stop
            edit_stop(stop_loss)
            stops[0] = stop_loss

def getData():
    global data,prices
    # data = pd.read_csv('candleminutely.csv') # 15 mins
    data = pd.read_csv('c:/q/w32/rl/experiment/trade/candlehourly.csv') # 4 hr
    # data = pd.read_csv('candledaily.csv')
    # data = pd.read_csv('candleweekly.csv')

    data.time = pd.to_datetime(data.time,format='%Y-%m-%dD%H:%M:%S.%f')
    data.index = data['time']
    # data = data.drop_duplicates(keep=False)

    prices = data.close.copy()
    print(prices)

def checkHarmonic():
    global i, current_idx,current_pat,start,end, sign, price,prices
    i = len(prices) - 1

    current_idx,current_pat,start,end = peak_detect(prices.values[:i],order=7)

    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    moves = [ XA , AB , BC , CD ]

    # gart = is_gartley(moves,err_allowed)
    # butt = is_butterfly(moves,err_allowed)
    # bat = is_bat(moves,err_allowed)
    # crab = is_crab(moves,err_allowed)
    shark = is_shark(moves,err_allowed)
    trio = is_trio(moves,err_allowed)

    harmonics = np.array([shark,trio])
    labels = ['Shark','Trio']
    # harmonics = np.array([shark])
    # labels = ['Shark']

    start = np.array(current_idx).min()
    end = np.array(current_idx).max()
    price = prices.values[end]

    if delta == 0.0:
        if np.any(harmonics == 1) or np.any(harmonics == -1):
            for j in range (0,len(harmonics)):
                if harmonics[j] == 1 or harmonics[j]==-1:
                    sense = 'Bearish ' if harmonics[j]==-1 else 'Bullish '
                    label = sense + labels[j] 
                    print(label)

                    sign = harmonics[j]
                    
                    date = data.iloc[end].name
                    trade_dates = np.append(trade_dates,date)                

                    if harmonics[j]==-1:
                        sell_limit(price)
                    else:
                        buy_limit(price)
    else:
        if delta < 0.0:
            sign = -1
        else:
            sign = 1

        walk(price,sign)


def iterarte():
    getAccess()
    getaccSum()
    getData()
    checkHarmonic()

# set_interval(iterarte,3600)
scheduler = BlockingScheduler()
scheduler.add_job(iterarte, 'interval', hours=4)
scheduler.start()

