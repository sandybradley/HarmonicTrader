import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

def peak_detect(price,order=7):
    max_idx = list(argrelextrema(price,np.greater,order=order)[0])
    min_idx = list(argrelextrema(price,np.less,order=order)[0])

    idx = max_idx + min_idx + [len(price)-1]
    idx.sort()

    current_idx = idx[-5:]
    start = min(current_idx)
    end = max(current_idx)

    current_pat = price[current_idx]

    return current_idx,current_pat,start,end

def is_gartley(moves,err_allowed):
    XA=moves[0]
    AB=moves[1]
    BC=moves[2]
    CD=moves[3]

    retVal = np.NAN

    AB_range = np.array([0.618 - err_allowed,0.618 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed,0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([1.27 - err_allowed,1.618 + err_allowed]) * abs(BC)
    
    
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = 1
    elif XA < 0  and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = -1

    return retVal

def is_butterfly(moves,err_allowed):
    XA=moves[0]
    AB=moves[1]
    BC=moves[2]
    CD=moves[3]

    retVal = np.NAN

    AB_range = np.array([0.786 - err_allowed,0.786 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed,0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([1.618 - err_allowed,2.618 + err_allowed]) * abs(BC)
    
    
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = 1
    elif XA < 0  and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = -1

    return retVal

def is_bat(moves,err_allowed):
    XA=moves[0]
    AB=moves[1]
    BC=moves[2]
    CD=moves[3]

    retVal = np.NAN

    AB_range = np.array([0.382 - err_allowed,0.5 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed,0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([1.618 - err_allowed,2.618 + err_allowed]) * abs(BC)
    
    
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = 1
    elif XA < 0  and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = -1

    return retVal

def is_crab(moves,err_allowed):
    XA=moves[0]
    AB=moves[1]
    BC=moves[2]
    CD=moves[3]

    retVal = np.NAN

    AB_range = np.array([0.382 - err_allowed,0.618 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed,0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([2.24 - err_allowed,3.618 + err_allowed]) * abs(BC)
    
    
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = 1
    elif XA < 0  and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = -1

    return retVal

def is_shark(moves,err_allowed):
    XA=moves[0]
    AB=moves[1]
    BC=moves[2]
    CD=moves[3]

    retVal = np.NAN

    # AB_range = np.array([0.382 - err_allowed,0.618 + err_allowed]) * abs(XA)
    BC_range = np.array([1.13 - err_allowed,1.618 + err_allowed]) * abs(AB)
    CD_range = np.array([1.618 - err_allowed,2.24 + err_allowed]) * abs(BC)
    
    
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if  BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = 1
    elif XA < 0  and AB > 0 and BC < 0 and CD > 0:
        if  BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = -1

    return retVal

def is_trio(moves,err_allowed):
    XA=moves[1]
    AB=moves[2]
    BC=moves[3]
    # CD=moves[3]

    retVal = np.NAN

    AB_range = np.array([0.618 - err_allowed,0.786 + err_allowed]) * abs(XA)
    BC_range = np.array([1.27 - err_allowed,1.618 + err_allowed]) * abs(AB)
    # CD_range = np.array([1.618 - err_allowed,2.24 + err_allowed]) * abs(BC)
    
    
    if XA > 0 and AB < 0 and BC > 0:
        if  BC_range[0] < abs(BC) < BC_range[1] and AB_range[0] < abs(AB) < AB_range[1]:
            retVal = -1
    elif XA < 0  and AB > 0 and BC < 0:
        if  BC_range[0] < abs(BC) < BC_range[1] and AB_range[0] < abs(AB) < AB_range[1]:
            retVal = 1

    return retVal

def walk_forward(price,sign,slippage=10.0,stop=150.0):
    if sign == 1:
        initial_stop_loss = price[0] - stop
        stop_loss = initial_stop_loss
        for i in range (1,len(price)):
            move = price[i] - price[i-1]
            if move > 0 and (price[i]-stop)>initial_stop_loss:
                stop_loss = price[i] - stop
            elif price[i] < stop_loss:
                return stop_loss - price[0] -slippage
    elif sign == -1:
        initial_stop_loss = price[0] - stop
        stop_loss = initial_stop_loss
        for i in range (1,len(price)):
            move = price[i] - price[i-1]
            if move < 0 and (price[i]+stop)<initial_stop_loss:
                stop_loss = price[i] + stop
            elif price[i] > stop_loss:
                return  price[0] - stop_loss - slippage

def is_cyph(moves,err_allowed):
    XA=moves[0]
    AB=moves[1]
    BC=moves[2]
    CD=moves[3]

    retVal = np.NAN

    AB_range = np.array([0.382 - err_allowed,0.618 + err_allowed]) * abs(XA)
    BC_range = np.array([1.13 - err_allowed,1.414 + err_allowed]) * abs(AB)
    CD_range = np.array([1.272 - err_allowed,2.0 + err_allowed]) * abs(BC)
    
    
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = 1
    elif XA < 0  and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
            retVal = -1

    return retVal