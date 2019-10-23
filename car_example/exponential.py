#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

"""
Dump exponential features


Usage:
    exponential.py <input-path> <output-path> [--degree=<arg>]
    exponential.py -h | --help

Options:
  --degree=<arg>   Degree of the polynomium  [default: 2]
  -h --help        Show this screen
"""

import pandas
from docopt import docopt
import numpy
import bob.io.base
import os

def main():

    args = docopt(__doc__, version='')

    dataset = pandas.read_csv(args["<input-path>"])

    data_numpy = dataset.to_numpy()[:, 0:-2].astype("float64")
    labels = dataset.to_numpy()[:, -1].astype("str")
    for i,l in enumerate(set(labels)):
        labels[numpy.where(labels==l)[0]] = i
    labels = labels.astype("uint8")

    base = data_numpy
    for i in range(1,int(args["--degree"])):
        data_numpy = numpy.hstack((data_numpy,base**i))
   

    hdf5 = bob.io.base.HDF5File(args["<output-path>"],"w")
    hdf5.set("data", data_numpy)
    hdf5.set("labels", labels)
    del hdf5


if __name__=="__main__":
    main()
