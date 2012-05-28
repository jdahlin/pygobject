# -*- Mode: Python -*-

import unittest

from gi.repository import GObject
try:
    import testhelper
except ImportError:
    testhelper = None


GUnknown = GObject.type_from_name("TestUnknown")
Unknown = GUnknown.pytype


class TestIfaceImpl(unittest.TestCase):

    def testReImplementInterface(self):
        class MyUnknown(Unknown, testhelper.Interface):
            some_property = GObject.Property(type=str)

            def __init__(self):
                Unknown.__init__(self)
                self.called = False

            def do_iface_method(self):
                self.called = True
                Unknown.do_iface_method(self)
        GObject.type_register(MyUnknown)

        m = MyUnknown()
        m.iface_method()
        self.assertEqual(m.called, True)

    def testImplementInterface(self):
        class MyObject(GObject.GObject, testhelper.Interface):
            some_property = GObject.Property(type=str)

            def __init__(self):
                GObject.GObject.__init__(self)
                self.called = False

            def do_iface_method(self):
                self.called = True
        GObject.type_register(MyObject)
        m = MyObject()
        m.iface_method()
        self.assertEqual(m.called, True)
