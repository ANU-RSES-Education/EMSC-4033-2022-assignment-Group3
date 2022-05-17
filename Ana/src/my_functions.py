"""All the functions we need to make a map:

    - my_documentation()
    - my_coastlines()
    - my_water_features()
    - my_basemaps()

"""

from .dependencies import *

def my_documentation():

    markdown_documentation = """   

hello
"""
    
    return markdown_documentation



def my_coastlines(resolution):
    """ returns the relevant coastlines at the requested resolution """

    import cartopy.feature as cfeature

    return cfeature.NaturalEarthFeature('physical', 'coastline', resolution,
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none")


# fixed typo (physical) and changed res to resolution
# do a test for valid resolution 


def my_water_features(resolution, lakes=True, rivers=True, ocean=True):
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


# append means add to the end of the list, so added .append to features. Also changed ocean=False to ocean=True

#added import cartopy.io.img_tiles as cimgt
# copied code from notebooks - mapping 7 

# import cartopy.io.img_tiles as cimgt
# import cartopy.crs as ccrs
# from cartopy.io.img_tiles import GoogleWTS


# class MapboxTiles(GoogleWTS):
#     """
#     Implement web tile retrieval from Mapbox.
#     For terms of service, see https://www.mapbox.com/tos/.
#     """
#     def __init__(self, access_token, map_id):
#         """
#         Set up a new Mapbox tiles instance.
#         Access to Mapbox web services requires an access token and a map ID.
#         See https://www.mapbox.com/api-documentation/ for details.
#         Parameters
#         ----------
#         access_token
#             A valid Mapbox API access token.
#         map_id
#             An ID for a publicly accessible map (provided by Mapbox).
#             This is the map whose tiles will be retrieved through this process.
#         """
#         self.access_token = access_token
#         self.map_id = map_id
#         super().__init__()
        

#     def _image_url(self, tile):
#         x, y, z = tile
#         url = ('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}'
#                '?access_token={token}'.format(z=z, y=y, x=x,
#                                               id=self.map_id,
#                                               token=self.access_token))
#         return url

# mapbox_outdoors = MapboxTiles(map_id='mapbox/outdoors-v11', 
#                                      access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')

# basemap_name = mapbox_outdoors

def my_basemaps():
#     """Returns a dictionary of map tile generators that cartopy can use"""
    
    ## The full list of available interfaces is found in the source code for this one:
    ## https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py

    # dictionary of possible basemap tile objects
    
    
    mapper = {}
    
    ## Open Street map
    mapper["open_street_map"] = cimgt.OSM()
    # mapper["mapbox_outdoors"] = cimgt.MapboxTiles(map_id='outdoors-v11', access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')

    return mapper




# mapbox_outdoors = MapboxTiles(map_id='mapbox/outdoors-v11', 
#                                      access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')





# # specify some point data (e.g. global seismicity in this case)

def download_point_data(region):
    #looked up ?get_events and got the list i need to add, added that to the doc, found the 
    
    from obspy.core import event
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime

    client = Client("IRIS")
    
    extent = region

    starttime = UTCDateTime("1975-01-01")
    endtime   = UTCDateTime("2022-01-01")
    
    # cat = client.get_events(starttime=None,endtime=None,minlatitude=None,maxlatitude=None,minlongitude=None,maxlongitude=None,latitude=None,longitude=None,minradius=None,maxradius=None,mindepth=None,maxdepth=None,minmagnitude=None,maxmagnitude=None,magnitudetype=None,eventtype=None,includeallorigins=None,includeallmagnitudes=None,includearrivals=None,eventid=None,limit=None,offset=None,orderby=None,catalog=None,contributor=None,updatedafter=None,filename=None,**kwargs,)
    
    cat = client.get_events(starttime=starttime, 
                            endtime=endtime,
                            minlongitude=extent[0],
                            maxlongitude=extent[1],
                            minlatitude=extent[2],
                            maxlatitude=extent[3],
                            minmagnitude=5, catalog="ISC")

    print (cat.count(), " events in catalogue")

# lat0 =  30  ; lat1 = 40
# lon0 =  -123; lon1 = -113
# left min magnitude as 5.5


    print ("Point data: {} events in catalogue".format(cat.count()))
    
    # Unpack the obspy data into a plottable array

    event_count = cat.count()

    eq_origins = np.zeros((event_count, 4))
    
 # I have copied the code from himalaya 

    for ev, event in enumerate(cat.events):
        eq_origins[ev,0] = dict(event.origins[0])['longitude']
        eq_origins[ev,1] = dict(event.origins[0])['latitude']
        eq_origins[ev,2] = dict(event.origins[0])['depth']
        eq_origins[ev,3] = dict(event.magnitudes[0])['mag']
        #eq_origins[ev,4] = (dict(event.origins[0])['time']).date.year

    return eq_origins


def my_point_data(region):
    
    data = download_point_data(region)
    
    return data


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

    datasize = (1801, 3601, 3)
    raster_data = np.empty(datasize)
    
    
    ages = np.load("Resources/global_age_data.3.6.z.npz")["ageData"]

    lats = np.linspace(90, -90, datasize[0])
    lons = np.linspace(-180.0,180.0, datasize[1])

    arrlons,arrlats = np.meshgrid(lons, lats)

    raster_data[...,0] = arrlons[...]
    raster_data[...,1] = arrlats[...]
    raster_data[...,2] = ages[...]

    return raster_data


def my_global_raster_data():

    raster = download_raster_data()
    
    return raster






