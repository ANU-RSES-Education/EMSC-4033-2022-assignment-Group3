import pytest
from src.functions import *
from src.my_functions import *

def test_foo_function(rtol=1.e-13):
    result = foo_function(4) - 16
    assert result < rtol, " *** error is too big "
    
def test_my_coastlines():
    
    
    assert 