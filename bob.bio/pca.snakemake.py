import bob.bio.face
import bob.bio.base
import bob.io.base
import numpy
import re


workdir: "PCA-experiment"

def compute(executor, input_file, output_file):
    img = bob.io.base.load(input_file)
    preprocessed = executor(img)
    bob.io.base.save(preprocessed, output_file)

def load(file_names, extractor):
    return bob.bio.base.tools.extractor.read_features(file_names,
            extractor,
            split_by_client=False
            )

path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
db = bob.bio.face.database.AtntBioDatabase()
group = "dev"


BACKGROUND_MODEL_FILE = "projector.hdf5"

#########
# TOOLS
########
preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                              dtype = numpy.float64)

extractor = bob.bio.base.extractor.Linearize()

algorithm = bob.bio.base.algorithm.PCA(subspace_dimension=0.95)


##########
# PATHS
#########

TRAINING_RAW_DATA = [f.make_path(directory=path, extension=".pgm") for f in db.training_files()]

TRAINING_PREPROCESSED_DATA = [f.make_path(directory="preprocessed", extension=".hdf5") for f in db.training_files()]

TRAINING_EXTRACTED_DATA = [f.make_path(directory="extracted", extension=".hdf5") for f in db.training_files()]

TRAINING_PROJECTED_DATA = [f.make_path(directory="projected", extension=".hdf5") for f in db.training_files()]




###########
# PROJECTED
###########


projected_dict = dict(zip(TRAINING_PROJECTED_DATA, TRAINING_EXTRACTED_DATA))

# define the preprocessor
wildcard_constraints:
    z = '|'.join(re.escape(z) for z in TRAINING_PROJECTED_DATA)


rule project_all:
    input:
        expand('{z}', z=TRAINING_PROJECTED_DATA)


rule PROJECT:
    input: 
        input_file = lambda wc: projected_dict[wc.z],
        projected_file = BACKGROUND_MODEL_FILE
    output:
        output_file='{z}',
    run:
        
        algorithm.load_projector(input.projected_file)
        compute(algorithm.project,input.input_file, output.output_file)




################
# TRAIN BACKGROUND
################


rule TRAIN:
    input:        
        input_file = TRAINING_EXTRACTED_DATA
    output:
        output_file = BACKGROUND_MODEL_FILE
    run:
        features = load(input.input_file, extractor)
        algorithm.train_projector(features, output.output_file)


################
# EXTRACTOR
################


extracted_dict = dict(zip(TRAINING_EXTRACTED_DATA, TRAINING_PREPROCESSED_DATA))

# define the preprocessor
wildcard_constraints:
    y = '|'.join(re.escape(y) for y in TRAINING_EXTRACTED_DATA)


rule extract_all:
    input:
        expand('{y}', y=TRAINING_EXTRACTED_DATA)


rule EXTRACTOR:
    input:        
        input_file = lambda wc: extracted_dict[wc.y]
    output:
        output_file='{y}'
    run:        
        compute(extractor, input.input_file, output.output_file)


###################
# PREPROCESSING
###################


preprocessed_dict = dict(zip(TRAINING_PREPROCESSED_DATA, TRAINING_RAW_DATA))

# define the preprocessor
wildcard_constraints:
    x = '|'.join(re.escape(x) for x in TRAINING_PREPROCESSED_DATA)


rule preprocessing_all:
    input:
        expand('{x}', x=TRAINING_PREPROCESSED_DATA)


rule PREPROCESSING:
    input:
        input_file = lambda wc: preprocessed_dict[wc.x]
    output:
        output_file = '{x}'
    run:
        # define the preprocessor
        compute(preprocessor, input.input_file, output.output_file)

