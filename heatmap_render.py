"""Script to render the heatmap from the final AQI data"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from codes import HEATMAP_COLUMNS, HEATMAP_DIR, LOCATION, PLOT_DIR

sns.set()


def render_plot():
    """
    Function to render the heatmap for the given data with
    the X axis as YEAR and Y being the Month for a location
    """

    FINAL_DF = pd.read_csv(".\\datas\\Heatmap_AQI_India.csv", usecols=HEATMAP_COLUMNS)

    city_group = FINAL_DF.groupby(['City'])
    cities = city_group.groups.keys()

    for city in cities:

        city_data = city_group.get_group(city)
        sub_locality_group = city_data.groupby(['Stn Code'])

        sub_localities = sub_locality_group.groups.keys()
        sub_localities = [locality for locality in sub_localities if locality in LOCATION]

        nrows = len(sub_localities)

        # Draw a heatmap with the numeric values in each cell
        figure, axes = plt.subplots(figsize=(8, 20),
                                    nrows=nrows,
                                    squeeze=False
                                   )

        for index, sub_locality in enumerate(sub_localities):

            sub_localities_data = sub_locality_group.get_group(sub_locality)
            sub_localities_data = sub_localities_data.drop('Stn Code', 1)

            sub_localities_data = sub_localities_data.pivot("Year", "Month", "AQI")

            sns.heatmap(sub_localities_data, ax=axes[index, 0],
                        vmin=0, vmax=500
                       ).set_title(LOCATION[sub_locality])
        plt.tight_layout()
        figure.savefig(PLOT_DIR +"\\" + HEATMAP_DIR + "\\" + str(city) + ".svg")
        plt.close(figure)
