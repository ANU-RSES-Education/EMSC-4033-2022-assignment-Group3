"""Import dependencies for this notebook"""

import matplotlib.pyplot as plt
import numpy as np

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
import warnings

from IPython.display import display_markdown
from matplotlib import cm

import cloudstor
from scipy.io import netcdf

# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import matplotlib.ticker as mticker