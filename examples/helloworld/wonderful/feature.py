def select(composer):
    
    #refine hello.main using wonderful.main
    from hello import main as hello_main
    from wonderful import main as wonderful_main
    composer.compose(wonderful_main, hello_main)
