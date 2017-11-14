import os

import matplotlib.pyplot as plt
import numpy
import pandas as pd


def construct_initial_dataframe():
    """Function to read resources and construct the initial dataframe"""
    reqd_cols = ['Sampling Date', 'State', 'City/Town/Village/Area', 'Location of Monitoring Station', 'SO2', 'NO2', 'RSPM/PM10']
    #Reading all files inside resources folder
    files_list = os.listdir('resources')
    df_list = []
    for filex in files_list:
        df = pd.read_csv('.\\resources\\'+filex, usecols=reqd_cols)
        df.fillna(0, inplace=True)
        df[['SO2', 'NO2', 'RSPM/PM10']] = df[['SO2', 'NO2', 'RSPM/PM10']].astype(numpy.int64)
        df_list.append(df)
    #Sending back a list of dataframes
    return df_list

def calculate_sub_index_pm10(pm_10):
    """Function to calculate the sub-index of the pollutant PM10"""
    #Formula taken from AQI calculator excel sheet
    if pm_10 <= 100:
        return pm_10
    elif pm_10 > 100 and pm_10 <= 250:
        return 100 + (pm_10 - 100) * 100/150
    elif pm_10 > 250 and pm_10 <= 350:
        return 200 + (pm_10 - 250)
    elif pm_10 > 350 and pm_10 <= 430:
        return 300 + (pm_10 - 350) * (100/80)
    elif pm_10 > 430:
        return 400 + (pm_10 - 430) * (100/80)

def calculate_sub_index_so2(so2):
    """Function to calculate the sub-index of the pollutant SO2"""
    #Formula taken from AQI calculator excel sheet
    if so2 <= 40:
        return so2*50/40
    elif so2 > 40 and so2 <=80:
        return 50 + (so2 - 40) * 50/40
    elif so2 > 80 and so2 <= 380:
        return 100 + ( so2- 80) * 100/300
    elif so2 > 380 and so2 <= 380:
        return 200 + (so2 - 380) * 100/420
    elif so2 > 800 and so2 <= 1600:
        return 300 + (so2 - 800) * 100/800
    elif so2 > 1600:
        return 400 + ( so2 - 1600) * 100/80

def calculate_sub_index_no2(no2):
    """Function to calculate the sub-index of the pollutant no2"""
    #Formula taken from AQI calculator excel sheet
    if no2 <= 40:
        return no2
    elif no2 > 40 and no2 <= 80:
        return 50 + (no2 - 40)
    elif no2 > 80 and no2 <= 180:
        return 100 + (no2 - 80)
    elif no2 > 180 and no2 <= 280:
        return 200 + (no2 - 180)
    elif no2 > 280 and no2 <= 400:
        return 300 + (no2 - 280) * (100 / 120)
    elif no2 > 400:
        return 400 + (no2 - 400) * (100 / 120)

df_list = construct_initial_dataframe()
output_columns = ['Sampling Date', 'State', 'City/Town/Village/Area', 'Location of Monitoring Station', 'AQI']
for df in df_list:
    df['RSPM/PM10'] = df['RSPM/PM10'].map(lambda pm_10: int(calculate_sub_index_pm10(pm_10)))
    df['SO2'] = df['SO2'].map(lambda so2: int(calculate_sub_index_so2(so2)))
    df['NO2'] = df['NO2'].map(lambda no2: int(calculate_sub_index_no2(no2)))
    #Now the columns have been replaced with their sub index values
    #Let's calculate the AQI for each of the locations
    group_object = df.groupby(['Location of Monitoring Station'])
    key_values = group_object.groups.keys()
    for key in key_values:
        df = group_object.get_group(key)
        df['AQI'] = df[['SO2','NO2','RSPM/PM10']].max(axis=1)
        df.to_csv('.\\output\\'+key+'.csv', mode='a', header=False, columns=output_columns)

#Reading all files inside resources folder
files_list = os.listdir('output')
df_list = []
for filex in files_list:
    df = pd.read_csv('.\\output\\'+filex, names=output_columns)
    axle = df.plot(x='Sampling Date', y='AQI')
    axle.get_figure().savefig('.\\images\\'+ filex +'.png')
