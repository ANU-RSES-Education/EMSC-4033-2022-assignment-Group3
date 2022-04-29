import pytest
from src.functions import *

def test_foo_function(rtol=1.e-13):
    result = foo_function(4) - 16
    assert result < rtol, " *** error is too big "