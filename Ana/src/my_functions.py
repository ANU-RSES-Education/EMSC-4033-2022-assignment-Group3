"""

##Introduction to my_functions.py

Welcome to my_functions.py! This module contains the functions that are needed to run MapMaker.ipyn - a notebook for easily creating maps from structured tabular data. This notebook makes use of the Python cartopy package, which is designed for easy data analysis and visualisation.

def + The function name goes here ():
    " This is a docstring"
    The code goes here # This is a comment

The comment here will help us understand and edit the code, while docstrings will be helpful in explaining what the function does.

Additionally, docstrings are formatted in the following way: 

Description of the function 

Parameters
----------
     The variables listed inside the parentheses in the function definition

Returns
-------
    This is a description of what is returned.


Finally, here is all the functions we need to make a map:

    - my_documentation()
    - my_coastlines()
    - my_water_features()
    - my_basemaps()
    - my_point_data()
    - my_global_raster_data()
    
"""

from .dependencies import *

def my_documentation():
    """This function returns a text that describes the purpose of this notebook, and instructions on how to use it
    Parameters
----------
     none

Returns
-------
    markdown_documentation (string):  """   


    markdown_documentation = """   

##Introduction to MapMaker.ipyn

Welcome to MapMaker.ipyn - a seismic event map generator! Currently, this notebook can be run to display the locations of earthquakes that occured from 1975-2022 in the California region, but can be easily modified: you can define the temporal and spatial scales of interest, as well as the geographical projection and the resolution of geographic features displayed on the map, in addition to the magnitude of seismic events. Instructions on how to modify this map are contained within my_functions.py.
"""    
    return markdown_documentation



def my_coastlines(resolution):
    """ This function returns the relevant coastlines at the requested resolution. 

    Parameters
    ----------
    resolution (string) : the scale of the coastlines displayed on the map, which should be one of '10m', '50m', or '110m'.
    The resolution can be defined in MapMaker.ipyn, i.e. when calling my_coastlines("10m")

    Returns
    -------
    The cartopy feature for coastlines at the requested resolution 
    """

    import cartopy.feature as cfeature

    return cfeature.NaturalEarthFeature('physical', 'coastline', resolution,
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none") 


def my_water_features(resolution, lakes=True, rivers=True, ocean=True):
    """This function returns a [list] of cartopy features(lakes, rivers and oceans) at the requested resolution
    
    Parameters
    ----------
    - Paremeter (1) - resolution (string) : the scale of the features displayed on the map, which should be one of '10m', '50m', or '110m'.
    The resolution can be defined in MapMaker.ipyn, i.e. when calling my_water_features("50m")
    - Paremeters (2) (3) (4) - relevant features, which must be called by name=True

    Returns
    -------
    features (list) : A list of the cartopy features for lakes, rivers and oceans.
    """
    
    features = [] # creates an empty list. 
    
    if rivers:
        features.append(cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m',
                                        edgecolor='Blue', facecolor="none"))
        
        # .append adds each feature to the "features" list defined above that can be called if True.
        
    if lakes:
        features.append(cfeature.NaturalEarthFeature('physical', 'lakes', '10m',
                                        edgecolor="blue", facecolor="blue"))

    if ocean:
        features.append(cfeature.NaturalEarthFeature('physical', 'ocean', '10m',
                           edgecolor="green",
                           facecolor="blue"))
    
    return features



def my_basemaps():
    """Returns a dictionary of map tile generators that cartopy can use.
    The full list of available interfaces is found in the source code for this one:
    https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py
    
    Parameters
    ----------
     none

    Returns
    -------
    mapper (dict): dictionary of possible basemap tile objects - projection for the map.
    Only one in this instance: "open_street_map"
    
    """
    
    mapper = {} # empty dictionary of possible basemap tile objects

    mapper["open_street_map"] = cimgt.OSM() ## Adding Open Street map to the dictionary above

    return mapper



# # specify some point data (e.g. global seismicity in this case)

def download_point_data(region):
    """downloads and creates an array for the point data - these are the seismic events.
    
    Parameters
    ----------
     region (list): a list that contains the co-ordinates for the extent of the map. This can be defined in MapMaker.ipyn, i.e. when calling map_extent = [lon0, lon1, lat0, lat1].

    Returns
    -------
    eq_origins (numpy array) : contains the latitude, longitude, depth and magnitude of the earthquakes
    
    """
    
    from obspy.core import event
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime

    client = Client("IRIS")
    
    extent = region

    # Define the temporal scale which should be altered here
    
    starttime = UTCDateTime("1975-01-01") 
    endtime   = UTCDateTime("2022-01-01") 
    
    # Download data relevant to the spatial scale which can be altered in MapMaker.ipyn

    cat = client.get_events(starttime=starttime, 
                            endtime=endtime,
                            minlongitude=extent[0],
                            maxlongitude=extent[1],
                            minlatitude=extent[2],
                            maxlatitude=extent[3],
                            minmagnitude=5, catalog="ISC") #You can change the minimum magnitude of the seismic events here! i.e. minmagnitude=4
    
    #Two ways of counting seimsic events

    print (cat.count(), " events in catalogue") 

    print ("Point data: {} events in catalogue".format(cat.count())) 
    
    # Unpack the obspy data into a plottable array

    event_count = cat.count()

    # Setting up the array 
    
    eq_origins = np.zeros((event_count, 4))
    
    # Store information for longitude, latitude, depth and magnitude from point_data

    for ev, event in enumerate(cat.events):
        eq_origins[ev,0] = dict(event.origins[0])['longitude']
        eq_origins[ev,1] = dict(event.origins[0])['latitude']
        eq_origins[ev,2] = dict(event.origins[0])['depth']
        eq_origins[ev,3] = dict(event.magnitudes[0])['mag']

    return eq_origins



def my_point_data(region):
    """Renames the data downloaded in download_point_data
    
    Parameters
    ----------
     region (list): a list that contains the co-ordinates for the extent of the map. This can be defined in MapMaker.ipyn, i.e. when calling map_extent = [lon0, lon1, lat0, lat1].

    Returns
    -------
    data (numpy array) : contains the latitude, longitude, depth and magnitude of the earthquake
    
    """
    
    data = download_point_data(region)
    
    return data



# - Some global raster data (lon, lat, data) global plate age, in this example

def download_raster_data():
    
    """downloads and creates an array for the raster data - these are Seafloor age data and global image (data from Earthbyters). The data is then reformatted to fit to a latitude and longitude grid. 
    
    Parameters
    ----------
     none

    Returns
    -------
    raster_data (numpy array) : contains the latitude, longitude and age of the sea floor. 
    """
   
    # The data come as ascii lon / lat / age tuples with NaN for no data. 
    # This can be loaded with ...
    # age = numpy.loadtxt("Resources/global_age_data.3.6.xyz")
    # age_data = age.reshape(1801,3601,3)  # I looked at the data and figured out what numbers to use
    # age_img  = age_data[:,:,2]

    # But this is super slow, so I have just stored the Age data on the grid (1801 x 3601) which we can reconstruct easily

    # Import data 
    from cloudstor import cloudstor
    teaching_data = cloudstor(url="L93TxcmtLQzcfbk", password='')
    teaching_data.download_file_if_distinct("global_age_data.3.6.z.npz", "Resources/global_age_data.3.6.z.npz")

   # Create array

    datasize = (1801, 3601, 3)
    raster_data = np.empty(datasize)
    
    #Fit to a latitude and longitude grid. 
    
    ages = np.load("Resources/global_age_data.3.6.z.npz")["ageData"]
    
    lats = np.linspace(90, -90, datasize[0])
    lons = np.linspace(-180.0,180.0, datasize[1])

    arrlons,arrlats = np.meshgrid(lons, lats)

    raster_data[...,0] = arrlons[...]
    raster_data[...,1] = arrlats[...]
    raster_data[...,2] = ages[...]

    return raster_data


def my_global_raster_data():
    
    """Renames the data downloaded in download_raster_data
    
    Parameters
    ----------
     none

    Returns
    -------
    raster (numpy array) : contains the latitude, longitude and age of the sea floor. 
    
    """

    raster = download_raster_data()
    
    return raster


