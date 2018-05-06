
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import style
style.use('seaborn')

df = pd.read_csv(r'data/GOOGL_data.csv', parse_dates=['Date'])
df.drop(['Close'],axis=1,inplace=True)
df.set_index(['Date'], inplace=True)
df.dropna(inplace=True)
df = df[-200:] #Avgränsa

def STOK(df):  
    Stoch = pd.Series((df['Adj Close'] - df['Low']) / (df['High'] - df['Low']), name = 'Stoch')  
    df = df.join(Stoch)  
    return df

stocha = STOK(df)
df = df.join(stocha['Stoch'])


# In[2]:



###USER PARAMETERS ###
initial_capital = 10000
number_of_shares = 10

lower_threshold = 0.2
higher_threshold = 0.8
###

price = df.loc[:, 'Adj Close'].tolist()
open_p = df.loc[:, 'Open'].tolist()
stoch = df.loc[:, 'Stoch'].tolist()

open_trade = False
entry_trade = []
exit_trade = []
equity = []
sum_eq = []
activetrade = [] #1 for long, -1 for short and 0 for flat

#Run strat
for i in range(len(df)):
    if stoch[i] > lower_threshold and stoch[i-1] < lower_threshold and not open_trade: #Crossing
        entry_price = open_p[i+1] #Next bar buy price (entry price)
        entry_trade.append(entry_price)
        activetrade.append(1) 
        open_trade = True
        
    elif stoch[i] < higher_threshold and stoch[i-1] > higher_threshold and open_trade: #Crossing 
        if activetrade:
            exit_price = price[i]
            exit_trade.append(exit_price)
            activetrade.append(0)
            open_trade = False
            
    elif open_trade:
        activetrade.append(1)
    else:
        activetrade.append(0) 
        
#Equity calc
try:
    for i in range(len(entry_trade)):
        trade_equity = exit_trade[i] - entry_trade[i]
        equity.append(trade_equity)
except Exception as e:
    print(e)
    
#Visualize equity
for i in range(len(equity)):
    sum_eq.append((sum(equity[0:i]))*number_of_shares)
    
#Final equity  
for i in sum_eq[-1:]:
    final_eq = i

#Append active trade? to df
df['Active_trade'] = activetrade


# In[3]:


plt.figure()
plt.suptitle('GOOGL')
ax1 = plt.subplot2grid((4,1),(0,0), rowspan=2, colspan=1)
ax2 = plt.subplot2grid((4,1),(2,0), rowspan=1, colspan=1, sharex=ax1)
ax3 = plt.subplot2grid((4,1),(3,0), rowspan=1, colspan=1)

ax1.plot(df['Adj Close'])
ax2.plot(df['Stoch'])
ax3.plot(df['Active_trade'])

ax2.axhline(lower_threshold, color='c')
ax2.axhline(higher_threshold, color='c')

ax1.set_xticklabels([])

plt.show()


# In[4]:


### EQUITY ###
plt.plot(sum_eq)
plt.title('Equity curve')
plt.show()
print('Result in percentage:')
print((final_eq / initial_capital)*100,'%')

