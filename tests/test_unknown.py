# -*- Mode: Python -*-

import unittest

from gi.repository import GObject
try:
    import testhelper
except ImportError:
    testhelper = None


TestInterface = GObject.GType.from_name('TestInterface')


class TestUnknown(unittest.TestCase):
    def testFoo(self):
        obj = testhelper.get_unknown()
        TestUnknownGType = GObject.GType.from_name('TestUnknown')
        TestUnknown = GObject.new(TestUnknownGType).__class__
        assert isinstance(obj, testhelper.Interface)
        assert isinstance(obj, TestUnknown)
