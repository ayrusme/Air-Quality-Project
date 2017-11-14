import os

import numpy
import pandas as pd


def construct_initial_dataframe():
    """Function to read resources and construct the initial dataframe"""
    reqd_cols = ['Sampling Date', 'State', 'City/Town/Village/Area', 'Location of Monitoring Station', 'SO2', 'NO2', 'RSPM/PM10']
    files_list = os.listdir('resources')
    df_list = []
    for filex in files_list:
        df = pd.read_csv('.\\resources\\'+filex, usecols=reqd_cols)
        df.fillna(0, inplace=True)
        df[['SO2', 'NO2', 'RSPM/PM10']] = df[['SO2', 'NO2', 'RSPM/PM10']].astype(numpy.int64)
        df_list.append(df)
    return df_list

def calculate_sub_index_pm10(pm_10):
    """Function to calculate the sub-index of the pollutant PM10"""
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

df_list = construct_initial_dataframe()
for df in df_list:
    df['RSPM/PM10'] = df['RSPM/PM10'].map(lambda pm_10: calculate_sub_index_pm10(pm_10))
    df['SO2'] = df['SO2'].map(lambda so2: calculate_sub_index_so2(so2))