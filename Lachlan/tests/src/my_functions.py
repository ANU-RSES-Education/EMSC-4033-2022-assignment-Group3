"""All the functions we need to make a map:

    - my_documentation()
    - my_coastlines()
    - my_water_features()
    - my_basemaps()

"""

from .dependencies import *

def my_documentation():

    markdown_documentation = """   
# Haec progressio est tabula faciens
    
## Moderni progressio programmandi 

Moderni programmandi rationem habet organicam, accumsan sentientem, ut mirum inveniat. In hoc cursu discimus quomodo per laminis perlegere discamus quomodo programmata aedificent et quomodo nostra edificent. Incipiamus cum aliquibus praecipuis quaestionibus. 

## Quid computatorium ? 

Computatorium classicum est machina alicuius generis ad informationes puras expediendas. Varia elementa opus sunt ad hoc possibilis efficiendum, inter quas aliqua instrumenta initialisendi et recondendi informationes ante et post discursum est, et ma- china ad informationes expediendas (including casus ubi processus pendet ab ipsa informatione). Multae variae machinis his criteriis occurrere possunt, sed plerumque unam saltem exigentiam adiungimus:

## Aequationes mathematicae 

Per "Navier-Stokes" datae sunt

$$
    \\frac{D \\mathbf{u}}{Dt} -\\nabla \cdot \\eta \\left( \\nabla \mathbf{u} + \\nabla \mathbf{u}^T \\right) - \\nabla p = \cdots
$$


## `Python` documentum

Python hic est aliquis codicem quem animum advertere volumus

```python

# The classic "hello world" program
print("salve mundi !")

```

"""
    
    return markdown_documentation



def my_coastlines(resolution):
    """ returns the relevant coastlines at the requested resolution """
    
    import cartopy.feature as cfeature
    

    return cfeature.NaturalEarthFeature('physical', 'coastline', resolution,
                           edgecolor=(0.0,0.0,0.0),
                           facecolor="none")


def my_water_features(resolution, lakes=True, rivers=True, ocean=False):
    """Returns a [list] of cartopy features - the ones you ask for"""
    
    features = []
    
    if rivers:
        features.append(cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', resolution,
                                        edgecolor='Blue', facecolor="none"))
        
    if lakes:
        features.append(cfeature.NaturalEarthFeature('physical', 'lakes', resolution,
                                        edgecolor="blue", facecolor="blue"))

    if ocean:
        features.append(cfeature.NaturalEarthFeature('physical', 'ocean', resolutio,
                           edgecolor="green",
                           facecolor="blue"))
    
    
    return features

def my_basemaps():
    """Returns a dictionary of map tile generators that cartopy can use"""
    
    ## The full list of available interfaces is found in the source code for this one:
    ## https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py

    # dictionary of possible basemap tile objects
    
    mapper = {}
    
    ## Continental US terrain images
    mapper["stamen_terrain"] = cimgt.Stamen('terrain-background')
    mapper["stamen_terrain_plus"] = cimgt.Stamen('terrain')
    mapper["stamen_artist"] = cimgt.Stamen('watercolor')

    ## Mapquest satellite / streetmap images 
    mapper["map_quest_aerial"] = cimgt.MapQuestOpenAerial()
    mapper["map_quest_street"] = cimgt.MapQuestOSM()

    ## Open Street map
    mapper["open_street_map"] = cimgt.OSM()

    ## Satellite Quadtree
    mapper["qtree_satellite_plus"]  = cimgt.QuadtreeTiles()


    ## Ordinance Survey (not set up)
    # ord_survey = cimgt.OrdnanceSurvey(apikey="")

    ## Azure (Not released in cartopy)
    # azure = None

    ## Mapbox Satellite images 
    
    mapper["mapbox_streets"] = cimgt.MapboxTiles(map_id='streets-v11', 
                                     access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')

    mapper["mapbox_outdoors"] = cimgt.MapboxTiles(map_id='outdoors-v11', 
                                         access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')

    mapper["mapbox_satellite"] = cimgt.MapboxTiles(map_id='satellite-v9', 
                                         access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')

    ## Google maps image tiles ()
    mapper["google_maps_street"] = cimgt.GoogleTiles(style="street") 
    mapper["google_maps_satellite"] = cimgt.GoogleTiles(style="satellite") 
    mapper["google_maps_terrain"] = cimgt.GoogleTiles(style="terrain") 

    return mapper
    
    
## specify some point data (e.g. global seismicity in this case)

def download_point_data(region):
    
    from obspy.core import event
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime

    client = Client("IRIS")

    extent = region

    starttime = UTCDateTime("1975-01-01")
    endtime   = UTCDateTime("2022-01-01")
    cat = client.get_events(starttime=starttime, endtime=endtime,
                        minlongitude=extent[0],
                        maxlongitude=extent[1],
                        minlatitude=extent[2],
                        maxlatitude=extent[3],
                        minmagnitude=4.1, catalog="ISC")

    print ("Point data: {} events in catalogue".format(cat.count()))
    
    
    # Unpack the obspy data into a plottable array

    event_count = cat.count()

    eq_origins = np.zeros((event_count, 4))

    for ev, event in enumerate(cat.events):
        eq_origins[ev,0] = dict(event.origins[0])['longitude']
        eq_origins[ev,1] = dict(event.origins[0])['latitude']
        eq_origins[ev,2] = dict(event.origins[0])['depth'] 
        eq_origins[ev,3] = dict(event.magnitudes[0])['mag'] 
        
    # scale 
    eq_origins[ev,3] = 50.0*(eq_origins[ev,3] - 4.0)


    return eq_origins


def my_point_data(region):
    
    data = download_point_data(region)
    
    return data


## - Some global raster data (lon, lat, data) global plate age, in this example


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
    teaching_data.download_file_if_distinct("global_age_data.3.6.z.npz", "global_age_data.3.6.z.npz")
    
    datasize = (1801, 3601, 3)
    age_data = np.empty(datasize)

    ages = np.load("global_age_data.3.6.z.npz")["ageData"]

    lats = np.linspace(90, -90, datasize[0])
    lons = np.linspace(-180.0,180.0, datasize[1])

    arrlons,arrlats = np.meshgrid(lons, lats)
    
    age_data[...,0] = arrlons[...]
    age_data[...,1] = arrlats[...]
    age_data[...,2] = ages[...]
     
    return age_data


def my_global_raster_data():
    
    
    raster = download_raster_data()
    
    return raster