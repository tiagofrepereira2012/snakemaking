___author__ = "Tiago de Freitas Pereira"

import bob.bio.face
import bob.io.base
import numpy



#### FETCHING INPUTS AND OUTPUTS
# A module called snakemake is already imported
input_file = snakemake.input.input_file
output_file = snakemake.output.output_file


preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                              dtype = numpy.float64)


img = bob.io.base.load(input_file)
preprocessed = preprocessor(img)
bob.io.base.save(preprocessed, output_file)


