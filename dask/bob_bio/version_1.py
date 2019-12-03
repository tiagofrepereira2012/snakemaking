##########
# DOING EVERYTHING MONOLITICALLY JUST TO SEE HOW THINGS WORK
########

import os
from dask.distributed import Client, LocalCluster
import string
import numpy

from random import randint
from time import sleep
from utils import read_biofiles, amend_path, split_data 
import itertools


NODES = 1


### LOCAL EXECUTION SINGLE THREAD SINGLE PROCESS

cluster = LocalCluster(nanny=False, processes=False, n_workers=1, threads_per_worker=1)
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


def process_bobbiofile(bio_files=[],
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
    for f in bio_files:

        # Defining Input/Output
        input_file  = f.make_path(f.current_directory, f.current_extension)
        output_file = f.make_path(output_path, output_extension)

        # TODO: Make a proper check for that
        if os.path.exists(output_file):
            f.current_directory = output_path
            f.current_extension = output_extension     
            continue

        if raw_data:
            data = f.load(f.current_directory, f.current_extension)
        else:
            data = read_bobbiodata(input_file)
        
        f.current_directory = output_path
        f.current_extension = output_extension
 
        # Preprocessing
        processed = processor(data)

        # Writing       
        bob.io.base.create_directories_safe(os.path.dirname(output_file))
        write_bobbiodata(processed, output_file)


    return bio_files


def train_bobalgorithm(bio_files, algorithm, output_model):
    import functools
    import operator

    # TODO: Make a proper check for that
    if os.path.exists(output_model):
        return output_model

    # Concatenating list of objects
    merged_training_futures = functools.reduce(operator.concat, bio_files)

    training_data = read_biofiles(merged_training_futures, bob.io.base.load)
    # TODO: Issue 106
    algorithm.train_projector(training_data, output_model)
  
    return output_model


def project_bobalgorithm(bio_files, algorithm, background_model, output_path, output_extension=".hdf5"):

    # Loading backgroundmodel
    algorithm.load_projector(background_model)

    for f in bio_files:
        # Defining Input/Output    
        input_file  = f.make_path(f.current_directory, f.current_extension)
        output_file = f.make_path(output_path, output_extension)

        # TODO: Make a proper check for that
        if os.path.exists(output_file):
            f.current_directory = output_path
            f.current_extension = output_extension     
            continue

        data = f.load(f.current_directory, f.current_extension)
       
        f.current_directory = output_path
        f.current_extension = output_extension

        projected = algorithm.project(data)

        bob.io.base.create_directories_safe(os.path.dirname(output_file))
        write_bobbiodata(projected, output_file)

 
    return bio_files



#####
##### TODO: HACKING Working with the idea that objects should know their location
##### 


training_objects = amend_path(db.training_files(), database_path, database_extension)
enroll_objects = amend_path(db.enroll_files(), database_path, database_extension)
probe_objects = amend_path(db.probe_files(), database_path, database_extension)




####### BUILDING THE PIPELINE ########


# 1. PREPROCESS
preproc_futures = []
preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                              dtype = numpy.float64)
output_path = os.path.join(experiment_path, "./preprocessed")


# Initial split
training_objects_split = split_data(training_objects, NODES)
enroll_objects_split = split_data(enroll_objects, NODES)
probe_objects_split = split_data(probe_objects, NODES)

preproc_training_futures = []
preproc_enroll_futures = []
preproc_probe_futures = []
for t_o, e_o, p_o in zip(training_objects_split, enroll_objects_split, probe_objects_split):
    preproc_training_futures.append(
            client.submit(process_bobbiofile,
                          t_o,
                          preprocessor,
                          output_path,
                          raw_data=True
                         )
            )

    preproc_enroll_futures.append(
            client.submit(process_bobbiofile,
                          e_o,
                          preprocessor,
                          output_path,
                          raw_data=True
                         )
            )
    
    preproc_probe_futures.append(
            client.submit(process_bobbiofile,
                          p_o,
                          preprocessor,
                          output_path,
                          raw_data=True
                         )
            )



# 2. EXTRACT
extract_training_futures = []
extract_enroll_futures = []
extract_probe_futures = []


extractor = bob.bio.base.extractor.Linearize()
output_path = os.path.join(experiment_path, "./extracted")
for t_o, e_o, p_o in zip(preproc_training_futures, preproc_enroll_futures, preproc_probe_futures):
       

    extract_training_futures.append(
            client.submit(process_bobbiofile,
                          t_o,
                          extractor,
                          output_path,
                          raw_data=False
                          )
            )

    extract_enroll_futures.append(
            client.submit(process_bobbiofile,
                          e_o,
                          extractor,
                          output_path,
                          raw_data=False
                          )
            )

    extract_probe_futures.append(
            client.submit(process_bobbiofile,
                          p_o,
                          extractor,
                          output_path,
                          raw_data=False
                          )
            )



#3. BACKGROUND MODEL TRAINING
from bob.bio.base.algorithm import PCA
algorithm = PCA(0.99)
output_model = os.path.join(experiment_path, "Project.hdf5")
background_model = client.submit(train_bobalgorithm, extract_training_futures, algorithm, output_model)


#4. PROJECTING

projected_enroll_futures = []
projected_probe_futures = []


output_path = os.path.join(experiment_path, "./projected")

for  e_o, p_o in zip(preproc_enroll_futures, preproc_probe_futures):

    projected_enroll_futures.append(
            client.submit(project_bobalgorithm,
                          e_o,
                          algorithm,
                          background_model,
                          output_path)
            )

    projected_probe_futures.append(
            client.submit(project_bobalgorithm,
                          p_o,
                          algorithm,
                          background_model,
                          output_path)
            )



#5. CREATE TEMPLATE

template_enroll_futures = []

output_path = os.path.join(experiment_path, "./models")


"""
for e_o, p_o in zip(preproc_enroll_futures, preproc_probe_futures):

    projected_enroll_futures.append(
            client.submit(project_bobalgorithm,
                          e_o,
                          algorithm,
                          background_model,
                          output_path)
            )

    projected_probe_futures.append(
            client.submit(project_bobalgorithm,
                          p_o,
                          algorithm,
                          background_model,
                          output_path)
            )
"""

#for  e_o, p_o in zip(projected_enroll_futures, projected_probe_futures):
#    e_o.result()
#    p_o.result()


#project_bobalgorithm(bio_files, algorithm, background_model, output_path, output_extension=".hdf5"):

#serialized_machine = pca_model.result()
#machine = from_dict(serialized_machine)

#print(machine.weights)

pass

