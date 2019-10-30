#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

"""
create model


Usage:
    create_model.py <input-file> <input-file>... --output-file=<arg>
    create_model.py -h | --help

Options:
  --output-file=<arg>      Output file
  -h --help                Show this screen
"""

import pandas
from docopt import docopt
import numpy
import bob.io.base
import os

def main():

    args = docopt(__doc__, version='')

    models = dict()
    for filename in args["<input-file>"]:
        hdf5 = bob.io.base.HDF5File(filename)

        data   = hdf5.get("data")
        labels  = hdf5.get("labels")
        del hdf5
        
        for l in set(labels):
            m = data[numpy.where(labels==l)].mean(axis=0)

            if f"{l}" in models:
                models[f"{l}"] = numpy.hstack((m, models[f"{l}"])) 
            else:
                models[f"{l}"] = m
    
    hdf5 = bob.io.base.HDF5File(args["--output-file"],"w")
    for k in models:
        hdf5.set(k, models[k])
    del hdf5


if __name__=="__main__":
    main()
