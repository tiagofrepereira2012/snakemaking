import bob.bio.base
import numpy

model_file  = snakemake.input.input_file
model_id    = snakemake.params.model_ids[model_file]

probe_files = snakemake.input.probe_files
probe_file_ids = snakemake.params.probe_file_ids
output_file = snakemake.output.output_file



algorithm    = bob.bio.base.algorithm.PCA(subspace_dimension=snakemake.params.pca_dim)

# LOADING PROBES
probes = numpy.array(bob.bio.base.tools.extractor.read_features(probe_files, algorithm, split_by_client=False))

output_file  = snakemake.output.output_file


model      = algorithm.read_model(model_file)


f = open(output_file, 'w')

# write scores in four-column format as string
for i, probe_file in enumerate(probe_files):
    # TODO: hacking here
    probe_id = probe_file_ids[probe_file]
    f.write("%s %s %s %3.8f\n" % (str(model_id), str(probe_id), str(probe_file), algorithm.score(model, probes[i, :])))

