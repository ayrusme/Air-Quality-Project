"""Analysing air quality levels of India"""

import os

from codes import DIRECTORIES
import parse
import heatmap_render


#Setting up the folder structure
for directory in DIRECTORIES:
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    parse.construct_data()
    heatmap_render.render_plot()
