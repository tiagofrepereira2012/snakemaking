import bob.bio.base
import numpy

input_files  = snakemake.input.input_files
algorithm    = bob.bio.base.algorithm.PCA(subspace_dimension=snakemake.params.pca_dim)
features = numpy.array(bob.bio.base.tools.extractor.read_features(input_files, algorithm, split_by_client=False))
output_file  = snakemake.output.output_file


model      = algorithm.enroll(features)
algorithm.write_model(model, output_file)


