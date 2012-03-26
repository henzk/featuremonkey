
def refine_hello(original):
    def hello():
        original()
        print 'wonderful',
    return hello
