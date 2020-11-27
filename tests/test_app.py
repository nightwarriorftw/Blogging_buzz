import unittest

from flaskblog.routes import test_urban_route

def test_test():
    assert test_urban_route() == "Works!"
