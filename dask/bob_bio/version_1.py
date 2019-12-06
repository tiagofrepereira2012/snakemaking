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

from samples import BiometricSamples


NODES = 1


### LOCAL EXECUTION SINGLE THREAD SINGLE PROCESS

cluster = LocalCluster(nanny=False, processes=False, n_workers=1, threads_per_worker=1)
client = Client(cluster)  # start local workers as threads

### SGE

"""
from dask_jobqueue import PBSCluster, SGECluster

q1d_resource_spec = "q_1day=TRUE,io_big=TRUE"
gpu_resource_spec = "q_gpu=TRUE"


cluster = SGECluster(queue="q_1day", memory='4GB', cores=2,
        log_directory="/idiap/user/tpereira/github/snakemaking/dask/bob_bio/logs",
        local_directory="/idiap/user/tpereira/github/snakemaking/dask/bob_bio/logs",
        resource_spec=q1d_resource_spec
        )
"""     

#############
# HERE I'M TESTING HETEROGENEOUS JOBS
#

### NODES q1d
#for i in range(NODES-1):
    # GETTING THE SPEC TEMPLATE#
    #spec = cluster.new_spec

    # PATCHING
    #spec['options']['resource_spec'] = q1d_resource_spec
    #cluster.worker_spec[i] = spec

#import ipdb; ipdb.set_trace()    
#cluster.scale_up(NODES-1)

### NODE GPU

# GETTING THE SPEC TEMPLATE#
#spec = cluster.new_spec

# PATCHING
#spec['options']['resource_spec'] = gpu_resource_spec
#spec['options']['queue'] = 'q_gpu'
#cluster.worker_spec[i] = spec
#cluster.scale_up(1)

##############
#import ipdb; ipdb.set_trace()

cluster.scale_up(10)
client = Client(cluster)


##########
# HANDLING DATABASE
##########

experiment_path = "/idiap/user/tpereira/github/snakemaking/dask/bob_bio/test/"
database_path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
database_extension = ".pgm"


import bob.bio.face
db = bob.bio.face.database.AtntBioDatabase(original_directory=database_path,
                                           original_extension=database_extension)


# TODO: REPLACE 
training_samples = BiometricSamples.create_training_samples(db)

template_samples = BiometricSamples.create_biometric_template(db)

#    def create_biometric_template(cls, database, group="dev", protocol="Default"):

#training_objects = amend_path(db.training_files(), database_path, database_extension)
#enroll_objects = amend_path(db.enroll_files(), database_path, database_extension)
#probe_objects = amend_path(db.probe_files(), database_path, database_extension)

#training_objects = db.training_files()
#enroll_objects = db.enroll_files()
#probe_objects = db.probe_files()


def read_bobbiodata(file_name):
    return bob.io.base.load(file_name)

def write_bobbiodata(data, file_name):
    bob.io.base.save(data, file_name)


def cache_bobbio_samples(output_path, output_extension):
    def decorator(func):
                       
        def wrapper(*args, **kwargs):

            biometric_samples = func(*args, **kwargs)

            for b in biometric_samples:

                for o in b.samples:
                    # Setting the current location of the biofile
                    o.current_directory = output_path
                    o.current_extension = output_extension

                    # Saving
                    file_name = o.make_path(o.current_directory, o.current_extension)
                    
                    # If it is already cached, don't do anything
                    if os.path.exists(file_name):
                        continue

                    # Save
                    bob.io.base.create_directories_safe(os.path.dirname(file_name))
                    write_bobbiodata(o.sample, file_name)
                    o.sample = None


            #import logging
            #logging.basicConfig()
            #logger = logging.getLogger()

            #logger.setLevel(logging.INFO)
            #logger.info("##############")
            #logger.info("Done")
            #logger.info("##############")

            return biometric_samples
             
        return wrapper
    return decorator



def process_bobbiofile(biometric_samples=[],
                       processor=None):
    """
    Given a list of BioFiles:
      1. Load
      2. Process
      3. Save
    """

    for b in biometric_samples:

        for f in b.samples:

            if f.sample is None:
                input_file = f.make_path(f.current_directory, f.current_extension)
                f.sample   = read_bobbiodata(input_file) 
               
            # Preprocessing
            data = f.sample
            processed = processor(data)

            # Injecting the sample in bio_file
            f.sample = processed

    return biometric_samples


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


def project_bobalgorithm(bio_files, algorithm, background_model):

    # Loading backgroundmodel
    algorithm.load_projector(background_model)

    for f in bio_files:

        if f.sample is None:
            input_file = f.make_path(f.current_directory, f.current_extension)
            f.sample   = read_bobbiodata(input_file) 

        data = f.sample
        projected = algorithm.project(data)
        f.sample = data

    return bio_files





######################################
####### BUILDING THE PIPELINE ########
######################################


# 1. PREPROCESS
preproc_futures = []
preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                              dtype = numpy.float64)


# Initial split
training_objects_split = split_data(training_samples, NODES)
template_objects_split = split_data(template_samples, NODES)
#probe_objects_split = split_data(probe_objects, NODES)

preproc_training_futures = []
preproc_enroll_futures = []
preproc_probe_futures = []


# DECORATING INPUT AND OUTPUT
output_path = os.path.join(experiment_path, "./preprocessed")
decorated_preprocess = cache_bobbio_samples(output_path, ".hdf5")(process_bobbiofile)
#decorated_preprocess = process_bobbiofile

for t_o, e_o, p_o in zip(training_objects_split, template_objects_split, template_objects_split):
    preproc_training_futures.append(
            client.submit(decorated_preprocess,
                          biometric_samples=t_o,
                          processor=preprocessor
                         )
            )


    preproc_enroll_futures.append(
            client.submit(decorated_preprocess,
                          biometric_samples=e_o,
                          processor=preprocessor
                         )
            )

    
  
    
    #preproc_probe_futures.append(
    #        client.submit(decorated_preprocess,
    #                      bio_files=p_o,
    #                      processor=preprocessor
    #                     )
    #        )

for t_o, e_o in zip(preproc_training_futures, preproc_enroll_futures):
    t_o.result()
    e_o.result()

"""
 
# 2. EXTRACT
extract_training_futures = []
extract_enroll_futures = []
extract_probe_futures = []


extractor = bob.bio.base.extractor.Linearize()
output_path = os.path.join(experiment_path, "./extracted")

decorated_extractor = cache_bobbio_samples(output_path, ".hdf5")(process_bobbiofile)
#decorated_extractor = process_bobbiofile


for t_o, e_o, p_o in zip(preproc_training_futures, preproc_enroll_futures, preproc_probe_futures):
       

    extract_training_futures.append(
            client.submit(decorated_extractor,
                          bio_files=t_o,
                          processor=extractor
                          )
            )

    extract_enroll_futures.append(
            client.submit(decorated_extractor,
                          bio_files=e_o,
                          processor=extractor
                          )
            )

    extract_probe_futures.append(
            client.submit(decorated_extractor,
                          bio_files=p_o,
                          processor=extractor
                          )
            )


#for i, j, k in zip(extract_training_futures, extract_enroll_futures, extract_probe_futures):
#    i.result()
#    j.result()
#    k.result()


#3. BACKGROUND MODEL TRAINING

from bob.bio.base.algorithm import PCA
algorithm = PCA(0.99)
output_model = os.path.join(experiment_path, "Project.hdf5")
background_model = client.submit(train_bobalgorithm, extract_training_futures, algorithm, output_model)



#4. PROJECTING
projected_enroll_futures = []
projected_probe_futures = []


# DECORATING INPUT AND OUTPUT
output_path = os.path.join(experiment_path, "./projected")
decorated_projected = cache_bobbio_samples(output_path, ".hdf5")(project_bobalgorithm)

for  e_o, p_o in zip(preproc_enroll_futures, preproc_probe_futures):

    projected_enroll_futures.append(
            client.submit(decorated_projected,
                          e_o,
                          algorithm,
                          background_model
                          )
            )

    projected_probe_futures.append(
            client.submit(decorated_projected,
                          p_o,
                          algorithm,
                          background_model
                         )
            )

for  e_o, p_o in zip(projected_enroll_futures, projected_probe_futures):
    e_o.result()
    p_o.result()
"""




#5. CREATE TEMPLATE
"""
template_enroll_futures = []
output_path = os.path.join(experiment_path, "./models")


pass
"""
