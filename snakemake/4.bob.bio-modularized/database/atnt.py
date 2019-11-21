import bob.bio.face
import re

path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
db = bob.bio.face.database.AtntBioDatabase()
group = "dev"


##########
# PATHS
#########

TRAINING_RAW_DATA = [f.make_path(directory=path, extension=".pgm") for f in db.training_files()]
ENROLL_RAW_DATA = [f.make_path(directory=path, extension=".pgm") for f in db.enroll_files()]
PROBE_RAW_DATA = [f.make_path(directory=path, extension=".pgm") for f in db.probe_files()]
# TODO: IT SEEMS THAT I CAN'T PROVIDE AS INPUT A CONCATENATION OF LISTS
ALL_RAW_DATA = TRAINING_RAW_DATA + ENROLL_RAW_DATA + PROBE_RAW_DATA 


TRAINING_PREPROCESSED_DATA = [f.make_path(directory="preprocessed", extension=".hdf5") for f in db.training_files()]
ENROLL_PREPROCESSED_DATA = [f.make_path(directory="preprocessed", extension=".hdf5") for f in db.enroll_files()]
PROBE_PREPROCESSED_DATA = [f.make_path(directory="preprocessed", extension=".hdf5") for f in db.probe_files()]
ALL_PREPROCESSED_DATA = TRAINING_PREPROCESSED_DATA + ENROLL_PREPROCESSED_DATA + PROBE_PREPROCESSED_DATA 



TRAINING_EXTRACTED_DATA = [f.make_path(directory="extracted", extension=".hdf5") for f in db.training_files()]
ENROLL_EXTRACTED_DATA = [f.make_path(directory="extracted", extension=".hdf5") for f in db.enroll_files()]
PROBE_EXTRACTED_DATA = [f.make_path(directory="extracted", extension=".hdf5") for f in db.probe_files()]
ALL_EXTRACTED_DATA = TRAINING_EXTRACTED_DATA + ENROLL_EXTRACTED_DATA + PROBE_EXTRACTED_DATA 



#TRAINING_PROJECTED_DATA = [f.make_path(directory="projected", extension=".hdf5") for f in db.training_files()]
ENROLL_PROJECTED_DATA = [f.make_path(directory="projected", extension=".hdf5") for f in db.enroll_files()]
PROBE_PROJECTED_DATA = [f.make_path(directory="projected", extension=".hdf5") for f in db.probe_files()]


model_numbers = db.model_ids(groups="dev")

MODELS = ["models/s{0}.hdf5".format(str(model_id)) for model_id in model_numbers]

ENROLL_DATA = dict([["models/s{0}.hdf5".format(model_id),
                    [f.make_path(directory="projected", extension=".hdf5") 
                       for f in db.enroll_files(model_id=int(model_id))]]
                    for model_id in model_numbers])

SCORES = ["scores/s{0}.txt".format(str(model_id)) for model_id in model_numbers]



