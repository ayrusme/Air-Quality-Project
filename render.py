"""Script to render the plots from the final AQI data"""
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from codes import FINAL_COLUMNS, LOCATION, PLOT_DIR

sns.set()

def render_plot():
    """Function to render the plots for the given data"""

    FINAL_DF = pd.read_csv(".\\datas\\AQI_India.csv", usecols=FINAL_COLUMNS)

    city_group = FINAL_DF.groupby(['City'])
    cities = city_group.groups.keys()

    for city in cities:

        city_data = city_group.get_group(city)
        sub_locality_group = city_data.groupby(['Stn Code'])

        sub_localities = sub_locality_group.groups.keys()
        sub_localities = [x for x in sub_localities if x in LOCATION]

        # Draw a heatmap with the numeric values in each cell
        figure, axes = plt.subplots(figsize=(9, 6), ncols=len(sub_localities), squeeze=False)

        for sub_locality, ax in zip(sub_localities, axes):

            sub_localities_data = sub_locality_group.get_group(sub_locality)
            sub_localities_data = sub_localities_data.drop('Stn Code', 1)

            sub_localities_data = sub_localities_data.pivot("Month", "Year", "AQI")

            sns.heatmap(sub_localities_data,
                        ax=ax,
                        vmin=0,
                        vmax=500
                       ).set_title(LOCATION[sub_locality])
        figure.savefig(PLOT_DIR +"\\" + str(city) + ".svg")
        plt.close(figure)
