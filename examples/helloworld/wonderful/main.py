
def refine_hello(original):
    def hello():
        original()
        print('Wonderful')
    return hello
