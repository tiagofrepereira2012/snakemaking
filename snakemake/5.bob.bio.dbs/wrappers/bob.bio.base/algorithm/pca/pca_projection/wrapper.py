import bob.bio.base



input_file    = snakemake.input.input_file
pca_model     = snakemake.input.background_model
output_file   = snakemake.output.output_file

algorithm = bob.bio.base.algorithm.PCA(subspace_dimension=snakemake.params.pca_dim)


algorithm.load_projector(pca_model)
feature   = bob.io.base.load(input_file)
projected = algorithm.project(feature)
algorithm.write_feature(projected, output_file)

