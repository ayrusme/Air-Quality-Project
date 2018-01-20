"""Script to render the plots from the final AQI data"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from locations import LOCATION

sns.set()

FINAL_COLUMNS = ['Stn Code', 'Year', 'Month', 'AQI']

FINAL_DF = pd.read_csv(".\\datas\\AQI_India.csv", usecols=FINAL_COLUMNS)

sub_locality_group = FINAL_DF.groupby(['Stn Code'])
sub_localities = sub_locality_group.groups.keys()

for sub_locality in sub_localities:

    sub_localities_data = sub_locality_group.get_group(sub_locality)
    sub_localities_data = sub_localities_data.drop('Stn Code', 1)

    sub_localities_data = sub_localities_data.pivot("Month", "Year", "AQI")

    location = LOCATION[sub_locality] if sub_locality in LOCATION else sub_locality

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    heatmap = sns.heatmap(sub_localities_data,
                          ax=ax,
                          vmin=0,
                          vmax=500
                         ).set_title(location)
    fig = heatmap.get_figure()
    fig.savefig(".\\output\\" + str(location) + ".svg")
