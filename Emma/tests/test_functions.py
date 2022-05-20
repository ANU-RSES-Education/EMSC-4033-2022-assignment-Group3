import pytest
#from src import my_functions
from src.functions import *


def test_my_water_features():

    features = my_water_features(resolution = '10m')
    assert len(features) == 2, "only lakes and rivers whould be listed, so a list of 2 features"

    #tested how many resolutions of '10m' are in the function, which should be two as only rivers and lakes are defined as True. #test that the three features are being imput into the function and the output is lakes=True, rivers=True, ocean=False at the correct resolution


def test_my_basemaps():

    result = my_basemaps()
    assert len(result) == 1, "mapper should return a single dictionary of map tiles for cartopy to use"
    # Returns a dictionary of map tile generators that cartopy can use


# region
def test_my_coastlines():

    result = my_coastlines(resolution = '50m')
    assert type(result) != None, "result should be an cartopy object"

#"type = {}".format(type(result))
#returns the relevant coastlines at the requested resolution
# endregion


def test_download_point_data():
    
    result = download_point_data(region)
    assert type(result) == numpy.ndarray


# region
def test_download_raster_data():
    
    result = download_raster_data()
    assert result.shape == (1801, 3601, 3)

# test whether the raster data is being downloaded from cloudstor and that the raster data is being specified

# endregion


# region
# def test_download_raster_data():
    
#     result_lats = download_raster_data(x = [1])
#     assert result_lat == all(-90 <= x <= 90, [1])

    """ I was trying to make the test specific to spatial points in the array, such as testing whether 
    the second coloumn (latitude) is within the boundaries of -90 to 90. I couldn't get it to work"""
# endregion
