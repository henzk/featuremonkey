from __future__ import absolute_import
import unittest
from featuremonkey.test.composer import *

def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestObjectComposition),
        unittest.TestLoader().loadTestsFromTestCase(TestClassComposition),
        unittest.TestLoader().loadTestsFromTestCase(TestModuleComposition),
    ])


def run_all():

    return unittest.TextTestRunner(verbosity=2).run(suite())
