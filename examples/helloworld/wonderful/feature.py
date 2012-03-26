def select():
    
    #refine hello.main using wonderful.main
    from featuremonkey import compose
    from hello import main as hello_main
    from wonderful import main as wonderful_main
    compose(wonderful_main, hello_main)
