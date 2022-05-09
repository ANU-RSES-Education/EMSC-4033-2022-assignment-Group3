# +
from obspy.core import event
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

client = Client("IRIS")
    
# ?client.get_events

# -

client.get_events(
    starttime=None,
    endtime=None,
    minlatitude=None,
    maxlatitude=None,
    minlongitude=None,
    maxlongitude=None,
    latitude=None,
    longitude=None,
    minradius=None,
    maxradius=None,
    mindepth=None,
    maxdepth=None,
    minmagnitude=None,
    maxmagnitude=None,
    magnitudetype=None,
    eventtype=None,
    includeallorigins=None,
    includeallmagnitudes=None,
    includearrivals=None,
    eventid=None,
    limit=None,
    offset=None,
    orderby=None,
    catalog=None,
    contributor=None,
    updatedafter=None,
    filename=None,
)
    
    **kwargs,
)


def my_coastlines(resolution):
    """ returns the relevant coastlines at the requested resolution """

    import cartopy.feature as cfeature

    return cfeature.NaturalEarthFeature('physical', 'coastline', res,
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none")



def my_coastlines(resolution):
    """ returns the relevant coastlines at the requested resolution """

    import cartopy.feature as cfeature

    return cfeature.NaturalEarthFeature('physical', 'coastline', '110m',
                                        edgecolor=(0.0,0.0,0.0),
                                        facecolor="none")


coastline = my_coastlines("10m")
water_features = my_water_features("50m")


def my_water_features(resolution, lakes=True, rivers=True, ocean=False):
    """Returns a [list] of cartopy features"""
    
    features = []
    
    if rivers:
        features.append('rivers')
        
    if lakes:
        features.append('lakes')

    if ocean:
        features.append('ocean')
    
    return features



print(water_features)

features


def my_point_data(region):
    
    data = download_point_data(region)
    
    return data



# +
point_data = my_point_data(map_extent)

print(point_data)
# -




