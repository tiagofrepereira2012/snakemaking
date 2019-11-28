##########
# DOING EVERYTHING MONOLITICALLY JUST TO SEE HOW THINGS WORK
########

import os
from dask.distributed import Client
import string
import numpy

from random import randint
from time import sleep

NODES = 10


### LOCAL EXECUTION

client = Client(processes=False)  # start local workers as threads

### SGE

#from dask_jobqueue import PBSCluster

#cluster = PBSCluster(cores=2, memory="4GB", queue="all.q")
#cluster.scale(NODES)
#client = Client(cluster)


import bob.bio.face
db = bob.bio.face.database.AtntBioDatabase()


def to_dict(machine):
    """
    Dumps its content to a :py:class:`dict`
    
    **Returns**
      A :py:class:`dict` with :py:class:`bob.learn.linear.Machine` variables
      
    """
    
    output_dict = dict()
    output_dict["input_sub"] = machine.input_subtract
    output_dict["input_div"] = machine.input_divide
    output_dict["weights"] = machine.weights
    output_dict["activation"] = "Activation.Linear"
    output_dict["biases"] = machine.biases

    return output_dict

def from_dict(input_dict):
    """
    Loads itself from a python dict :py:class:`dict`
    
    **Parameters**

      input_dict: :py:class:`dict` to be imported
         Dictionary with the machine
    """
    import bob.learn.activation
    import bob.learn.linear
    
    machine = bob.learn.linear.Machine(numpy.array(input_dict["weights"], dtype="float"))
    machine.biases = numpy.array(input_dict["biases"], dtype="float")
    machine.input_subtract = numpy.array(input_dict["input_sub"], dtype="float")
    machine.input_divide = numpy.array(input_dict["input_div"], dtype="float")

    activation = bob.learn.activation.Linear()

    machine.activation = activation

    return machine




def preprocess(inputs=[]):
    database_path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
    database_extension = ".pgm"

    import bob.bio.face
    import bob.io.base
    import numpy 
    preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                                  dtype = numpy.float64)

    outputs = dict()
    for i in inputs:
          
        data = i.load(database_path, database_extension)
        preprocessed = preprocessor(data)
        outputs[i.make_path()] = preprocessed

    return outputs


def extract(inputs):

    import bob.bio.base
    import bob.io.base
        
    extractor = bob.bio.base.extractor.Linearize()
    outputs = dict()
    for i in inputs:
            
        data = inputs[i]
        extracted = extractor(data)
        outputs[i] = extracted
   
    return outputs


def extract(inputs):

    import bob.bio.base
    import bob.io.base
        
    extractor = bob.bio.base.extractor.Linearize()
    outputs = dict()
    for i in inputs:
            
        data = inputs[i]
        extracted = extractor(data)
        outputs[i] = extracted
   
    return outputs


def train_pca(inputs, objects_for_training):
    ## TODO: I KNOW IT'S INNEFICIENT, SO JUST KEEP YOUR COMMENT FOR YOURSELF

    import bob.learn.linear

    big_dict = dict()
    for i in inputs:
        big_dict.update(i)
    
    first = big_dict[next(iter(big_dict.keys()))]
    #import ipdb; ipdb.set_trace()
    data = numpy.zeros(shape=(len(objects_for_training), first.shape[0]))

    for i,o in enumerate(objects_for_training):
        data[i] = big_dict[o.make_path()]
    
    t = bob.learn.linear.PCATrainer()
    machine, variances = t.train(data)
    machine.resize(machine.shape[0], 300)

    return to_dict(machine)



preproc_data = numpy.array(db.training_files() + db.enroll_files() + db.probe_files())
offset=0
step = len(preproc_data)//NODES

####### BUILDING THE PIPELINE ########


# 1. PREPROCESS
preprocessed = []
for i in range(NODES):
    preprocessed.append(client.submit(preprocess, preproc_data[offset:offset+step]))
    offset += step

# 2. EXTRACT
extracted = []
for i in range(NODES):
    extracted.append(client.submit(extract, preprocessed[i]))

import ipdb; ipdb.set_trace()

# 3. BACKGROUND
pca_model = client.submit(train_pca, extracted, db.training_files())
serialized_machine = pca_model.result()

machine = from_dict(serialized_machine)

print(machine.weights)

pass

