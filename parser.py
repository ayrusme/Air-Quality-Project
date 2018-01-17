"""Analysing air quality levels of India"""

import os

import pandas as pd

REQ_COLUMNS = ['Stn Code', 'Sampling Date', 'State', 'City/Town/Village/Area',
               'Location of Monitoring Station', 'SO2', 'NO2',
               'RSPM/PM10']
FINAL_COLUMNS = ['Stn Code', 'Year', 'Month', 'AQI']

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
    final_df = pd.DataFrame(columns=FINAL_COLUMNS)
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
    
    city_group = data.groupby(['City/Town/Village/Area'])
    cities = city_group.groups.keys()

    for city in cities:
        sub_data = city_group.get_group(city)
        sub_locality_group = sub_data.groupby(['Stn Code'])
        sub_localities = sub_locality_group.groups.keys()

        for sub_locality in sub_localities:
            location_data = sub_locality_group.get_group(sub_locality)

            legend = location_data.iloc[0]['Location of Monitoring Station']

            location_data['Sampling Date'] = pd.to_datetime(location_data['Sampling Date'])

            year_group = location_data.groupby(location_data['Sampling Date'].map(lambda x: x.year))
            year_keys = year_group.groups.keys()

            for year in year_keys:
                year_data = year_group.get_group(year)

                year_data['Sampling Date'] = pd.to_datetime(year_data['Sampling Date'])
                
                month_group = year_data.groupby(year_data['Sampling Date'].map(lambda x: x.month))
                month_keys = month_group.groups.keys()

                for month in month_keys:
                    final_df = final_df.append({"Stn Code" : sub_locality,
                                                "Year" : year,
                                                "Month" : month,
                                                "AQI" : month_group.get_group(month)['AQI'].median()},
                                               ignore_index=True)
    final_df[['Stn Code', 'Year', 'Month']] = final_df[['Stn Code', 'Year', 'Month']].applymap(lambda x: int(x))
    final_df.to_csv(".\\datas\\AQI_India.csv")
