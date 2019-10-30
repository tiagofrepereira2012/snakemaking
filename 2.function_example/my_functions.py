#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

"""
Functions example

"""

import pandas
from docopt import docopt
import numpy
import bob.io.base
import os

def exponential(input_file, output_file, degree=2):

    dataset = pandas.read_csv(input_file)
    data_numpy = dataset.to_numpy()[:, 0:-2].astype("float64")
    labels = dataset.to_numpy()[:, -1].astype("str")
    for i,l in enumerate(set(labels)):
        labels[numpy.where(labels==l)[0]] = i
    labels = labels.astype("uint8")

    base = data_numpy
    for i in range(1,degree):
        data_numpy = numpy.hstack((data_numpy,base**i))
   

    hdf5 = bob.io.base.HDF5File(output_file,"w")
    hdf5.set("data", data_numpy)
    hdf5.set("labels", labels)
    del hdf5


def create_models(input_files, output_file):

    models = dict()
    for filename in input_files:
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
    
    hdf5 = bob.io.base.HDF5File(output_file,"w")
    for k in models:
        hdf5.set(k, models[k])
    del hdf5

