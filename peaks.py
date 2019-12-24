import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from harmonic_functions import *

# data = pd.read_csv('candleminutely.csv')
data = pd.read_csv('candlehourly.csv')
# data = pd.read_csv('candledaily.csv')
# data = pd.read_csv('candleweekly.csv')

data.time = pd.to_datetime(data.time,format='%Y-%m-%dD%H:%M:%S.%f')
data.index = data['time']
data = data.drop_duplicates(keep=False)

price = data.close.copy()

err_allowed = 7.0/100

pnl = []
trade_dates=[]
correct_pats=0
pats=0

plt.ion()

for i in range (100,len(price)):
        
    current_idx,current_pat,start,end = peak_detect(price.values[:i],order=7)

    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    moves = [XA,AB,BC,CD]

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

    if np.any(harmonics == 1) or np.any(harmonics == -1):
        for j in range (0,len(harmonics)):
            if harmonics[j] == 1 or harmonics[j]==-1:
                pats+=1
                sense = 'Bearish ' if harmonics[j]==-1 else 'Bullish '
                label = sense + labels[j] + ' found' 

                start = np.array(current_idx).min()
                end = np.array(current_idx).max()
                date = data.iloc[end].name
                trade_dates = np.append(trade_dates,date)

                pips = walk_forward(price.values[end:],harmonics[j])

                pnl = np.append(pnl,pips)

                cumpips = pnl.cumsum()

                if pips>0:
                    correct_pats+=1

                lbl = 'Accuracy ' + str(100*float(correct_pats)/float(pats)) + ' %'

                plt.clf()
                plt.plot(cumpips,label=lbl)
                plt.legend()
                plt.pause(5.05)

                # plt.title(label)
                # plt.plot(np.arange(start,i+15),price.values[start:i+15])
                # plt.scatter(current_idx,current_pat,c='r')
                # plt.show()


# peaks = price.values[idx]

# print(max_idx)
# print(min_idx)

