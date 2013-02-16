
class MainRefinement(object):
    def refine_hello(self, original):
        def hello():
            original()
            print 'World'
        return hello

def select(composer):
    
    #here we declare the refinement directly in feature.py
    #see wonderful feature for an example on how to reference refinements specified in extra files
    from hello import main
    composer.compose(MainRefinement(), main)
