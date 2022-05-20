import pytest
from src.my_functions import *


# **Tests for my_documentation**

# +
# def test_my_documentation_keyword():
#     """Test whether documentation is the correct one by searching for a keyword"""
#     documentation = my_documentation()
#     assert "map" in documentation, "Failed to return the correct documentation"
# -

def test_my_documentation_is_string():
    """Tests whether the function we are calling is a string"""
    documentation = type(my_documentation())
    assert documentation == str, "this function is not a string"


# **Tests for my_coastlines**

def test_my_coastlines():
    """Tests whether the feature we are calling has the correct type"""
    feature = my_coastlines("50m")
    assert type(feature) == cfeature.NaturalEarthFeature, "The cartopy feature is not returned"


# **Tests for my_water_features**

def test_my_water_features():
    """checks the length of "my_water_features" function to check if all three features are present"""
    features_length = len(my_water_features("10m"))
    assert features_length == 2, "Not all features are displayed"


def test_my_water_features_is_list():
    """Tests whether the function we are calling is a list"""
    features_type = type(my_water_features("10m"))
    assert features_type == list, "this function is not a list"


def test_my_water_features_type():
    """Tests whether the features we are calling have the correct type"""
    features = my_water_features("10m")
    assert type(features[0]) == cfeature.NaturalEarthFeature, "The cartopy feature 'rivers' is not contained"
    assert type(features[1]) == cfeature.NaturalEarthFeature, "The cartopy feature 'lakes' is not contained"
    # assert type(features[2]) == cfeature.NaturalEarthFeature, "The cartopy feature 'oceans' is not contained"


# **Tests for my_basemaps**

def test_my_basemaps_has_map():
    """Tests whether the map we want is contained within the dictionary"""
    mapper = my_basemaps() 
    assert "open_street_map" in mapper, "map is not contained within dictionary"


def test_my_basemaps_is_dictionary():
    """Tests whether the function we are calling is a dictionary"""
    mapper = my_basemaps() 
    assert type(mapper) == dict, "this function is not a dictionary"


def test_my_basemaps_length():
    """checks the length of "my_basemaps" function to check if all maps are contained"""
    mapper_length = len(my_basemaps()) 
    assert mapper_length == 7, "not all basemap types are contained within dictionary"


# **Tests for my_point_data**

def test_my_point_data():
    """Testing whether the coordinates of seismic events we have are within the extent of the map"""
    map_extent = [-123, -113, 30, 40]
    point_data = download_point_data(map_extent)
    for ev in range(len(point_data)):
        assert map_extent[0] <= point_data[ev][0] <= map_extent[1],  "longitude of seimsic event is out of the map extent"
        assert map_extent[2] <= point_data[ev][1] <= map_extent[3],  "latitude of seimsic event is out of the map extent"


# **Tests for download_raster_data**

def test_download_raster_data():
    """tests whether the shape of the raster data matches our array""" 
    raster_data = download_raster_data() 
    assert raster_data.shape == (1801, 3601, 3), " raster data for seafloor age does not have the right size"

# !pytest
