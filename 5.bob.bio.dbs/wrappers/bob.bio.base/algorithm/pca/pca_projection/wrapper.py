import bob.bio.base


input_file    = snakemake.input.input_file
pca_model     = snakemake.input.background_model
output_file   = snakemake.input.output_file


algorithm = bob.bio.base.algorithm.PCA(subspace_dimension=0.95)

algorithm.load_projector(pca_model)
feature = bob.io.base.load(input_file)
algorithm.project(input_file, output_file)

