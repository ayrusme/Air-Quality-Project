"""Script to render line charts from the final AQI data"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from codes import LINE_COLUMNS, LINE_DIR, LOCATION, PLOT_DIR

sns.set()


def render_plot():
    """
    Function to render the heatmap for the given data with
    the X axis as YEAR and Y being the Month for a location
    """

    FINAL_DF = pd.read_csv(".\\datas\\Line_AQI_India.csv", usecols=LINE_DIR)

    city_group = FINAL_DF.groupby(['City'])
    cities = city_group.groups.keys()

    for city in cities:

        city_data = city_group.get_group(city)
        sub_locality_group = city_data.groupby(['Stn Code'])

        sub_localities = sub_locality_group.groups.keys()
        sub_localities = [locality for locality in sub_localities if locality in LOCATION]
