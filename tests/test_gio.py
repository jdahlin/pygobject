# -*- Mode: Python -*-

import os
import unittest

from common import gio, gobject


class TestInputStream(unittest.TestCase):
    def setUp(self):
        f = open("inputstream.txt", "w")
        f.write("testing")

        self._f = open("inputstream.txt", "r")
        self.stream = gio.unix.InputStream(self._f.fileno(), False)

    def tearDown(self):
        self._f.close()
        os.unlink("inputstream.txt")

    def testRead(self):
        self.assertEquals(self.stream.read(), "testing")

    def testReadAsync(self):
        def callback(stream, result):
            self.assertEquals(stream.read_finish(result), len("testing"))
            loop.quit()

        self.stream.read_async(10240, 0, None, callback)

        loop = gobject.MainLoop()
        loop.run()


class TestOutputStream(unittest.TestCase):
    def setUp(self):
        self._f = open("outputstream.txt", "w")
        self.stream = gio.unix.OutputStream(self._f.fileno(), False)
        self._f.flush()

    def tearDown(self):
        self._f.close()
        os.unlink("outputstream.txt")

    def testWrite(self):
        self.stream.write("testing")
        self.stream.close()
        self.failUnless(os.path.exists("outputstream.txt"))
        self.assertEquals(open("outputstream.txt").read(), "testing")
