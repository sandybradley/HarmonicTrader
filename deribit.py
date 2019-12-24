import requests 
  
# api-endpoint 
URL = "https://www.deribit.com/api/v2/public/auth"
    
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'client_id':'id','client_secret':'secret','grant_type':'client_credentials'} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
  
# extracting data in json format 
dat = r.json() 
# print(dat)
# Configure Bearer authorization (Auth. Token): bearerAuth
access_token = dat['result']['access_token']
instrument_name = 'BTC-PERPETUAL' # str | Instrument name
amount = 10 # float | It represents the requested order size. For perpetual and futures the amount is in USD units, for options it is amount of corresponding cryptocurrency contracts, e.g., BTC or ETH
currency = 'BTC' # str | The currency symbol

equity = 0.0
delta = 0.0
pnl = 0.0

limit_buys = []
limit_sells = []
buy_order_ids = []
sell_order_ids = []
stop_order_ids = []
stops = []

def getAccess():
    global access_token
    # api-endpoint 
    URL = "https://www.deribit.com/api/v2/public/auth"
        
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'client_id':'id','client_secret':'secret','grant_type':'client_credentials'} 
    
    try:
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, params = PARAMS) 
        
        # extracting data in json format 
        dat = r.json() 
        # print(dat)
        # Configure Bearer authorization (Auth. Token): bearerAuth
        access_token = dat['result']['access_token']
    except:
        print('Could not get access token')

def getaccSum():
    global equity,delta,pnl
    URL = "https://www.deribit.com/api/v2/private/get_account_summary"
    
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'currency':currency} 
    HEADERS={'Authorization': 'Bearer ' + access_token}
    
    try:
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, params = PARAMS, headers=HEADERS) 
        
        # extracting data in json format 
        dat = r.json() 
        # print(dat['result'])

        # assign globals
        delta = dat['result']['delta_total']
        equity = dat['result']['equity']
        pnl = dat['result']['total_pl']
        
        print('Equity ',equity)
        print('delta ',delta)
        print('pnl ',pnl)
    except:
        print('Could not get account summary')

def buy_limit(price):
    global limit_buys,buy_order_ids
    # create an instance of the API class
    type = 'limit' # str | The order type, default: `\"limit\"` (optional)
    label = 'harmonic_trader' # str | user defined label for the order (maximum 32 characters) (optional)
    price = price # float | <p>The order price in base currency (Only for limit and stop_limit orders)</p> <p>When adding order with advanced=usd, the field price should be the option price value in USD.</p> <p>When adding order with advanced=implv, the field price should be a value of implied volatility in percentages. For example,  price=100, means implied volatility of 100%</p> (optional)
    time_in_force = 'good_til_cancelled' # str | <p>Specifies how long the order remains in effect. Default `\"good_til_cancelled\"`</p> <ul> <li>`\"good_til_cancelled\"` - unfilled order remains in order book until cancelled</li> <li>`\"fill_or_kill\"` - execute a transaction immediately and completely or not at all</li> <li>`\"immediate_or_cancel\"` - execute a transaction immediately, and any portion of the order that cannot be immediately filled is cancelled</li> </ul> (optional) (default to 'good_til_cancelled')
    post_only = 'true' # bool | <p>If true, the order is considered post-only. If the new price would cause the order to be filled immediately (as taker), the price will be changed to be just below the bid.</p> <p>Only valid in combination with time_in_force=`\"good_til_cancelled\"`</p> (optional) (default to True)
    reduce_only = 'false' # bool | If `true`, the order is considered reduce-only which is intended to only reduce a current position (optional) (default to False)
 
    
    URL = "https://www.deribit.com/api/v2/private/buy"
    
    # defining a params dict for the parameters to be sent to the API 
    params = {'instrument_name':instrument_name,'amount':amount,'type':type,'price':price,'time_in_force':time_in_force,'post_only':post_only,'reduce_only':reduce_only} 
    HEADERS={'Authorization': 'Bearer ' + access_token,'content-type': 'application/json'}
    
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = params, headers=HEADERS ) 
    
    # extracting data in json format 
    dat = r.json() 
    print(dat['result'])

    limit_buys.append(price)
    buy_order_ids.append(dat['result']['order_id'])
    

def sell_limit(price):
    global limit_sells,sell_order_ids
    # create an instance of the API class
    type = 'limit' # str | The order type, default: `\"limit\"` (optional)
    label = 'harmonic_trader' # str | user defined label for the order (maximum 32 characters) (optional)
    price = price # float | <p>The order price in base currency (Only for limit and stop_limit orders)</p> <p>When adding order with advanced=usd, the field price should be the option price value in USD.</p> <p>When adding order with advanced=implv, the field price should be a value of implied volatility in percentages. For example,  price=100, means implied volatility of 100%</p> (optional)
    time_in_force = 'good_til_cancelled' # str | <p>Specifies how long the order remains in effect. Default `\"good_til_cancelled\"`</p> <ul> <li>`\"good_til_cancelled\"` - unfilled order remains in order book until cancelled</li> <li>`\"fill_or_kill\"` - execute a transaction immediately and completely or not at all</li> <li>`\"immediate_or_cancel\"` - execute a transaction immediately, and any portion of the order that cannot be immediately filled is cancelled</li> </ul> (optional) (default to 'good_til_cancelled')
    post_only = 'true' # bool | <p>If true, the order is considered post-only. If the new price would cause the order to be filled immediately (as taker), the price will be changed to be just below the bid.</p> <p>Only valid in combination with time_in_force=`\"good_til_cancelled\"`</p> (optional) (default to True)
    reduce_only = 'false' # bool | If `true`, the order is considered reduce-only which is intended to only reduce a current position (optional) (default to False)
 
    
    URL = "https://www.deribit.com/api/v2/private/sell"
    
    # defining a params dict for the parameters to be sent to the API 
    params = {'instrument_name':instrument_name,'amount':amount,'type':type,'price':price,'time_in_force':time_in_force,'post_only':post_only,'reduce_only':reduce_only} 
    HEADERS={'Authorization': 'Bearer ' + access_token,'content-type': 'application/json'}
   
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = params, headers=HEADERS ) 
    
    # extracting data in json format 
    dat = r.json() 
    print(dat['result'])

    limit_sells.append(price)
    sell_order_ids.append(dat['result']['order_id'])
  

def buy_stop(price):
    global stops,stop_order_ids
    # create an instance of the API class
    type = 'stop_market' # str | The order type, default: `\"limit\"` (optional)
    label = 'harmonic_trader' # str | user defined label for the order (maximum 32 characters) (optional)
    price = price # float | <p>The order price in base currency (Only for limit and stop_limit orders)</p> <p>When adding order with advanced=usd, the field price should be the option price value in USD.</p> <p>When adding order with advanced=implv, the field price should be a value of implied volatility in percentages. For example,  price=100, means implied volatility of 100%</p> (optional)
    time_in_force = 'good_til_cancelled' # str | <p>Specifies how long the order remains in effect. Default `\"good_til_cancelled\"`</p> <ul> <li>`\"good_til_cancelled\"` - unfilled order remains in order book until cancelled</li> <li>`\"fill_or_kill\"` - execute a transaction immediately and completely or not at all</li> <li>`\"immediate_or_cancel\"` - execute a transaction immediately, and any portion of the order that cannot be immediately filled is cancelled</li> </ul> (optional) (default to 'good_til_cancelled')
    post_only = 'true' # bool | <p>If true, the order is considered post-only. If the new price would cause the order to be filled immediately (as taker), the price will be changed to be just below the bid.</p> <p>Only valid in combination with time_in_force=`\"good_til_cancelled\"`</p> (optional) (default to True)
    reduce_only = 'true' # bool | If `true`, the order is considered reduce-only which is intended to only reduce a current position (optional) (default to False)
 
    
    URL = "https://www.deribit.com/api/v2/private/buy"
    
    # defining a params dict for the parameters to be sent to the API 
    params = {'instrument_name':instrument_name,'amount':amount,'type':type,'price':price,'time_in_force':time_in_force,'post_only':post_only,'reduce_only':reduce_only} 
    HEADERS={'Authorization': 'Bearer ' + access_token,'content-type': 'application/json'}
    
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = params, headers=HEADERS ) 
    
    # extracting data in json format 
    dat = r.json() 
    print(dat['result'])

    stops.append(price)
    stop_order_ids.append(dat['result']['order_id'])
   

def sell_stop(price):
    global stops,stop_order_ids
    # create an instance of the API class
    type = 'stop_market' # str | The order type, default: `\"limit\"` (optional)
    label = 'harmonic_trader' # str | user defined label for the order (maximum 32 characters) (optional)
    price = price # float | <p>The order price in base currency (Only for limit and stop_limit orders)</p> <p>When adding order with advanced=usd, the field price should be the option price value in USD.</p> <p>When adding order with advanced=implv, the field price should be a value of implied volatility in percentages. For example,  price=100, means implied volatility of 100%</p> (optional)
    time_in_force = 'good_til_cancelled' # str | <p>Specifies how long the order remains in effect. Default `\"good_til_cancelled\"`</p> <ul> <li>`\"good_til_cancelled\"` - unfilled order remains in order book until cancelled</li> <li>`\"fill_or_kill\"` - execute a transaction immediately and completely or not at all</li> <li>`\"immediate_or_cancel\"` - execute a transaction immediately, and any portion of the order that cannot be immediately filled is cancelled</li> </ul> (optional) (default to 'good_til_cancelled')
    post_only = 'true' # bool | <p>If true, the order is considered post-only. If the new price would cause the order to be filled immediately (as taker), the price will be changed to be just below the bid.</p> <p>Only valid in combination with time_in_force=`\"good_til_cancelled\"`</p> (optional) (default to True)
    reduce_only = 'true' # bool | If `true`, the order is considered reduce-only which is intended to only reduce a current position (optional) (default to False)
 
    
    URL = "https://www.deribit.com/api/v2/private/sell"
    
    # defining a params dict for the parameters to be sent to the API 
    params = {'instrument_name':instrument_name,'amount':amount,'type':type,'price':price,'time_in_force':time_in_force,'post_only':post_only,'reduce_only':reduce_only} 
    HEADERS={'Authorization': 'Bearer ' + access_token,'content-type': 'application/json'}
    
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = params, headers=HEADERS ) 
    
    # extracting data in json format 
    dat = r.json() 
    print(dat['result'])

    stops.append(price)
    stop_order_ids.append(dat['result']['order_id'])

def edit_stop(price):
    global stops
    
    URL = "https://www.deribit.com/api/v2/private/edit"
    
    # defining a params dict for the parameters to be sent to the API 
    params = {'order_id':stop_order_ids[0],'amount':amount,'price':price} 
    HEADERS={'Authorization': 'Bearer ' + access_token,'content-type': 'application/json'}
    
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = params, headers=HEADERS ) 
    
    # extracting data in json format 
    dat = r.json() 
    print(dat['result'])

    stops[0] = price


    
