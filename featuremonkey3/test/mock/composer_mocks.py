class Base:
    
    base_prop = 8
    
    def base_method(self, a_str):
        return a_str


class MemberIntroduction:
    introduce_a = 1

class ExistingMemberIntroduction:
    introduce_base_prop = 1

class MethodIntroduction:

    def introduce_method(self):
        
        def method(self):
            return True
        
        return method

class MethodRefinement:
    
    def refine_base_method(self, original):
        
        def base_method(self, a_str):
            return original(self, a_str) + 'refined'
        
        return base_method


class MethodRefinement2:
    
    def refine_base_method(self, original):
        
        def base_method(self, a_str):
            return original(self, a_str) + 'refined'
        
        return base_method


class StaticBase:

    @staticmethod
    def base_method(a_str):
        return a_str


class StaticMethodRefinement:

    def refine_base_method(self, original):

        def base_method(a_str):
            return original(a_str) + 'refined'

        return base_method


class ClassMethodBase:

    @classmethod
    def base_method(cls, a_str):
        return a_str


class ClassMethodRefinement:

    def refine_base_method(self, original):

        def base_method(cls, a_str):
            return original(cls, a_str) + 'refined'

        return base_method



