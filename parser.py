"""Analysing Tamilnadu air quality"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.io import save
from bokeh.models import BoxAnnotation
from bokeh.plotting import figure, output_file

REQ_COLUMNS = ['Stn Code', 'Sampling Date', 'State', 'City/Town/Village/Area',
               'Location of Monitoring Station', 'SO2', 'NO2',
               'RSPM/PM10']
AGG_COLUMNS = ['Sampling Date', 'Location of Monitoring Station', 'AQI']
FINAL_COLUMNS = ['Sampling Date', 'AQI']

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
    elif so2 > 40 and so2 <= 80:
        return 50 + (so2 - 40) * 50/40
    elif so2 > 80 and so2 <= 380:
        return 100 + (so2- 80) * 100/300
    elif so2 > 380 and so2 <= 380:
        return 200 + (so2 - 380) * 100/420
    elif so2 > 800 and so2 <= 1600:
        return 300 + (so2 - 800) * 100/800
    elif so2 > 1600:
        return 400 + (so2 - 1600) * 100/80

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

if __name__ == "__main__":
    data = pd.DataFrame()
    for data_f in os.listdir('resources'):
        tdf = pd.read_csv(
            os.path.join('resources', data_f),
            usecols=REQ_COLUMNS
        )
        data = pd.concat([
            data,
            tdf
        ])
    data['Sampling Date'] = pd.to_datetime(data['Sampling Date'])
    data['SO2'] = data['SO2'].apply(calculate_sub_index_so2)
    data['NO2'] = data['NO2'].apply(calculate_sub_index_no2)
    data['RSPM/PM10'] = data['RSPM/PM10'].apply(calculate_sub_index_pm10)
    data['AQI'] = data[['SO2', 'NO2', 'RSPM/PM10']].max(axis=1)
    data.set_index('Stn Code', inplace=True)
    data = data[AGG_COLUMNS]
    group_object = data.groupby(['Stn Code'])
    key_values = group_object.groups.keys()
    for key in key_values:
        sub_data = group_object.get_group(key)
        location = sub_data.iloc[0]['Location of Monitoring Station']

        #Sort the df
        sub_data.sort_values(by='Sampling Date', inplace=True)

        #Create the plot
        plot = figure(plot_width=3840, plot_height=2160, x_axis_type="datetime")
        #Set attributes
        plot.xaxis.axis_label = 'Date'
        plot.yaxis.axis_label = 'Air Quality Index'

        #Construct the image
        plot.line(x=sub_data['Sampling Date'], y=sub_data['AQI'])

        #Add Plot Bands
        good = BoxAnnotation(bottom=0, top=50, fill_alpha=0.1, fill_color='#79bc6a')
        satisfactory = BoxAnnotation(bottom=50, top=100, fill_alpha=0.1, fill_color='#bbcf4c')
        moderately_polluted = BoxAnnotation(bottom=100, top=200, fill_alpha=0.1, fill_color='#FFCF00')
        poor = BoxAnnotation(bottom=200, top=300, fill_alpha=0.1, fill_color='#FF9A00')
        very_poor = BoxAnnotation(bottom=300, top=400, fill_alpha=0.1, fill_color='red')
        severe = BoxAnnotation(bottom=400, top=500, fill_alpha=0.1, fill_color='brown')

        plot.add_layout(good)
        plot.add_layout(satisfactory)
        plot.add_layout(moderately_polluted)
        plot.add_layout(poor)
        plot.add_layout(very_poor)
        plot.add_layout(severe)

        #Save the image
        output_file(".\\images\\"  + location + ".html")
        save(plot)
