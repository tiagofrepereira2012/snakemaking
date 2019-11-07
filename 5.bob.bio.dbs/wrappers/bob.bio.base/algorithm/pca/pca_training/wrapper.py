import bob.bio.base
import numpy

BACKGROUND_MODEL_FILE = "projector.hdf5"
algorithm = bob.bio.base.algorithm.PCA(subspace_dimension=0.95)

################
# TRAIN BACKGROUND
################

input_files = snakemake.input.input_files
reader      = bob.bio.base.extractor.Extractor()
output_file = snakemake.output.output_file


features = numpy.array(bob.bio.base.tools.extractor.read_features(input_files, reader, split_by_client=False))
algorithm.train_projector(features, output_file)

