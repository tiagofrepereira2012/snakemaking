import os
from dask.distributed import Client
import string

from random import randint
from time import sleep

### LOCAL EXECUTION

#client = Client(processes=False)  # start local workers as threads

### SGE

from dask_jobqueue import PBSCluster

cluster = PBSCluster(cores=2, memory="4GB", queue="all.q")
cluster.scale(10)
client = Client(cluster)


# Creating my tasks

def get_jobid():
    job_id = ""
    if "JOB_ID" in os.environ:
        job_id = str(os.environ["HOSTNAME"])

    return job_id


def taskA (inputs=[]):
    
    outputs = []
    for i in inputs:
        seconds = randint(0,5)
        sleep(seconds)
        job_id = get_jobid()
        outputs.append(f'TASK A input {i} ({seconds}s)---- {job_id}')

    return outputs


def taskB(inputs=[]):
    outputs = []
    for i in inputs:
        job_id = get_jobid()      
        outputs.append(f'TASK B | {i} ---- {job_id}')

    return outputs


# building the pipeline
inputs = [f'{i}.txt' for i in string.ascii_lowercase]
future_A = []
for i in inputs:
    future_A.append(client.submit(taskA, [i]))

future_B = client.submit(taskB, future_A)

#import ipdb; ipdb.set_trace()


print(future_B)
print("")
output = future_B.result()
for o in output:
    print(o)
print("")
print(future_B)
pass


