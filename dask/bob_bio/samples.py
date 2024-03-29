#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

from utils import read_biofiles, amend_path, split_data 


class BiometricSamples(object):
    """
    This class stores a set of samples to create a biometric template
    

    Parameters:

      template_id:
        Id of the template

      samples:
        List of `:py:obj:bob.db.base.File`
    """

    def __init__(self, template_id, samples):

        
        self.template_id = template_id
        self.samples = samples


class BiometricProbeSamples(BiometricSamples):
    """

    Parameters:

      template_id:
        Id of the template

      samples:
        List of `:py:obj:bob.db.base.File`

       template_list:
        List of templates where a probe sample is
    """

    def __init__(self, template_id, samples, template_list):
        
        self.template_id = template_id
        self.samples = [samples]
        self.template_list = template_list


def create_biometric_probes(cls, database, templates, group="dev", protocol="Default"):
    """
    Attempt to generate probe objects
    """

    probes = dict()
    for t in templates:
        objects = database.objects(
                protocol=protocol, groups=group, model_ids=(t.template_id,), purposes='probe')
        for o in objects:
            if o.id not in probes:

                o.current_directory = database.original_directory
                o.current_extension = database.original_extension
                o.sample = None

                probes[o.id] = BiometricProbeSamples(o.client_id, o, [])

            probes[o.id].template_list.append(t)

    probes_list = [probes[k] for k in probes]

    return probes_list



def create_biometric_template(cls, database, group="dev", protocol="Default"):
    """
     Factory of Biometric templates.

     The class is meant to interface with `:py:class:bob.db.base.Database` to
     dump BiometricTemplateSample       
    """

    biometric_templates = []
    # TODO: MISSING PROTOCOL
    model_ids = database.model_ids(groups=group)
    for m in model_ids:
        samples = database.objects(
                protocol=protocol, groups=group, model_ids=(m,), purposes='enroll')

        for s in samples:
            s.current_directory = database.original_directory
            s.current_extension = database.original_extension
            s.sample = None


        biometric_template = cls(m, samples)
        biometric_templates.append(biometric_template)
        
    return biometric_templates


def create_training_samples(cls, database, group="dev", protocol="Default"):
    """
     Factory of Biometric templates.

     The class is meant to interface with `:py:class:bob.db.base.Database` to
     dump BiometricTemplateSample       
    """

    # TODO: Maybe organize by client
    biometric_samples = []
    samples = database.objects(
              protocol=protocol, groups='world')

    for s in samples:
        s.current_directory = database.original_directory
        s.current_extension = database.original_extension
        s.sample = None

        biometric_sample = cls(s.client_id, [s])
        biometric_samples.append(biometric_sample)

    return biometric_samples

