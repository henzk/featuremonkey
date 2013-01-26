from __future__ import absolute_import
from featuremonkey import compose, compose_later
from featuremonkey.test.mock import composer_mocks as mocks
from featuremonkey.test.mock import testmodule1, testpackage1
import unittest
import sys

try:
    #python3
    from imp import reload
except ImportError:
    #python2
    pass

class TestObjectComposition(unittest.TestCase):

    def setUp(self):
        pass

    def test_noparam(self):
        self.assertRaises(Exception, compose)

    def test_singleparam(self):
        self.assertEquals(self, compose(self))

    def test_idendity(self):
        instance = mocks.Base()
        composition = compose(mocks.MemberIntroduction(), instance)
        self.assertEquals(instance, composition)

    def test_member_introduction(self):
        instance = mocks.Base()
        composition = compose(mocks.MemberIntroduction(), instance)
        self.assertEquals(8, composition.base_prop)
        self.assertEquals(1, composition.a)

    def test_existing_member_introduction(self):
        instance = mocks.Base()
        self.assertRaises(Exception, compose, mocks.ExistingMemberIntroduction(), instance)

    def test_method_introduction(self):
        instance = mocks.Base()
        composition = compose(mocks.MethodIntroduction(), instance)
        self.assertEquals(8, composition.base_prop)
        self.assertTrue(composition.method())

    def test_method_refinement(self):
        instance = mocks.Base()
        composition = compose(mocks.MethodRefinement(), instance)
        self.assertEquals('Hellorefined', composition.base_method('Hello'))


class TestClassComposition(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        reload(mocks)

    def test_idendity(self):
        clss = mocks.Base
        composition = compose(mocks.MemberIntroduction, clss)
        self.assertEquals(clss, composition)

    def test_member_introduction(self):
        compose(mocks.MemberIntroduction, mocks.Base)
        self.assertEquals(8, mocks.Base.base_prop)
        self.assertEquals(1, mocks.Base.a)

    def test_existing_member_introduction(self):
        self.assertRaises(Exception, compose, mocks.ExistingMemberIntroduction, mocks.Base)

    def test_method_introduction(self):
        compose(mocks.MethodIntroduction(), mocks.Base)
        self.assertEquals(8, mocks.Base.base_prop)
        self.assertTrue(mocks.Base().method())

    def test_method_refinement(self):
        compose(mocks.MethodRefinement2(), mocks.Base)
        self.assertEquals('Hellorefined', mocks.Base().base_method('Hello'))

class TestModuleComposition(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if hasattr(testmodule1, 'module_introduction'):
            del testmodule1.module_introduction
        reload(testmodule1)
        reload(testpackage1)

    def test_reloading_clears_composition(self):

        self.assertEquals(False, hasattr(testmodule1, 'module_introduction'))

    def test_member_introduction(self):

        class ModuleIntroduction(object):

            introduce_module_introduction = 478

        compose(ModuleIntroduction(), testmodule1)
        self.assertEquals(True, hasattr(testmodule1, 'module_introduction'))
        self.assertEquals(478, testmodule1.module_introduction)

    def test_member_refinement(self):

        class ModuleRefinement(object):

            refine_attr_in_module = 234

        self.assertEquals(123, testmodule1.attr_in_module)
        compose(ModuleRefinement(), testmodule1)
        self.assertEquals(234, testmodule1.attr_in_module)

    def test_function_introduction(self):

        class ModuleFunctionIntroduction(object):

            def introduce_my_function(self):

                def my_function(x, y):
                    return x - y

                return my_function

        self.assertEquals(False, hasattr(testmodule1, 'my_function'))
        compose(ModuleFunctionIntroduction(), testmodule1)
        self.assertEquals(0, testmodule1.my_function(3, 3))

    def test_function_refinement(self):

        class ModuleFunctionRefinement(object):

            def refine_func_in_module(self, original):

                def func_in_module(x, y):
                    return original(x, y) * 2

                return func_in_module

        self.assertEquals(2, testmodule1.func_in_module(1, 1))
        compose(ModuleFunctionRefinement(), testmodule1)
        self.assertEquals(4, testmodule1.func_in_module(1, 1))

    def test_tuple_refinement(self):

        class ModuleTupleRefinement(object):

            def refine_tuple_in_module(self, original):

                refinement = list(original)
                refinement.append(4)
                refinement = tuple(refinement)

                return refinement

        self.assertEquals(3, len(testmodule1.tuple_in_module))
        compose(ModuleTupleRefinement(), testmodule1)
        self.assertEquals(4, len(testmodule1.tuple_in_module))
        self.assertEquals(4, testmodule1.tuple_in_module[-1])

    def test_class_deep_refinement(self):

        class ClassRefinement(object):

            introduce_a = 123

            def refine_attr_in_class(self, original):
                return False

            def refine_plus(self, original):
                def plus(self, a, b):
                    return (a + b) * 2
                return plus

        class ModuleDeepRefinement(object):

            child_ClassInModule = ClassRefinement

        self.assertEquals(False, hasattr(testmodule1.ClassInModule, 'a'))
        self.assertEquals(2, testmodule1.ClassInModule().plus(1, 1))
        self.assertEquals(True, testmodule1.ClassInModule().attr_in_class)
        compose(ModuleDeepRefinement(), testmodule1)
        self.assertEquals(False, testmodule1.ClassInModule().attr_in_class)
        self.assertEquals(4, testmodule1.ClassInModule().plus(1, 1))

    def test_submodule_deep_refinement(self):

        class SubmoduleRefinement(object):

            introduce_a = 123

            def introduce_afunction(self):

                def afunction(a, b):

                    return a * b

                return afunction

        class PackageDeepRefinement(object):

            child_submodule = SubmoduleRefinement

        self.assertEquals(False, hasattr(testpackage1.submodule, 'a'))
        compose(PackageDeepRefinement(), testpackage1)
        self.assertEquals(123, testpackage1.submodule.a)
        self.assertEquals(5, testpackage1.submodule.afunction(1, 5))

    def test_compose_later(self):

        class LateModuleRefinement(object):

            introduce_a = 123

            def introduce_afunction(self):

                def afunction(a, b):
                    return a * b

                return afunction

        self.assertEquals(True, 'featuremonkey.test.mock.testmodule2' not in sys.modules)
        compose_later(LateModuleRefinement(), 'featuremonkey.test.mock.testmodule2')
        from featuremonkey.test.mock import testmodule2
        self.assertEquals(123, testmodule2.a)

    def test_compose_later_composition_order(self):

        class LateModuleRefinementA(object):

            introduce_a = 123

            def introduce_afunction(self):

                def afunction(a, b):
                    return a * b

                return afunction

        class LateModuleRefinementB(object):

            refine_a = 456

            def refine_afunction(self, original):

                def afunction(a, b):
                    return original(a, b) + 1

                return afunction

        self.assertEquals(True, 'featuremonkey.test.mock.testmodule3' not in sys.modules)
        compose_later(LateModuleRefinementA(), 'featuremonkey.test.mock.testmodule3')
        compose_later(LateModuleRefinementB(), 'featuremonkey.test.mock.testmodule3')
        from featuremonkey.test.mock import testmodule3
        self.assertEquals(456, testmodule3.a)
        self.assertEquals(5, testmodule3.afunction(2, 2))

if __name__ == '__main__':
    unittest.main()
