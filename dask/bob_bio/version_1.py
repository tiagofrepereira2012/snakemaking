##########
# DOING EVERYTHING MONOLITICALLY JUST TO SEE HOW THINGS WORK
########

import os
from dask.distributed import Client, LocalCluster
import string
import numpy

from random import randint
from time import sleep
from utils import read_biofiles



NODES = 1


### LOCAL EXECUTION

cluster = LocalCluster(nanny=False, processes=False)
client = Client(cluster)  # start local workers as threads

### SGE

#from dask_jobqueue import PBSCluster
#cluster = PBSCluster(cores=2, memory="4GB", queue="all.q")
#cluster.scale(NODES)
#client = Client(cluster)


experiment_path = "/idiap/user/tpereira/github/snakemaking/dask/bob_bio/test/"
database_path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
database_extension = ".pgm"

import bob.bio.face
db = bob.bio.face.database.AtntBioDatabase(original_directory=database_path,
                                           original_extension=database_extension)



def read_bobbiodata(file_name):
    return bob.io.base.load(file_name)

def write_bobbiodata(data, file_name):
    bob.io.base.save(data, file_name)



def process_bobbiofile(input_data=[],
                       processor=None,
                       output_path=None,
                       output_extension=".hdf5",
                       raw_data=True):
    """
    Given a list of BioFiles:
      1. Load
      2. Process
      3. Save
    """
    for f in input_data:

        # Defining Input/Output
        input_file  = f.make_path(f.current_directory, f.current_extension)
        output_file = f.make_path(output_path, output_extension)
   
        if raw_data:
            data = f.load(f.current_directory, f.current_extension)
        else:
            data = read_bobbiodata(input_file)
        
        # Preprocessing
        processed = processor(data)

        # Writing       
        bob.io.base.create_directories_safe(os.path.dirname(output_file))
        write_bobbiodata(processed, output_file)


    return input_data


def train_bobalgorithm(input_files, algorithm, output_model):

    import ipdb; ipdb.set_trace()

    training_data = read_biofiles(input_files, bob.io.base.load)
    

    import ipdb; ipdb.set_trace()

    return training_data

    pass



#####
##### TODO: HACKING Working with the idea that objects should know their location
##### 

def amend_path(objects, path, extension):
    for o in objects:
        o.current_directory = path
        o.current_extension = extension
    return objects
    

training_objects = amend_path(db.training_files(), database_path, database_extension)
enroll_objects = amend_path(db.enroll_files(), database_path, database_extension)
probe_objects = amend_path(db.probe_files(), database_path, database_extension)


input_data = training_objects + enroll_objects + probe_objects



offset=0
step = len(input_data)//NODES

####### BUILDING THE PIPELINE ########


# 1. PREPROCESS
preproc_futures = []
preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                              dtype = numpy.float64)

#import ipdb; ipdb.set_trace()

# Initial split
output_path = os.path.join(experiment_path, "./preprocessed")
for i in range(NODES):
    preproc_futures.append(

            client.submit(process_bobbiofile,
                          input_data[offset:offset+step],
                          preprocessor,
                          output_path,
                          raw_data=True
                         )
            )
    offset += step


# 2. EXTRACT
extract_futures = []
extractor = bob.bio.base.extractor.Linearize()
output_path = os.path.join(experiment_path, "./extracted")
for i in range(NODES):
    extract_futures.append(
            client.submit(process_bobbiofile,
                          preproc_futures[i],
                          extractor,
                          output_path,
                          raw_data=False
                          )
            )


#for i in range(NODES):
#    extract_futures[i].result()
#    pass

#import ipdb; ipdb.set_trace()

# 3. BACKGROUND
from bob.bio.base.algorithm import PCA
algorithm = PCA(0.99)
output_model = os.path.join(experiment_path, "Projected.hdf5")
background_model_training = client.submit(train_bobalgorithm, training_objects, algorithm, output_model)
background_model_training.result()


#serialized_machine = pca_model.result()
#machine = from_dict(serialized_machine)

#print(machine.weights)

pass

