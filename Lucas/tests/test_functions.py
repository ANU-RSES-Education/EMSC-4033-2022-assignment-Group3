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

        assert not record.list, "A warning was raised."
    
    except:
        #check if an error is raised
        assert False, "An error was raised."
    
def test_my_coastlines_warning():
    """Tests if my_coastlines gives a warning when it should.""" 
    with pytest.warns(UserWarning):
        my_coastlines("5")

