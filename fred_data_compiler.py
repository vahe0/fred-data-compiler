import pandas as pd
from fredapi import Fred
from functools import reduce

#############################################
#ENTER YOUR API KEY HERE IN THE SINGLE QUOTES
api_key = ''


fred = Fred(api_key= api_key)

#Code for the menu and deciding which time series frequencies to use when gathering and resampling the data
options = {1:'d', 2:'m', 3:'q',4:'a'}
symbols = input("Enter symbols seperated by a space \n").upper().split()
frequency = int(input('\nSelect frequency (type corresponding number and press enter)\n (1) Daily \n (2) Monthly \n (3) Quarterly \n (4) Annually\n'))

if frequency in options.keys():
    freq = options[frequency]

if frequency == 2:
    resample_freq = 'MS'
elif frequency == 3:
    resample_freq = 'QS'
elif frequency == 4:
    resample_freq = 'YS'
else:
    resample_freq = options[frequency]



data_list =[]

for symbol in symbols:
    try:
        #Get monthly symbol data and store in a dataframe
        data_series = fred.get_series(symbol, frequency = freq)
        data = pd.DataFrame({'Date': data_series.index, symbol: data_series.values})
    except ValueError as e:
        #If the data in FRED does not have the frequency of 'monthly', resample to monthly
        if "Bad Request.  Value of frequency is not one of:" in str(e):
            print(str(e), 'for symbol ', symbol)
            print(f'    The {symbol} series will be resampled from its default.')
            data = fred.get_series(symbol, frequency = 'a')
            dataframe = pd.DataFrame({'Date': data.index, symbol: data.values})
            data = dataframe.set_index('Date').resample(resample_freq).bfill().reset_index()
           
            
    #Set name for dataframe and append to a list for merging    
    try:
        data.name = symbol
    except NameError:
        print("One or more symbols may be incorrect. Exiting")
        raise SystemExit(0)
        
    
    data_list.append(data)


#Merge dataframes and export to csv

merged_dataframe = reduce(lambda left,right: pd.merge(left,right,on=['Date'], how='outer'), data_list)

#Drop duplicate columns and remove _x suffix
to_drop = [x for x in merged_dataframe if x.endswith('_y')]
merged_dataframe.drop(to_drop, axis=1, inplace=True)

for col in merged_dataframe:
        if col.endswith('_x'):
            merged_dataframe.rename(columns={col:col.rstrip('_x')}, inplace=True)


#Drop rows with null values
final_dataframe = merged_dataframe.dropna(how='any',axis=0) 


#Export
while True:
    try:
        final_dataframe.to_csv('./FRED Data.csv', index = False)
        break
    except PermissionError:
        input('Previous CSV file may be open. Please close it and press enter to overwrite.')


