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

Moderni programmandi rationem habet organicam, accumsan sentientem, ut mirum inveniat. 
In hoc cursu discimus quomodo per laminis perlegere discamus quomodo programmata aedificent et 
quomodo nostra edificent. Incipiamus cum aliquibus praecipuis quaestionibus. 

## Quid computatorium ? 

Computatorium classicum est machina alicuius generis ad informationes 
puras expediendas. Varia elementa opus sunt ad hoc possibilis efficiendum, 
inter quas aliqua instrumenta initialisendi et recondendi informationes ante 
et post discursum est, et ma- china ad informationes expediendas (including casus 
ubi processus pendet ab ipsa informatione). Multae variae machinis his criteriis 
occurrere possunt, sed plerumque unam saltem exigentiam adiungimus:

## Aequationes mathematicae 

Per "Navier-Stokes" datae sunt

$$
    \\frac{D \\mathbf{u}}{Dt} -\\nabla \cdot \\eta \\left( \\nabla \mathbf{u} + 
    \\nabla \mathbf{u}^T \\right) - \\nabla p = \cdots
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

    return cfeature.NaturalEarthFeature('physcical', 'coastline', res,
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none")


def my_water_features(resolution, lakes=True, rivers=True, ocean=False):
    """Returns a [list] of cartopy features"""
    
    features = []
    
    if rivers:
        features.append(something)
        
    if lakes:
        features.append(somethingelse)

    if ocean:
        features.append(somethingelse)
    
    return features

def my_basemaps():
    """Returns a dictionary of map tile generators that cartopy can use"""
    
    ## The full list of available interfaces is found in the source code for this one:
    ## https://github.com/SciTools/cartopy/blob/master/lib/cartopy/io/img_tiles.py

    # dictionary of possible basemap tile objects
    
    mapper = {}
    
    ## Open Street map
    mapper["open_street_map"] = cimgt.OSM()

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
    
    cat = client.get_events...

    print ("Point data: {} events in catalogue".format(cat.count()))
    
    # Unpack the obspy data into a plottable array

    event_count = cat.count()

    eq_origins = np.zeros((event_count, 4))

    some_code

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
    raster_data = np.empty(datasize)

    return raster_data


def my_global_raster_data():

    raster = download_raster_data()
    
    return raster
