import bob.bio.face
import bob.bio.base
import bob.io.base
import numpy

path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
db = bob.bio.face.database.AtntBioDatabase()

group = "dev"

TRAIN_DATA = [f.make_path(directory=path, extension=".pgm") for f in db.training_files()]


#DATA_ENROLL = dict()
#for m in db.model_ids(groups=group):
#    DATA_ENROLL[m] = db.enroll_files(model_id=m)

#DATA_PROBE = db.probe_files()

#workdir: "preprocessed" #TODO: DOESN'T WORK.
rule PREPROCESSING:
    input:
        #input_file=[TRAIN_DATA, DATA_PROBE, DATA_ENROLL]
        input_file=TRAIN_DATA
    output:
        output_file=[f.make_path(directory="./preprocessed", extension=".hdf5") for f in db.training_files()]

    run:
        
        # define the preprocessor
        preprocessor = bob.bio.face.preprocessor.Base(
            color_channel="gray",
            dtype = numpy.float64)
        
        for f,o in zip(input.input_file, output.output_file):
            img = bob.io.base.load(f)
            preprocessed = preprocessor(img)
            bob.io.base.save(preprocessed, o)

#workdir: "extractor" #TODO: DOESN'T WORK.
rule EXTRACTOR:
    input:
        input_file=[f.make_path(directory="./preprocessed", extension=".hdf5") for f in db.training_files()]
    output:
        output_file=[f.make_path(directory="./extracted", extension=".hdf5") for f in db.training_files()]
    run:
        
        extractor = bob.bio.base.extractor.Linearize()
        # define the preprocessor
        for f,o in zip(input.input_file, output.output_file):
            img = bob.io.base.load(f)
            extracted = extractor(img)
            bob.io.base.save(extracted, o)
           
