########## COMPUTING PI EXAMPLE ########


import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from parsl.config import Config
from parsl.executors.threads import ThreadPoolExecutor
import numpy

# We have to load some config
##print(config)
#parsl.load(config)

THREADS = 1

config= Config(executors=[ThreadPoolExecutor(max_threads=THREADS,
                                 label='local_threads')])
parsl.load(config)


# App that estimates pi by placing points in a box
@python_app
def pi(num_points):
    from random import random
    #import ipdb; ipdb.set_trace()
    inside = 0
    for i in range(num_points):
        x, y = random(), random()  # Drop a random point in the box.
        if x**2 + y**2 < 1:        # Count points within the circle.
            inside += 1

    return (inside*4 / num_points)

# App that computes the mean of three values
@python_app
def mean(*numbers):
    return sum(numbers)/len(numbers)

# Estimate three values for pi
numbers = [pi(10**6) for i in range(THREADS)]
#import ipdb; ipdb.set_trace()

# Compute the mean of the three estimates
mean_pi  = mean(*numbers)

# Print the results
#print("a: {:.5f} b: {:.5f} c: {:.5f}".format(a.result(), b.result(), c.result()))
import ipdb; ipdb.set_trace()
print("Average: {:.5f}".format(mean_pi.result()))
