from .dependencies import *

def my_coastlines(resolution):
    """ returns the relevant coastlines at the requested resolution
        resolution should be one of '10m', '50m', or '110m' """
    import cartopy.feature as cfeature

    
    return cfeature.NaturalEarthFeature('physical', 'coastline', '50m',
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none")


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



def my_basemaps():
    """Returns a dictionary of map tile generators that cartopy can use"""

    mapper = {}

    mapper["basemap_name"] = cimgt.OSM()

    return mapper



def download_point_data(region):
    
    from obspy.core import event
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime

    client = Client("IRIS")

    extent = region

    starttime = UTCDateTime("1975-01-01")
    endtime   = UTCDateTime("2022-01-01")

    cat = client.get_events(starttime=starttime, endtime=endtime,
                        minlongitude=region[0],
                        maxlongitude=region[1],
                        minlatitude=region[2],
                        maxlatitude=region[3],
                        minmagnitude=5.5, catalog="ISC")
    
    
    print ("Point data: {} events in catalogue".format(cat.count()))

    event_count = cat.count()

    eq_origins = np.zeros((event_count, 5))

    for ev, event in enumerate(cat.events):
        eq_origins[ev,0] = dict(event.origins[0])['longitude']
        eq_origins[ev,1] = dict(event.origins[0])['latitude']
        eq_origins[ev,2] = dict(event.origins[0])['depth']
        eq_origins[ev,3] = dict(event.magnitudes[0])['mag']
        eq_origins[ev,4] = (dict(event.origins[0])['time']).date.year

    return eq_origins



def my_point_data(region):
    
    data = download_point_data(region)
    
    return data



def download_raster_data():
    

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


