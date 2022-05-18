# import pytest
# from src.functions import *

# def test_foo_function(rtol=1.e-13):
#    result = foo_function(4) - 16
#    assert result < rtol, " *** error is too big "


import pytest
#from src import my_functions
from src.functions import *


# +
def test_my_water_features():
    
    features = my_water_features(resolution = '10m')
    
    assert len(features) == 2, "only lakes and rivers whould be listed, so a list of 2 features"

#tested how many resolutions of '10m' are in the function, which should be two as only rivers and lakes are defined as True.
#test that the three features are being imput into the function and the output is lakes=True, rivers=True, ocean=False at the correct resolution


# +
def test_my_basemaps():
    
    result = my_basemaps()
    assert len(result) == 1, "mapper should return a single dictionary of map tiles for cartopy to use"
    
# Returns a dictionary of map tile generators that cartopy can use
# -



# +
def test_download_point_data(region):
    
    result = download_point_data(region)
    region = extent
    
assert  == 


# +
def test_my_coastlines():
    
    with pytest.warns(UserWarning):
    my_coastlines("5")
    
    assert 
    
# returns the relevant coastlines at the requested resolution

# +
# def test_my_point_data():
    
#     x = data 
#     y = download_point_data()
    
#     assert x == y, "data should be point data of the regions map extent"

# +
# def test_download_raster_data():
    
#     datasize = 
    
#     assert , "idk"
    
    

# test whether the raster data is being downloaded from cloudstor and that the raster data is being specified

# +
#def test_my_global_raster_data(): 
# -
# ! pytest



