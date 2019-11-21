# Simple sequential or procedural workflows can be created by passing an AppFuture from one task to another.
# The following example shows one such workflow, which first generates a random number and then writes it to a file.


import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config


# We have to load some config
#print(config)
parsl.load(config)



# App that generates a random number
@python_app
def generate(limit):
    from random import randint
    return randint(1,limit)

# App that writes a variable to a file
@bash_app
def save(variable, outputs=[]):
    return 'echo %s &> %s' % (variable, outputs[0])


# Generate a random number between 1 and 10
random = generate(10)

# Save the random number to a file
saved = save(random, outputs=[os.path.join(os.getcwd(), 'sequential-output.txt')])

print('Random number: %s' % random.result())


# Print the output file
with open(saved.outputs[0].result(), 'r') as f:
    print('File contents: %s' % f.read())

