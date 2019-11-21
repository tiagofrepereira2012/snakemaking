import bob.bio.base
import re

extractor = bob.bio.base.extractor.Linearize()

################
# EXTRACTOR
################


extracted_dict = dict(zip(ALL_EXTRACTED_DATA, ALL_PREPROCESSED_DATA))

# define the preprocessor
wildcard_constraints:
    y = '|'.join(re.escape(y) for y in ALL_EXTRACTED_DATA)


rule extract_all:
    input:
        expand('{y}', y=ALL_EXTRACTED_DATA)


rule EXTRACTOR:
    input:        
        input_file = lambda wc: extracted_dict[wc.y]
    output:
        output_file='{y}'
    run:        
        compute(extractor, input.input_file, output.output_file)

