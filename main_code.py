import os
import csv
import json
import time
import requests
import pandas as pd
import yfinance as yf
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use('fivethirtyeight')
from pytz import timezone
from datetime import datetime
from datetime import date
tabulate.PRESERVE_WHITESPACE = False
size = 0
df = pd.DataFrame()
index=0
trend_oi = 0
current = 0
oi_time = []
time_list = 0

#############################################################
## Function to get live price
#############################################################
def live_price():
    symbol = "^NSEI"
    stock = yf.Ticker(symbol)
    historic_data = stock.history(period='id')
    closing_price = historic_data['Close']
    global current
    current = closing_price.iloc[-1]
    return current

#########################################################################
## List of fields not required in out while displaying option chain date
##
#########################################################################
keys_to_exclude = [
                    'pchangeinOpenInterest', 
                    'totalBuyQuantity', 
                    'totalSellQuantity', 
                    'underlyingValue',
                    'expiryDate',
                    'underlying',
                    'identifier',
                    'pChange'
]

#############################################################
## Funtion to restric decimal value to n place
## In this example decimle value is restricted
## to only 2 places
#############################################################
def set_decimal(x):
    return ('%.2f' % x).rstrip('0').rstrip('.')

#############################################################
## Function to fetch data
##  
#############################################################
def create_OC_JSON_object(u, h, t_o):   

    inLoop = True
    r = 10
    c = 0

    while inLoop:

        response = requests.get(u, headers=h, timeout=t_o)

        if response.status_code == 200:
            jo = json.loads(response.text)

            return True, jo
        else:
            print('Retry: ', c, ' ', response.status_code)
            c = c +1
            time.sleep(5)

            if c >= r:
                return False, None

#############################################################
## Function to get Option chain data
##  
#############################################################
def create_edate_data_dict(oc_json_obj):
    
    r_data = oc_json_obj['records']['data']
    e_dt=oc_json_obj['records']['expiryDates']
    
    oc_data = {}
    
    for ed in e_dt:
        
        oc_data[ed]={"CE":[], "PE":[]}
        
        for di in range(len(r_data)):
            if r_data[di]['expiryDate'] == ed:
                if 'CE' in r_data[di].keys() and r_data[di]['CE']['expiryDate'] == ed:                
                    oc_data[ed]["CE"].append(r_data[di]['CE'])
                else:
                    oc_data[ed]["CE"].append('-')

                if 'PE' in r_data[di].keys() and r_data[di]['PE']['expiryDate'] == ed:
                    oc_data[ed]["PE"].append(r_data[di]['PE'])
                else:
                    oc_data[ed]["PE"].append('-')
                                    
    return oc_data

#############################################################
## Function to remove unwanted content
##
#############################################################
def delete_unwanted_fields(oc_full_data):
    
    exp_dates = list(oc_full_data.keys())
    
    for e_dt in exp_dates:

        for i in range(len(oc_full_data[e_dt]['CE'])):
            if oc_full_data[e_dt]['CE'][i] != '-':
                for key in keys_to_exclude:
                    del oc_full_data[e_dt]['CE'][i][key]

            if oc_full_data[e_dt]['PE'][i] != '-':
                for key in keys_to_exclude:
                    del oc_full_data[e_dt]['PE'][i][key]

#############################################################
## Function to format and create final list of Option Chain
## data which is similar to NSE website
#############################################################
def preprate_final_data(r_ce, r_pe):
    l_OC = []

    for i in range(len(r_ce)):
        l_CE=[]
        l_PE=[]

        if r_ce[i] != '-':
            sp = r_ce[i]['strikePrice']
            l_CE =  [  
                        r_ce[i]['openInterest'],        r_ce[i]['changeinOpenInterest'] , 
                        r_ce[i]['totalTradedVolume'],   r_ce[i]['impliedVolatility'] , 
                        r_ce[i]['lastPrice'],           set_decimal(r_ce[i]['change']), 
                        r_ce[i]['bidQty'],              r_ce[i]['bidprice'] , 
                        r_ce[i]['askPrice'],            r_ce[i]['askQty'] , 
                        r_ce[i]['strikePrice']
                    ]
        else:
            sp = r_pe[i]['strikePrice']
            l_CE= list(['-','-','-','-','-','-','-','-','-','-',sp])

        if r_pe[i] != '-':
            l_PE =  [
                        r_pe[i]['bidQty'],              r_pe[i]['bidprice'] ,
                        r_pe[i]['askPrice'],            r_pe[i]['askQty'] , 
                        set_decimal(r_pe[i]['change']), r_pe[i]['lastPrice'] ,
                        r_pe[i]['impliedVolatility'],   r_pe[i]['totalTradedVolume'] ,
                        r_pe[i]['changeinOpenInterest'],r_pe[i]['openInterest']
            ] 

        else:
            l_PE = list(['-','-','-','-','-','-','-','-','-','-'])


        l_OC_t = l_CE + l_PE
        l_OC_t[:] = [x if x != 0 else '-' for x in l_OC_t]

        l_OC.append(l_OC_t)
    
    return l_OC

#############################################################
## Getting index of live price
#############################################################
def index_live_price(current):
    
    for i in range(size-1):
        if ( current > df.at[i, 'STRIKE'] and current < df.at[i+1, 'STRIKE']):
            temp = df.at[i, 'STRIKE'] + 25
            if( current < temp):
                return i
                break
            else:
                return i+1
                break
    return i

#############################################################
## Trending OI
#############################################################

def trending_oi():
    print("TRENDING OI :")
    head = ['Call_OI','Chng_in_call_oi', 'Strike', 'Put_OI', 'Chng_in_put_oi']
    call_oi = []
    put_oi = []
    ch_call_oi = []
    ch_put_oi = []
    data = []
    sum_ce_oi = 0
    sum_pe_oi = 0
    sum_ch_call_oi = 0
    sum_ch_put_oi = 0
    for i in range(1,6):
        call_oi.append(df.at[index+i, 'c_OI'])
        put_oi.append(df.at[index+i, 'p_OI'])
        ch_call_oi.append(df.at[index+i, 'c_CHNG_IN_OI'])
        ch_put_oi.append(df.at[index+i, 'p_CHNG_IN_OI'])
        #print(index+i)
    for i in range(1,6):
        call_oi.append(df.at[index-i, 'c_OI'])
        put_oi.append(df.at[index-i, 'p_OI'])
        ch_call_oi.append(df.at[index+i, 'c_CHNG_IN_OI'])
        ch_put_oi.append(df.at[index+i, 'p_CHNG_IN_OI'])
        #print(index-i)
    #print(call_oi)
    #print(put_oi)
    for i in range(len(call_oi)):
        sum_ce_oi += call_oi[i]
        sum_pe_oi += put_oi[i]
        sum_ch_call_oi += ch_call_oi[i]
        sum_ch_put_oi += ch_put_oi[i]
    for i in range(5):
        data.append([])
        data[i].append(call_oi[i])
        data[i].append(ch_call_oi[i])
        data[i].append(df.at[index+1+i, 'STRIKE'])
        data[i].append(put_oi[i])
        data[i].append(ch_put_oi[i])
    j=1
    for i in range(5,10):
        data.append([])
        data[i].append(call_oi[i])
        data[i].append(call_oi[i])
        data[i].append(df.at[index-j, 'STRIKE'])
        data[i].append(put_oi[i])
        data[i].append(ch_put_oi[i])
        j+=1
    print(tabulate(data, headers=head, tablefmt="fancy_grid"))
    print("")
    print("Sum of call OI: ",sum_ce_oi)
    print("Sum of put OI: ",sum_pe_oi)
    print("Sum of change in call OI: ",sum_ch_call_oi)
    print("Sum of change in put OI: ",sum_ch_put_oi)
    print("")
    print("")
    print("TRENDING OI: ",sum_pe_oi - sum_ce_oi)
    print("Change in OI: ",sum_ch_put_oi - sum_ch_call_oi)
    print("")
    print("")
    trend = sum_pe_oi - sum_ce_oi
    global trend_oi
    trend_oi = trend
    global time_list
    time_list = (datetime.now(timezone("Asia/Kolkata")).strftime('%H : %M : %S'))
    print(time_list)
    print(trend_oi)
    print("Trending OI graph: ")

#############################################################
## Function to display option chain data based on
## expiry date. 
#############################################################
def display_oc_data(oc_full_data_edt, ed):

    ce_data_edt = oc_full_data_edt[ed]['CE']
    pe_data_edt = oc_full_data_edt[ed]['PE']

    ## prepare final data
    l_final_oc_data_edt = preprate_final_data(ce_data_edt, pe_data_edt)

    OC_col = ['c_OI', 'c_CHNG_IN_OI', 'c_VOLUME', 'c_IV', 'c_LTP', 'c_CHNG', 'c_BID_QTY', 'c_BID', 'c_ASK', 'c_ASK_QTY',  'STRIKE', 'p_BID_QTY', 'p_BID', 'p_ASK', 'p_ASK_QTY',  'p_CHNG', 'p_LTP', 'p_IV', 'p_VOLUME', 'p_CHNG_IN_OI', 'p_OI']
   
    pd.set_option('display.max_rows', None)
    global df
    df = pd.DataFrame(l_final_oc_data_edt)
    df.columns = OC_col
    current_price = live_price()
    print("Current Price: ",current_price)
    global size
    size = len(df)
    print('')
    print(df)
    #print(tabulate(df, headers='keys', tablefmt='fancy_grid', colalign="center"'''* len(headers)'''))
    global index
    index = index_live_price(current)
    print("Current Price: ",current_price)
    print("")
    print("Strike Price: ",df.at[index, 'STRIKE'])
    print("")
    trending_oi()

#############################################################
## Main function
#############################################################
if __name__ == '__main__':
    fieldnames = ["time_list","trend"]
    with open('graph.csv','w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames= fieldnames)
        csv_writer.writeheader()
    while True:
        url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'               
        headers={'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
        oc_data = {}
        refresh_time = 60 # in seconds
        pd.set_option('display.max_rows', None)
        #pd.set_option('display.max_columns', None)

        success, oc_json_object = create_OC_JSON_object(url, headers, 10) ## Populate all expiry dates

        if success:

            oc_full_data = create_edate_data_dict(oc_json_object)
            delete_unwanted_fields(oc_full_data)
            expiry_dates = list(oc_full_data.keys())
            
            ed_i = 0
            print(expiry_dates[ed_i]) ## Print first expiry date
            '''for i in range (len(expiry_dates)):
                print(i,'. ',expiry_dates[i])
            ed_i = input("Enter index of date: ")'''
            print('=====================')

            # Show Option chain final data
            display_oc_data(oc_full_data, expiry_dates[ed_i])
            l_sec = time.localtime().tm_sec 
            '''for i in range(len(time_list)):
                graphdata(i)'''
        else:
            print('Error: Failed to scrap data..')
    ############################################################   
    # To save Data in a csv file
    ############################################################    
        with open('graph.csv','a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames= fieldnames)
            info = {
                "time_list": time_list,
                "trend": trend_oi
            }
            csv_writer.writerow(info)
        time.sleep(refresh_time)
        os.system('clear') 