##########
# DOING EVERYTHING MONOLITICALLY JUST TO SEE HOW THINGS WORK
########


import parsl
import os
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config
from parsl.config import Config
from parsl.providers import LocalProvider, GridEngineProvider
from parsl.executors.threads import ThreadPoolExecutor
from parsl.executors import HighThroughputExecutor
from parsl.channels import LocalChannel, SSHChannel

import numpy

THREADS = 2

config= Config(executors=[ThreadPoolExecutor(
                              max_threads=THREADS,
                              label='local_threads'
                              )])


#config= Config(executors=[HighThroughputExecutor(
#                              label='local_threads',
#                              max_workers=2,
#                              provider=GridEngineProvider(channel=LocalChannel(), worker_init="source /idiap/user/tpereira/conda/bin/activate /idiap/user/tpereira/conda/envs/snakemaking")
#                              )])

parsl.load(config)

import bob.bio.face
db = bob.bio.face.database.AtntBioDatabase()



@python_app
def preprocess(inputs=[], outputs=[]):
    database_path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
    database_extension = ".pgm"

    import bob.bio.face
    import bob.io.base
    import numpy 
    preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                                  dtype = numpy.float64)
    print("#### PRE PROC #####")
    for i in inputs:
          
        data = i.load(database_path, database_extension)
        preprocessed = preprocessor(data)
        outputs.append(preprocessed)

    print("preproc outputs: " + str(len(outputs)))
   
    return outputs


@python_app
def extract(inputs=[], outputs=[]):

    import bob.bio.base
    import bob.io.base
        
    print("######### EXTRACT #####")
    extractor = bob.bio.base.extractor.Linearize()
    print("extract inputs " + str(len(inputs)))
    for i in inputs:
            
        data = i
        extracted = extractor(data)
        outputs.append(extracted)
 
   
    return outputs


#preproc_data = numpy.array(db.training_files() + db.enroll_files() + db.probe_files())
preproc_data = numpy.array(db.training_files())[0:2]
offset=0
step = len(preproc_data)//THREADS
preprocessed = []

#import ipdb; ipdb.set_trace()
for i in range(THREADS):
    preprocessed.append(preprocess(inputs = preproc_data[offset:offset+step]))
    offset += step

extracted = []
for i in range(THREADS):
    extracted.append(extract(preprocessed[i]))


#for i in range(THREADS):
#    print(len(extracted[i].result()))

#for i in range(THREADS):
#    print(len(extracted[i].result()))



pass

