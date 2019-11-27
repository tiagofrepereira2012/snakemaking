#### DUMMY


import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.config import Config
from parsl.providers import LocalProvider, GridEngineProvider
from parsl.executors.threads import ThreadPoolExecutor
from parsl.executors import HighThroughputExecutor
from parsl.channels import LocalChannel, SSHChannel

import numpy

THREADS = 1

config = Config(executors=[ThreadPoolExecutor(max_threads=THREADS, label='local_threads')])


#config= Config(executors=[HighThroughputExecutor(
#                              label='local_threads',
#                              provider=GridEngineProvider(channel=LocalChannel(), worker_init="source /idiap/user/tpereira/conda/bin/activate /idiap/user/tpereira/conda/envs/snakemaking")
#                              )])


# Execution config
parsl.load(config)



# MY FUNCTIONS
@python_app
def taskA (inputs=[]):
    
    outputs = []
    for i in inputs:
        outputs.append(f'Do whatever with my input {i}')

    return outputs


@python_app
def taskB(inputs=[]):
    outputs = []
    for i in inputs:
        outputs.append(f'DOING IT AGAIN | {i}')

    return outputs


# building the pipeline
future_A = taskA(['A.txt','B.txt'])
future_B = taskB(future_A)


print(future_B.result())
pass


