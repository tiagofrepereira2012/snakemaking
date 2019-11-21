# Here we show how AppFutures are used to wait for the result of a Python App.

import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config


# We have to load some config
#print(config)
parsl.load(config)


@python_app
def hello ():
    import time
    time.sleep(5)
    return 'Hello World!'

app_future = hello()

# Check if the app_future is resolved, which it won't be
print('Done: {}'.format(app_future.done()))

# Print the result of the app_future. Note: this
# call will block and wait for the future to resolve
print('Result: {}'.format(app_future.result()))
print('Done: {}'.format(app_future.done()))


print("")
print("####### DATA FUTURES ########")

# App that echos an input message to an output file

@bash_app
def slowecho(message, outputs=[]):
    return 'sleep 5; echo %s &> %s' % (message, outputs[0])

# Call slowecho specifying the output file
hello = slowecho('Hello World!', outputs=[os.path.join(os.getcwd(), 'hello-world.txt')])

# The AppFuture's outputs attribute is a list of DataFutures
print(hello.outputs)


# Also check the AppFuture
print('Done: {}'.format(hello.done()))

# Print the contents of the output DataFuture when complete
with open(hello.outputs[0].result(), 'r') as f:
    print(f.read())

# Now that this is complete, check the DataFutures again, and the Appfuture
print(hello.outputs)
print('Done: {}'.format(hello.done()))



