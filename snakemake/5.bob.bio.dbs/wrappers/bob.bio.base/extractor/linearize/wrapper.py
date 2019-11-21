__author__ = "Tiago de Freitas Pereira"


import bob.bio.base


extractor = bob.bio.base.extractor.Linearize()


input_file = snakemake.input.input_file
output_file = snakemake.output.output_file


img = bob.io.base.load(input_file)
extracted = extractor(img)
bob.io.base.save(extracted, output_file)

