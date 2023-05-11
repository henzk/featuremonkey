from __future__ import absolute_import
import unittest
from featuremonkey3.test.test_composer import *

def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestObjectComposition),
        unittest.TestLoader().loadTestsFromTestCase(TestClassComposition),
        unittest.TestLoader().loadTestsFromTestCase(TestModuleComposition),
    ])


def run_all():

    return unittest.TextTestRunner(verbosity=2).run(suite())


def run_in_jenkins():
    import xmlrunner
    return xmlrunner.XMLTestRunner(output='test-reports').run(suite())
