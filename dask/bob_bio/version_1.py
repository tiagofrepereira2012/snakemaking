##########
# DOING EVERYTHING MONOLITICALLY JUST TO SEE HOW THINGS WORK
########

import os
from dask.distributed import Client, LocalCluster
import string
import numpy
import time

from random import randint
from time import sleep
from utils import read_biofiles, amend_path, split_data 
import itertools

from samples import BiometricSamples, create_training_samples, create_biometric_template, create_biometric_probes


import functools
import operator


NODES = 10


### LOCAL EXECUTION SINGLE THREAD SINGLE PROCESS

#cluster = LocalCluster(nanny=False, processes=False, n_workers=1, threads_per_worker=1)
#cluster.scale_up(NODES)
#client = Client(cluster)  # start local workers as threads

#import ipdb; ipdb.set_trace()

### SGE


from dask_jobqueue import PBSCluster, SGECluster

q1d_resource_spec = "q_1day=TRUE,io_big=TRUE"
gpu_resource_spec = "q_gpu=TRUE"


cluster = SGECluster(queue="q_1day", memory='4GB', cores=2,
        log_directory="/idiap/user/tpereira/github/snakemaking/dask/bob_bio/logs",
        local_directory="/idiap/user/tpereira/github/snakemaking/dask/bob_bio/logs",
        resource_spec=q1d_resource_spec
        )

cluster.scale_up(NODES)
client = Client(cluster)  # start local workers as threads

   

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
training_samples = create_training_samples(BiometricSamples, db)

template_samples = create_biometric_template(BiometricSamples, db)

probe_samples = create_biometric_probes(BiometricSamples, db, template_samples)


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

            #LOAD 

            biometric_samples = func(*args, **kwargs)

            for b in biometric_samples:

                for o in b.samples:

                    if isinstance(b.samples, numpy.ndarray):

                        file_name = os.path.join(output_path, str(b.template_id) + output_extension)
                        if os.path.exists(file_name):
                            continue

                        bob.io.base.create_directories_safe(os.path.dirname(file_name))
                        write_bobbiodata(b.samples, file_name)
                    else:
                           
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


            return biometric_samples
             
        return wrapper
    return decorator



def process_bobbio_samples(biometric_samples,
                           processor):
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


def train_bobalgorithm(biometric_samples, algorithm, output_model):
    # TODO: Make a proper check for that
    if os.path.exists(output_model):
        return output_model

    # Concatenating list of objects
    merged_training_futures = functools.reduce(operator.concat, biometric_samples)

    training_data = read_biofiles(merged_training_futures, bob.io.base.load)
    
    # TODO: Issue 106
    algorithm.train_projector(training_data, output_model)
  
    return output_model


def project_bobalgorithm(biometric_samples, algorithm, background_model):

    # Loading backgroundmodel
    algorithm.load_projector(background_model)

    for f in biometric_samples:

        for s in f.samples:

            if s.sample is None:
                input_file = s.make_path(s.current_directory, s.current_extension)
                s.sample   = read_bobbiodata(input_file) 

            data = s.sample
            projected = algorithm.project(data)
            s.sample = projected

    return biometric_samples


def create_bobbio_templates(biometric_samples, algorithm):

    for f in biometric_samples:
        template_data = read_biofiles([f], bob.io.base.load)
        f.samples = algorithm.enroll(template_data)
        pass


    return biometric_samples


def compute_bobbio_scores(biometric_samples, biometric_templates, algorithm):

    # TODO this function it's not in its best shape
    template_list = [t.template_id for t in biometric_templates]

    score_strings = []
    for b in biometric_samples:
   
        for t in b.template_list:

            if t.template_id in template_list:

                template_sample = biometric_templates[template_list.index(t.template_id)]

                bobbio_path = b.samples[0].make_path()

                import logging
                logging.basicConfig()
                logger = logging.getLogger()
                logger.setLevel(logging.INFO)
                logger.info( template_sample.samples )
                logger.info(b.samples[0].sample)

                score = algorithm.score(numpy.array(template_sample.samples),  b.samples[0].sample)

                score_strings.append(f"{t.template_id} {b.template_id} {bobbio_path} {score}")

    return score_strings



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
probe_objects_split = split_data(probe_samples, NODES)

preproc_training_futures = []
preproc_enroll_futures = []
preproc_probe_futures = []


# DECORATING INPUT AND OUTPUT
output_path = os.path.join(experiment_path, "./preprocessed")
decorated_preprocess = cache_bobbio_samples(output_path, ".hdf5")(process_bobbio_samples)

#import ipdb; ipdb.set_trace()

for t_o, e_o, p_o in zip(training_objects_split, template_objects_split, probe_objects_split):
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

    
      
    preproc_probe_futures.append(
            client.submit(decorated_preprocess,
                          biometric_samples=p_o,
                          processor=preprocessor
                         )
            )
#import ipdb; ipdb.set_trace()


#for t_o, e_o, p_o in zip(preproc_training_futures, preproc_enroll_futures, preproc_probe_futures):
#    t_o.result()
#    e_o.result()
#    p_o.result()
#exit()

 
# 2. EXTRACT

extract_training_futures = []
extract_enroll_futures = []
extract_probe_futures = []


extractor = bob.bio.base.extractor.Linearize()
output_path = os.path.join(experiment_path, "./extracted")

decorated_extractor = cache_bobbio_samples(output_path, ".hdf5")(process_bobbio_samples)
#decorated_extractor = process_bobbiofile


for t_o, e_o, p_o in zip(preproc_training_futures, preproc_enroll_futures, preproc_probe_futures):
       

    extract_training_futures.append(
            client.submit(decorated_extractor,
                          biometric_samples=t_o,
                          processor=extractor
                          )
            )

    extract_enroll_futures.append(
            client.submit(decorated_extractor,
                          biometric_samples=e_o,
                          processor=extractor
                          )
            )

    extract_probe_futures.append(
            client.submit(decorated_extractor,
                          biometric_samples=p_o,
                          processor=extractor
                          )
            )

#for t_o, e_o, p_o in zip(extract_training_futures, extract_enroll_futures, extract_probe_futures):
#    t_o.result()
#    e_o.result()
#    p_o.result()



#3. BACKGROUND MODEL TRAINING

from bob.bio.base.algorithm import PCA
algorithm = PCA(0.99)
output_model = os.path.join(experiment_path, "Project.hdf5")
background_model = client.submit(train_bobalgorithm, extract_training_futures, algorithm, output_model)

background_model.result()



#4. PROJECTING
projected_enroll_futures = []
projected_probe_futures = []


# DECORATING INPUT AND OUTPUT
output_path = os.path.join(experiment_path, "./projected")
decorated_projected = cache_bobbio_samples(output_path, ".hdf5")(project_bobalgorithm)

for  e_o, p_o in zip(extract_enroll_futures, extract_probe_futures):

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

#for  e_o, p_o in zip(projected_enroll_futures, projected_probe_futures):
#    e_o.result()
#    p_o.result()



#5. CREATE TEMPLATE

template_enroll_futures = []
output_path = os.path.join(experiment_path, "./models")

decorated_templates = cache_bobbio_samples(output_path, ".hdf5")(create_bobbio_templates)


for e_o in projected_enroll_futures:
    template_enroll_futures.append(
            client.submit(
                    decorated_templates,
                    e_o,
                    algorithm
                )
            )
 


### SYNC. THE MODELS I DON'T KNOW IF THIS IS NECESSARY

all_templates = []
for e_o in projected_enroll_futures:
    all_templates += e_o.result()


for p_o in projected_probe_futures:
    while not p_o.done():
        print("Waiting PROBE .....")
        time.sleep(0.1)
        continue

#for e_o in projected_enroll_futures:
#    while not e_o.done():
#        print("Waiting ENROLL .....")
#        time.sleep(0.1)
#        continue


### END SYNC

 
#6. SCORING
score_futures = []
#import ipdb; ipdb.set_trace()
#all_templates = functools.reduce(operator.concat, template_enroll_futures)

for p_o in projected_probe_futures:
   
    score_futures.append(
            client.submit(
                    compute_bobbio_scores,
                    p_o,
                    all_templates,
                    algorithm
                )
            )

score_strings = []
for p_o in score_futures:
    score_strings += p_o.result()

open(os.path.join(experiment_path, "scores-dev"), 'w').write('\n'.join(score_strings))

#import ipdb; ipdb.set_trace()


pass
#"""
