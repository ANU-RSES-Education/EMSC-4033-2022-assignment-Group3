"""All the functions we need to make a map:

    - my_documentation()
    - my_coastlines()
    - my_water_features()
    - my_basemaps()

"""

from .dependencies import *

def my_documentation():

    markdown_documentation = """   
This purpose of this Notebook is to provide the commands and functions needed for Map Maker to run and produce 
a base-map for the LA Basin with super-imposed data based on sea-floor age and seismic data in the region. Topography has been specified by point data; to indicate regions as lakes, rivers, and oceans.
"""
    
    return markdown_documentation



def my_coastlines(resolution):
    """ returns the relevant coastlines at the requested resolution
        resolution should be one of '10m', '50m', or '110m' """
    import cartopy.feature as cfeature

# "Features" such as land, ocean, coastlines (50m =  the 1:50 million scale)

    return cfeature.NaturalEarthFeature('physical', 'coastline', '50m',
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none")


    """fixed typo 'physical' and added resolution of 50m to c.feature.NaturalEarthFeature set """

def my_water_features(resolution, lakes=True, rivers=True, ocean=False):
    """Returns a [list] of cartopy features"""
    
    features = []
    
    if rivers:
        features.append(cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m',
                                        edgecolor='Blue', facecolor="none"))
        
    if lakes:
        features.append(cfeature.NaturalEarthFeature('physical', 'lakes', '10m',
                                        edgecolor="blue", facecolor="blue"))

    if ocean:
        features.append(cfeature.NaturalEarthFeature('physical', 'ocean', '10m',
                           edgecolor="green",
                           facecolor="blue"))
    
    return features

    """ append adds to the end of the list, defined the features in water_features
    ocean=False to remove the oceans from being read/displayed in the maps
    added cfeature.NaturalEarthFeature specifications to each water body feature """

def my_basemaps():
    """Returns a dictionary of map tile generators that cartopy can use"""
    
    ## The full list of available interfaces is found in the source code for this one:
    ## https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py

    # dictionary of possible basemap tile objects

    mapper = {}

#     ## Mapquest satellite / streetmap images 
#     mapbox_outdoors = cimgt.MapQuestOSM()

    ## Open Street map
    mapper["basemap_name"] = cimgt.OSM()

    #changed to "basemap_name" in my_functions and in MapMaker.ipynb


#     ## Mapbox Satellite images 

#     mapbox_satellite = cimgt.MapboxTiles(map_id='satellite', access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')

#     ## Google maps image tiles ()
#     google_maps_street = cimgt.GoogleTiles(style="street") 
#     google_maps_satellite = cimgt.GoogleTiles(style="satellite") 
#     google_maps_terrain = cimgt.GoogleTiles(style="terrain") 

#     ax.add_image(map_tiles, 11)
#     ax.add_feature(coastline, linewidth=1.5,  edgecolor="Black", zorder=1, alpha=0.5)
#     ax.add_feature(rivers,    linewidth=1.0,  edgecolor="Blue",  zorder=2, alpha=0.5)

    return mapper


# # specify some point data (e.g. global seismicity in this case)

def download_point_data(region):
    
    from obspy.core import event
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime

    client = Client("IRIS")

    extent = region

    """region is defined in MapMaker as the map_extent? The code for cat=... did not work with map_extent,    
    however, is working with region. Maybe check if the postions in region (i.e. region[x]) allign with the 
    map_extent long and lats. """

    starttime = UTCDateTime("1975-01-01")
    endtime   = UTCDateTime("2022-01-01")

    cat = client.get_events(starttime=starttime, endtime=endtime,
                        minlongitude=region[0],
                        maxlongitude=region[1],
                        minlatitude=region[2],
                        maxlatitude=region[3],
                        minmagnitude=5.5, catalog="ISC")
    
    """ Defined the starttime and endtime as marked above, defined max and min longitude and latitude as the 
    map_extent (defined by region), and made the catalog "ISC". Not sure what the minmagnitude is meant to be so 
    I have left it at 5.5 """    


    print ("Point data: {} events in catalogue".format(cat.count()))


    # Unpack the obspy data into a plottable array

    event_count = cat.count()

    eq_origins = np.zeros((event_count, 5))

    for ev, event in enumerate(cat.events):
        eq_origins[ev,0] = dict(event.origins[0])['longitude']
        eq_origins[ev,1] = dict(event.origins[0])['latitude']
        eq_origins[ev,2] = dict(event.origins[0])['depth']
        eq_origins[ev,3] = dict(event.magnitudes[0])['mag']
        eq_origins[ev,4] = (dict(event.origins[0])['time']).date.year

    """changed the event_count from 4 to 5, however if it is meant to be 4 I am not sure if something needs to 
     be removed, or if it's accounting for the last event labelled as '4'. Also added in some_code for the event 
     specifications for lat, long, depth, mag and time """

    return eq_origins


def my_point_data(region):
    
    data = download_point_data(region)
    
    return data

# global_extent     = [-180.0, 180.0, -90.0, 90.0]
# # - Some global raster data (lon, lat, data) global plate age, in this example

def download_raster_data():
    
    # Seafloor age data and global image - data from Earthbyters

    # The data come as ascii lon / lat / age tuples with NaN for no data. 
    # This can be loaded with ...

    # age = numpy.loadtxt("Resources/global_age_data.3.6.xyz")
    # age_data = age.reshape(1801,3601,3)  # I looked at the data and figured out what numbers to use
    # age_img  = age_data[:,:,2]

    # But this is super slow, so I have just stored the Age data on the grid (1801 x 3601) which we can reconstruct easily

    from cloudstor import cloudstor
    teaching_data = cloudstor(url="L93TxcmtLQzcfbk", password='')
    teaching_data.download_file_if_distinct("global_age_data.3.6.z.npz", "Resources/global_age_data.3.6.z.npz")

# added "Resources" to the teaching_data to match below in ages
    datasize = (1801, 3601, 3)
    raster_data = np.empty(datasize)

    ages = np.load("Resources/global_age_data.3.6.z.npz")["ageData"]

    lats = np.linspace(90, -90, datasize[0])
    lons = np.linspace(-180.0,180.0, datasize[1])

    arrlons,arrlats = np.meshgrid(lons, lats)

    raster_data[...,0] = arrlons[...]
    raster_data[...,1] = arrlats[...]
    raster_data[...,2] = ages[...]

    """ added in specifications for age data (i.e. raster_data): ages, lats, lons, meshgrid """

    return raster_data


def my_global_raster_data():

    raster = download_raster_data()
    
    return raster

