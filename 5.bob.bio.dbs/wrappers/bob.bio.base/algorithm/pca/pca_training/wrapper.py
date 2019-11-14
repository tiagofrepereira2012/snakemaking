import bob.bio.base
import numpy


algorithm = bob.bio.base.algorithm.PCA(subspace_dimension=snakemake.params.pca_dim)

################
# TRAIN BACKGROUND
################

input_files = snakemake.input.input_files
output_file = snakemake.output.output_file


features = numpy.array(bob.bio.base.tools.extractor.read_features(input_files, algorithm, split_by_client=False))
algorithm.train_projector(features, output_file)

