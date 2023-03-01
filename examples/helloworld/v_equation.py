import hello.main
import featuremonkey

import os

featuremonkey.select_equation(os.path.join(
    os.path.dirname(__file__), 'max_product.equation'))
hello.main.hello()
