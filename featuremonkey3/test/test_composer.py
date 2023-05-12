# from __future__ import absolute_import
from importlib import reload
from featuremonkey3 import compose, compose_later
from featuremonkey3.test.mock import composer_mocks as mocks
from featuremonkey3.test.mock import testmodule1, testpackage1
import pytest
import sys

@pytest.fixture
def reload_mocks():
    reload(mocks)


class TestObjectComposition:

    def test_noparam(self, reload_mocks):
        with pytest.raises(Exception):
            compose()

    def test_singleparam(self, reload_mocks):
        assert self == compose(self)

    def test_idendity(self, reload_mocks):
        instance = mocks.Base()
        composition = compose(mocks.MemberIntroduction(), instance)
        assert instance == composition

    def test_member_introduction(self, reload_mocks):
        instance = mocks.Base()
        composition = compose(mocks.MemberIntroduction(), instance)
        assert composition.base_prop == 8
        assert composition.a == 1

    def test_existing_member_introduction(self, reload_mocks):
        instance = mocks.Base()
        with pytest.raises(Exception):
            compose(mocks.ExistingMemberIntroduction(), instance)

    def test_method_introduction(self, reload_mocks):
        instance = mocks.Base()
        composition = compose(mocks.MethodIntroduction(), instance)
        assert composition.base_prop == 8
        assert composition.method()

    def test_method_refinement(self, reload_mocks):
        instance = mocks.Base()
        composition = compose(mocks.MethodRefinement(), instance)
        assert composition.base_method("Hello") == "Hellorefined"

    def test_staticmethod(self, reload_mocks):
        instance = mocks.StaticBase()
        instance2 = mocks.StaticBase()
        assert instance.base_method("Hello") == "Hello"
        composition = compose(mocks.StaticMethodRefinement(), instance)
        assert composition.base_method("Hello") == "Hellorefined"
        assert instance2.base_method("Hello") == "Hello"

    def test_classmethod(self, reload_mocks):
        instance = mocks.ClassMethodBase()
        assert instance.base_method("Hello") == "Hello"
        composition = compose(mocks.ClassMethodRefinement(), instance)
        assert composition.base_method("Hello") == "Hellorefined"

class TestClassComposition:

    def test_idendity(self, reload_mocks):
        clss = mocks.Base
        composition = compose(mocks.MemberIntroduction, clss)
        assert composition == clss

    def test_membr_introduction(self, reload_mocks):
        compose(mocks.MemberIntroduction, mocks.Base)
        assert mocks.Base.base_prop == 8
        assert mocks.Base.a == 1

    def test_existing_member_introduction(self, reload_mocks):
        with pytest.raises(Exception):
            compose(mocks.ExistingMemberIntroduction, mocks.Base)

    def test_method_introduction(self, reload_mocks):
        compose(mocks.MethodIntroduction(), mocks.Base)
        assert mocks.Base.base_prop == 8
        assert mocks.Base().method()

    def test_method_refinement(self, reload_mocks):
        compose(mocks.MethodRefinement2(), mocks.Base)
        assert mocks.Base().base_method("Hello") == "Hellorefined"

    def test_staticmethod(self, reload_mocks):
        assert mocks.StaticBase.base_method("Hello") == "Hello"
        assert mocks.StaticBase().base_method("Hello") == "Hello"
        compose(mocks.StaticMethodRefinement(), mocks.StaticBase)
        assert mocks.StaticBase.base_method("Hello") == "Hellorefined"
        assert mocks.StaticBase().base_method("Hello") == "Hellorefined"

    def test_classmethod(self, reload_mocks):
        assert mocks.ClassMethodBase.base_method("Hello") == "Hello"
        assert mocks.ClassMethodBase().base_method("Hello") == "Hello"
        compose(mocks.ClassMethodRefinement(), mocks.ClassMethodBase)
        assert mocks.ClassMethodBase.base_method("Hello") == "Hellorefined"
        assert mocks.ClassMethodBase().base_method("Hello") == "Hellorefined"

@pytest.fixture
def reload_modules():
    if hasattr(testmodule1, "module_introduction"):
        del testmodule1.module_introduction

    reload(testmodule1)
    reload(testpackage1)

class TestModuleComposition:

    def test_reloading_clears_composition(self, reload_modules):

        assert not hasattr(testmodule1, "module_introduction")

    def test_member_introduction(self, reload_modules):

        class ModuleIntroduction(object):

            introduce_module_introduction = 478

        compose(ModuleIntroduction(), testmodule1)
        assert hasattr(testmodule1, "module_introduction")
        assert testmodule1.module_introduction == 478

    def test_member_refinement(self, reload_modules):

        class ModuleRefinement(object):

            refine_attr_in_module = 234

        assert testmodule1.attr_in_module == 123
        compose(ModuleRefinement(), testmodule1)

        assert testmodule1.attr_in_module == 234

    def test_function_introduction(self, reload_modules):

        class ModuleFunctionIntroduction(object):

            def introduce_my_function(self):

                def my_function(x, y):
                    return x - y

                return my_function

        assert not hasattr(testmodule1, "my_function")
        compose(ModuleFunctionIntroduction(), testmodule1)

        assert testmodule1.my_function(3, 3) == 0

    def test_function_refinement(self, reload_modules):

        class ModuleFunctionRefinement(object):

            def refine_func_in_module(self, original):

                def func_in_module(x, y):
                    return original(x, y) * 2

                return func_in_module

        assert testmodule1.func_in_module(1, 1) == 2
        compose(ModuleFunctionRefinement(), testmodule1)

        assert testmodule1.func_in_module(1, 1) == 4

    def test_tuple_refinement(self, reload_modules):

        class ModuleTupleRefinement(object):

            def refine_tuple_in_module(self, original):

                refinement = list(original)
                refinement.append(4)
                refinement = tuple(refinement)

                return refinement

        assert len(testmodule1.tuple_in_module) == 3
        compose(ModuleTupleRefinement(), testmodule1)

        assert len(testmodule1.tuple_in_module) == 4
        assert testmodule1.tuple_in_module[-1] == 4

    def test_class_deep_refinement(self, reload_modules):

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

        assert not hasattr(testmodule1.ClassInModule, "a")
        assert testmodule1.ClassInModule().plus(1, 1) == 2
        assert testmodule1.ClassInModule().attr_in_class
        compose(ModuleDeepRefinement(), testmodule1)

        assert not testmodule1.ClassInModule().attr_in_class
        assert testmodule1.ClassInModule().plus(1, 1) == 4

    def test_submodule_deep_refinement(self, reload_modules):

        class SubmoduleRefinement(object):

            introduce_a = 123

            def introduce_afunction(self):

                def afunction(a, b):

                    return a * b

                return afunction

        class PackageDeepRefinement(object):

            child_submodule = SubmoduleRefinement

        assert not hasattr(testpackage1.submodule, "a")
        compose(PackageDeepRefinement(), testpackage1)

        assert testpackage1.submodule.a == 123
        assert testpackage1.submodule.afunction(1, 5) == 5

    def test_submodule_function_refinement(self, reload_modules):

        class SubmoduleRefinement:

            def refine_add_one(self, original):

                def add_one(x):
                    return original(x) + 1

                return add_one

        class PackageDeepRefinement:
            child_submodule = SubmoduleRefinement

        assert testpackage1.submodule.add_one(1) == 2
        compose(PackageDeepRefinement(), testpackage1)

        assert testpackage1.submodule.add_one(1) == 3

    def test_compose_later(self, reload_modules):

        class LateModuleRefinement(object):

            introduce_a = 123

            def introduce_afunction(self):

                def afunction(a, b):
                    return a * b

                return afunction

        assert 'featuremonkey3.test.mock.testmodule2' not in sys.modules
        compose_later(LateModuleRefinement(), 'featuremonkey3.test.mock.testmodule2')
        from featuremonkey3.test.mock import testmodule2

        assert testmodule2.a == 123

    def test_compose_later_composition_order(self, reload_modules):

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

        assert "featuremonkey3.test.mock.testmodule3" not in sys.modules
        compose_later(LateModuleRefinementA(), 'featuremonkey3.test.mock.testmodule3')
        compose_later(LateModuleRefinementB(), 'featuremonkey3.test.mock.testmodule3')
        from featuremonkey3.test.mock import testmodule3

        assert testmodule3.a == 456
        assert testmodule3.afunction(2, 2) == 5
