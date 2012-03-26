
class MainRefinement(object):
    def refine_hello(self, original):
        def hello():
            original()
            print 'World'
        return hello

def select():
    
    #here we declare the refinement directly in feature.py
    #see wonderful feature for an example on how to reference refinements specified in extra files
    from featuremonkey import compose
    from hello import main
    compose(MainRefinement(), main)
