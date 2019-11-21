import bob.bio.face
import bob.bio.base
import bob.io.base
import numpy
import re


def compute(executor, input_file, output_file):
    img = bob.io.base.load(input_file)
    preprocessed = executor(img)
    bob.io.base.save(preprocessed, output_file)

def load(file_names, extractor):
    return bob.bio.base.tools.extractor.read_features(file_names,
            extractor,
            split_by_client=False
            )


