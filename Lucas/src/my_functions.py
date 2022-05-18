"""All the functions we need to make a map:

    - my_documentation()
    - my_coastlines()
    - my_water_features()
    - my_basemaps()

"""

from .dependencies import *

def my_documentation():

    markdown_documentation = """   
# Earthquake Depth and Magnitude Map Maker

This notebook allows you to plot earthquakes which occurred between 1975 and 2022 on a map of a selected region.
    
## Parameters

To create a map of a region, you must first select parameters for mapping;

Use these to define the region of the map
-min_latitude  
-max_latitude  
-min_longitude  
-max_longitude  

Decide what magnitude earthquake you want as a minimum. Note; there are a lot of low magnitude earthquakes.
-minimum_magnitude  

Decide on a resolution for map features. Must be one of "10m", "50m" or "110m".
-water_features_resolution  
-coastline_resolution  


"""
    
    return markdown_documentation


def valid_resolution(resolution):
    """Checks if an input resolution is valid.
    Valid resolutions are '10m','50m', & '110m'. 
    Any other input will be set to "50m" and a warning will be issued."""
    
    valid_resolutions = ['10m','50m','110m']
    
    if resolution in valid_resolutions:
        return(resolution)
    
    else:
        #if resolution is invalid, we return "50m" and issue a warning
        warnings.warn("""Invalid resolution. Valid resolutions are "10m","50m", & "110m". 
        Resolution has been set to "50m". """, UserWarning)
        return('50m')



def my_coastlines(resolution = "50m"):
    """ Returns the relevant coastlines at the requested resolution.
    Valid resolutions are "10m","50m", & "110m". Any other input will be set to "50m"."""
    
    #check if resolution is valid and return "50m" if invalid.
    res = valid_resolution(resolution)

    return cfeature.NaturalEarthFeature('physical', 'coastline', res,
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none")

def my_earth_features(resolution = "50m", features = ['lakes','rivers_lake_centerlines']):
    """Returns a [list] of cartopy natural earth physical features at the given resolution. 
    Valid resolutions are "10m","50m", & "110m". Any other input will be set to "50m".
    Valid physical features are from https://www.naturalearthdata.com/features/"""
    
    
    #these are the valid natural earth physical features
    valid_features = ['coastline','land', 'ocean',    
                      'minor_islands','reefs','physical_region_features',
                      'rivers_lake_centerlines','lakes','glaciated_areas','antarctic_ice_shelves',
                      'bathymetry','geographic_lines','graticules']
                      
                      
    #check if resolution is valid and return "50m" if invalid.
    res = valid_resolution(resolution)
        
    cartopy_features = []
    
    for feature in features:
        if feature in valid_features:
            cartopy_features.append(cfeature.NaturalEarthFeature('physical', feature, res,
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none"))
    
    return cartopy_features

def my_basemaps():
    """Returns a dictionary of map tile generators that cartopy can use."""
    
    ## The full list of available interfaces is found in the source code for this one:
    ## https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py

    # dictionary of possible basemap tile objects
    
    mapper = {}
    
    ## Open Street map
    mapper["open_street_map"] = cimgt.OSM()

    return mapper


## specify some point data (e.g. global seismicity in this case)

def download_point_data(region, min_magnitude):
    """
    Returns array of earthquake location (lat/long), magnitude and date from earthquakes in the given region between 1975 and 2022.
    Region is of the form [min longitude, max longitude, min latitude, max latitude].
    Earthquaked below min_magnitude are not returned.
    """
    
    from obspy.core import event
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime

    client = Client("IRIS")

    starttime = UTCDateTime("1975-01-01")
    endtime   = UTCDateTime("2022-01-01")
    
    cat = client.get_events(starttime, endtime,
                            minlongitude = region[0], maxlongitude = region[1],
                            minlatitude  = region[2], maxlatitude  = region[3],
                            catalog = "ISC", minmagnitude = min_magnitude)

    print ("Point data: {} events in catalogue".format(cat.count()))

    # Initialise an array of zeros of the same size as the data we want to return
    event_count = cat.count()
    eq_origins = np.zeros((event_count, 4))

    # Unpack the obspy data into a plottable array
    # We want lat, long, magnitude and depth.
    for event, earthquake in enumerate(cat.events):
        
        eq_origins[event,0] = dict(earthquake.origins[0])['longitude']
        eq_origins[event,1] = dict(earthquake.origins[0])['latitude']
        eq_origins[event,2] = dict(earthquake.magnitudes[0])['mag']
        eq_origins[event,3] = dict(earthquake.origins[0])['depth']

        
        #eq_origins[event,4] = (dict(earthquake.origins[0])['time']).date.year #dont really need time

    return eq_origins


def my_point_data(region, min_magnitude = 5.5):
    """
    Returns an array of earthquake location (lat/long), magnitude and date from earthquakes in the given region between 1975 and 2022.
    Region is of the form [min longitude, max longitude, min latitude, max latitude].
    Earthquakes with magnitude below min_magnitude are not returned.
    """
    
    data = download_point_data(region, min_magnitude)
    
    return data


## - Some global raster data (lon, lat, data) global plate age, in this example

def download_raster_data():
    """Gets raster seafloor age data from cloudstore. Returns an array with lats, longs and ages for each point."""
    
    # Seafloor age data and global image - data from Earthbyters

    # The data come as ascii lon / lat / age tuples with NaN for no data. 
    # This can be loaded with ...

    # age = numpy.loadtxt("Resources/global_age_data.3.6.xyz")
    # age_data = age.reshape(1801,3601,3)  # I looked at the data and figured out what numbers to use
    # age_img  = age_data[:,:,2]

    # But this is super slow, so I have just stored the Age data on the grid (1801 x 3601) which we can reconstruct easily

    from cloudstor import cloudstor
    teaching_data = cloudstor(url="L93TxcmtLQzcfbk", password='')
    teaching_data.download_file_if_distinct("global_age_data.3.6.z.npz", "global_age_data.3.6.z.npz")

    ages = np.load("global_age_data.3.6.z.npz")["ageData"]    
    
    datasize = (1801, 3601, 3)
    age_data = np.empty(datasize)
    
    lats = np.linspace(90, -90, datasize[0])
    lons = np.linspace(-180.0,180.0, datasize[1])

    arrlons,arrlats = np.meshgrid(lons, lats)

    age_data[...,0] = arrlons[...]
    age_data[...,1] = arrlats[...]
    age_data[...,2] = ages[...]
    

    return age_data


def my_global_raster_data():
    """Gets raster seafloor age data from cloudstore. Returns an array with lats, longs and ages for each point."""
        
    raster = download_raster_data()
    
    
    return raster
