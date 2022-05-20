import pytest
from src.functions import *
from src.my_functions import *

def test_foo_function(rtol=1.e-13):
    result = foo_function(4) - 16
    assert result < rtol, " *** error is too big "

def test_my_coastlines():
    """Check if my_coastlines resolution is valid"""
    resolution = my_coastlines('10m')
    assert my_coastlines('10m') != resolution, " Coastline resolution error"
    

def test_my_water_features_type():
    """Tests my_water_features to see if it a list of cartopy objects"""
    test = my_water_features("10m")
    assert type(test[0]) == cartopy.feature.NaturalEarthFeature, "No list of cartopy features found"
    
    
def test_my_basemaps():
    """Checks if my_basemaps contains cartopy images"""
    assert len(my_basemaps()) != 1, "Basemaps returns single entry" # in [cartopy.io.img_tiles.OSM], "Error with image" 
    
def test_download_point_data():
    """Checks if lon-lat values are valid"""
    #Test dataset
    lonlat = download_point_data([0, 10, 0, 10])
    lon = all(-180 <= x <= 180 for x in lonlat[:,0])
    lat = all(-90 <= x <= 90 for x in lonlat[:,1])
    assert  lon and lat, "Invalid input for either Longitude or Latitude"
    
    
def test_my_global_raster_data():
    """Checks if raster data is downloaded and valid"""
    raster = my_global_raster_data()
    lonlat = raster[1]
    #Check Longitude and Latitude are valid
    lon = all(-180 <= x <= 180 for x in lonlat[:,0])
    lat = all(-90 <= x <= 90 for x in lonlat[:,1])
    #Check raster_data is not empty
    empty_lon = not(all(x == 0 for x in lonlat[:,0]))
    empty_lat = not(all(x == 0 for x in lonlat[:,1]))
    assert lon and lat, "Invalid input for either Longitude or Latitude"
    assert empty_lon and empty_lat, "There are no input values for Longitude and Latitude"
