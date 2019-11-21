#### Getting around parsl Apps


import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config


# We have to load some config
print(config)
parsl.load(config)

@python_app
def hello ():
    return 'Hello World!'
print(hello().result())


@python_app
def multiply(a, b):
    return a * b
print(multiply(5, 9).result())


@python_app
def slow_hello ():
    import time
    time.sleep(5)
    return 'Hello World!'
print(slow_hello().result())


