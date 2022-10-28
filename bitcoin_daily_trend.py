from datetime import datetime, timedelta
from pytrends.request import TrendReq
import pandas as pd
import os
import sys
import time

daily = False
hourly = False
if len(sys.argv) != 2:
    print("Usage: python scaledata.py <hourly/daily>")
    exit(-1)
elif sys.argv[1] == 'hourly':
    hourly = True
elif sys.argv[1] == 'daily':
    daily = True
else:
    print("Usage: python scaledata.py <hourly/daily>")
    exit(-1)

path = '.'
os.chdir(path)
filename = 'bitcoin_daily_trend.csv'

if daily:
    maxstep = 269
    overlap = 40
    step = maxstep - overlap + 1
    dt = timedelta(days=step)
    time_fmt = '%Y-%m-%d'
elif hourly:
    overlap = 18
    step = 168
    dt = timedelta(hours=step)
    time_fmt = '%Y-%m-%dT%H'
kw_list = ['Bitcoin']
start_date = datetime(2009, 1, 2).date()

pytrend = TrendReq()

today = datetime.today().date()
old_date = today

new_date = today - dt
timeframe = new_date.strftime(time_fmt) + ' ' + old_date.strftime(time_fmt)
print(timeframe)
pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
interest_over_time_df = pytrend.interest_over_time()

while new_date > start_date:
    old_date = new_date + timedelta(hours=overlap-1)

    new_date = new_date - dt

    if new_date < start_date:
        new_date = start_date

    timeframe = new_date.strftime(time_fmt) + ' ' + old_date.strftime(time_fmt)
    print(timeframe)

    pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
    temp_df = pytrend.interest_over_time()
    if (temp_df.empty):
        raise ValueError('Google sent back an empty dataframe. Possibly there were no searches at all during this period! Set start_date to a later date.')

    for kw in kw_list:
        beg = new_date
        end = old_date - timedelta(hours=1)

        for t in range(1, overlap + 1):
            if temp_df[kw].iloc[-t] != 0:
                scaling = float(interest_over_time_df[kw].iloc[t-1])/temp_df[kw].iloc[-t]
                print(scaling)
                break
            elif t == overlap:
                print('Did not find non-zero overlap, set scaling to zero! Increase Overlap!')
                scaling = 0

        temp_df.loc[beg:end, kw] = temp_df.loc[beg:end, kw] * scaling
    interest_over_time_df = pd.concat([temp_df[:-overlap], interest_over_time_df])
    time.sleep(1)

interest_over_time_df.to_csv(filename)
