import pytest
from src.functions import *
from src.my_functions import *

# def test_foo_function(rtol=1.e-13):
#     result = foo_function(4) - 16
#     assert result < rtol, " *** error is too big "
    
# def test_valid_resolution_output():
#     """Tests if valid_resolution() outputs "50m" when an invalid input is chosen.
#     Also tests if it outputs valid resolution "10m" if input is "10m"
    
#     """

#     this is only for my code, which is why it is commented out
    
#     result1 = valid_resolution("5")
#     result2 = valid_resolution("10m")
    
#     assert result1 == "50m", "Resolution not coerced to '50m'"
#     assert result2 == "10m", "Result coerced incorrecty"

def test_my_coastlines():
    """Tests_my_coastlines to make sure it gives a valid output with all valid inputs with no warnings or errors."""
    
    try:    
        #check if anything raises an warning which shouldnt
        with pytest.warns(None) as record:
            my_coastlines("10m")
            my_coastlines("50m")
            my_coastlines("110m")

        assert not record.list, "A warning was raised when passing a valid resolution to my_coastlines."
    
    except:
        #check if an error was raised
        assert False, "An error was raised when passing a valid resolution to my_coastlines."
    
def test_my_coastlines_warning():
    """Tests if my_coastlines gives a warning when it should.""" 
    try:
        valid_resolution("10m")
    
        with pytest.warns(UserWarning):
            my_coastlines("5")
            
    except:
        #other people wont have a "valid_resolution" function, so this test is only for my functions
        assert True
        
        
def test_my_earth_features_type():
    """tests if my_earth_features (or my_water_features for other people) doesnt throw an error and returns a list of cartopy objects"""
    
    try:
        result = my_earth_features("50m")
    except:
        result = my_water_features("50m")
        
    assert type(result[0]) == cartopy.feature.NaturalEarthFeature, "Doesnt return a cartopy feature"


def test_my_basemaps_type():
    """checks if my_basemaps() returns a cartopy image"""
    
    assert type(my_basemaps().popitem()[1]) in [cartopy.io.img_tiles.OSM, cartopy.io.img_tiles.GoogleTiles], "An element in my_basemaps dictionary is not a cartopy image" 
    
def test_my_point_data_lats_longs():
    """Tests if the first two columns of the output of my_point_data contain acceptible latitude and longitude values."""
    
    #get a small dataset that calculates relatively quickly
    test_data = my_point_data([-121, -118, 32, 35])
    
    #other people may have these in a different order to me 
    #so I just check that the first two columns contain latitudes and longitudes.
    test1 = all(-180 <= x <= 180 for x in test_data[:,0])
    test2 = all(-90 <= x <= 90 for x in test_data[:,1])
    
    assert  test1 and test2, "One of the first two columns are outside of the accptible range for latitudes and longitudes respectively."
    
    


def test_my_global_raster_data_lats_longs():
    """Tests if the first two columns of the output of my_global_raster_data contain acceptible latitude and longitude values and are not equal to 0."""
    
    all_raster_data = my_global_raster_data()
    test_data = all_raster_data[1]
    
    #other people may have these in a different order to me 
    #so I just check that the first two columns contain latitudes and longitudes.  
    test1 = all(-180 <= x <= 180 for x in test_data[:,0])
    test2 = all(-90 <= x <= 90 for x in test_data[:,1])
    test3 = not(all(x == 0 for x in test_data[:,0]))
    test4 = not(all(x == 0 for x in test_data[:,1]))
              

    assert test3 and test4, "all values in either latitude or longitude in point [1] of my_global_raster_data is 0"
    
    assert test1 and test2, "One of the first two columns are outside of the acceptible range for latitudes and longitudes respectively."
    
    
