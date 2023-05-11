import hello.main
import featuremonkey3

import os

featuremonkey3.select_equation(os.path.join(
    os.path.dirname(__file__), 'max_product.equation'))
hello.main.hello()
