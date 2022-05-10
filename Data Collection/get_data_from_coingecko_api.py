#Import libs
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import time

def get_data(currency):
  url = f'https://api.coingecko.com/api/v3/coins/{currency}/market_chart?vs_currency=usd&days=max&interval=daily'

  response = requests.get(url)
  data = response.json()
  output = pd.DataFrame(data)

  for i in output['prices']:
    crypto['id'].append(currency)
    date = datetime.fromtimestamp(i[0]/1000)
    crypto['date'].append(date.strftime('%Y-%m-%d'))
    crypto['price'].append(round(i[1], 2))


#== Script start==

#--Getting general data--
url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
response = requests.get(url)
resp = response.json()
output = pd.DataFrame.from_dict(resp)
general_data = output[['id', 'symbol', 'name', 'market_cap']]

crypto = {'id':[], 'date':[], 'price':[]}

for i in general_data.id:
  time.sleep(0.5)
  print('Starting: ', i)
  get_data(i)

historical_data = pd.DataFrame.from_dict(crypto)

try:
    general_data.reset_index(drop=True, inplace=True)
    general_data.to_csv('general_data.csv', sep=';')
    print('General_data df saved into "general_data.csv"')
except:
    print('Ops, something goes wrong with General_data into file.')

try:
    historical_data.reset_index(drop=True, inplace=True)
    historical_data.to_csv('historical_data.csv', sep=';')
    print('Historical_data df saved into "historical_data.csv"')
except:
    print('Ops, something goes wrong with Historical_data into file.')

exec(open("insert_into_database.py").read())