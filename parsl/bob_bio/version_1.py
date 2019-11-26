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
from parsl.channels import LocalChannel

import numpy

THREADS = 1

#config= Config(executors=[ThreadPoolExecutor(
    #                          max_threads=THREADS,
    #                          label='local_threads',
    #                          provider=LocalProvider(channel=LocalChannel(), init_blocks=1, max_blocks=1)
    #                          )])


config= Config(executors=[HighThroughputExecutor(
                              label='local_threads',
                              provider=GridEngineProvider()
                              )])

parsl.load(config)

import bob.bio.face
db = bob.bio.face.database.AtntBioDatabase()


database_path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
database_extension = ".pgm"


@python_app
def preprocess(inputs=[], outputs=[]):

    import bob.bio.face
    import bob.io.base
        
    preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                                  dtype = numpy.float64)
        
    for i in inputs:
          
        data = i.load(database_path, database_extension)
        preprocessed = preprocessor(data)
        outputs.append(preprocessed)
            
    return outputs


@python_app
def extract(inputs=[], outputs=[]):

    import bob.bio.base
    import bob.io.base
        
    extractor = bob.bio.base.extractor.Linearize()
    for i in inputs:
            
        data = i
        extracted = extractor(data)
        outputs.append(extracted)
          
    return outputs



#import ipdb; ipdb.set_trace()

preproc_data = db.training_files() + db.enroll_files() + db.probe_files()
preprocessed = preprocess(inputs = preproc_data)

    #import ipdb; ipdb.set_trace()

#output = preprocessed.result()

extracted = extract(preprocessed)

output = extracted.result()

print(output)

pass



