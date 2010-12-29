""" A test runner that runs all the specified modules in this directory

    This script is a replacement for something like nose tests, since I
    don't want to add another dependency to this project """

import glob
import unittest

test_pattern = glob.glob("*_test.py")
modules = [s[0:-3] for s in test_pattern]

all_test_suites = [unittest.defaultTestLoader.loadTestsFromName(t) for t in modules]
suite = unittest.TestSuite(all_test_suites)
unittest.TextTestRunner(verbosity=3).run(suite)
