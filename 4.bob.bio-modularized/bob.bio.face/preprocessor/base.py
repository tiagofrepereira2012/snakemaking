import bob.bio.face
import re

#########
# TOOLS
########
preprocessor = bob.bio.face.preprocessor.Base(color_channel="gray",
                                              dtype = numpy.float64)

###################
# PREPROCESSING
###################


preprocessed_dict = dict(zip(ALL_PREPROCESSED_DATA, ALL_RAW_DATA))

# define the preprocessor
wildcard_constraints:
    x = '|'.join(re.escape(x) for x in ALL_PREPROCESSED_DATA)


rule preprocess_all:
    input:
        expand('{x}', x=ALL_PREPROCESSED_DATA)


rule PREPROCESSING:
    input:
        input_file = lambda wc: preprocessed_dict[wc.x]
    output:
        output_file = '{x}'
    run:
        # define the preprocessor
        compute(preprocessor, input.input_file, output.output_file)

