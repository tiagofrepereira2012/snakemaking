#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


class SnakemakeDb(object):
    """
    Map bob.db databases to the snakemake pipelines.
    
    This class maps input/outputs for each step in a recognition pipeline as well as
    with their corresponding wildcars.

    TODO: This could be simplified by having only one dictionary and the
    Snakefile takes care herself to orchestrate the dataflow. To be defined
    """

    def __init__(self, db, groups=["dev"]):
        """
        **Parameters**
           database:

        """
        self.preproc_dict = dict() # Map raw data to preprocessed
        self.extract_dict = dict() # Map preprocessed to extracted
        self.project_dict = dict() # Map extracted to projected
        self.enroll_dict = dict()  # Map projected to model files (each class)
        
        self.score_dict  = dict() # Map models files to score files 
        self.model_id_dict = dict() # Map model ids to score files
    
        self.groups     = "dev"
        self.db = db

    def get_1n1_dict(
        self, base_dict, input_dir, output_dir, input_extension, output_extension
    ):
        """
        Generic function to get a 1-1 dict
        """

        if len(base_dict.keys()) > 0:
            return base_dict

        input_files = [
            f.make_path(directory=input_dir, extension=input_extension)
            for f in self.db.training_files() + self.db.enroll_files() + self.db.probe_files()
        ]

        output_files = [
            f.make_path(directory=output_dir, extension=output_extension)
            for f in self.db.training_files() + self.db.enroll_files() + self.db.probe_files()
        ]

        return dict(zip(output_files, input_files))


    def get_wildcard(self, base_dict):
        """
        Generic function to get a wildcard constraint
        """
        return '|'.join(re.escape(x) for x in base_dict.keys())


    def get_preproc_dict(
        self, input_dir, output_dir, input_extension, output_extension
    ):
        """
        """

        self.preproc_dict = self.get_1n1_dict(
            self.preproc_dict, input_dir, output_dir, input_extension, output_extension
        )

        return self.preproc_dict

    def get_preproc_wildcard(self):
        return self.get_wildcard(self.preproc_dict)




    def get_extract_dict(
        self, input_dir, output_dir, input_extension, output_extension
    ):
        """
        """

        self.extract_dict = self.get_1n1_dict(
            self.extract_dict, input_dir, output_dir, input_extension, output_extension
        )

        return self.extract_dict

    def get_extract_wildcard(self):
        return self.get_wildcard(self.extract_dict)



    def get_project_dict(
        self, input_dir, output_dir, input_extension, output_extension
    ):
        """
        """

        self.project_dict = self.get_1n1_dict(
            self.project_dict, input_dir, output_dir, input_extension, output_extension
        )

        return self.project_dict

    def get_project_wildcard(self):
        return self.get_wildcard(self.project_dict)


 
    def get_enroll_wildcard(self):
        return self.get_wildcard(self.enroll_dict)

    def get_enroll_dict(self, input_dir, output_dir, input_extension, output_extension):

        if len(self.enroll_dict.keys())>0:
            return self.enroll_dict

        self.enroll_dict = dict([["{0}/{1}{2}".format(output_dir, model_id, output_extension),
               [f.make_path(directory=input_dir, extension=input_extension)
                 for f in self.db.enroll_files(model_id=int(model_id))
               ]
             ]
             for model_id in self.db.model_ids(groups=self.groups)]
           )

        return self.enroll_dict


    def get_probes(self, input_path, input_extension):
        return [f.make_path(directory=input_path, extension=input_extension) for f in self.db.probe_files()]

    def get_probes_model_id(self, input_path, input_extension):
        probes = self.get_probes(input_path, input_extension)
        ids = [f.client_id for f in self.db.probe_files()]
        return dict(zip(probes, ids))


    def get_score_wildcard(self):
        return self.get_wildcard(self.score_dict)

    def get_score_dict(self, input_dir, output_dir, input_extension, output_extension):

        if len(self.score_dict.keys())>0:
            return self.score_dict

        model_ids = self.db.model_ids(groups=self.groups)
        input_files = [f"{input_dir}/{i}{input_extension}" for i in model_ids]
        output_files = [f"{output_dir}/{self.groups}/{i}{output_extension}" for i in model_ids]
     
        self.score_dict = dict(zip(output_files, input_files))

        self.model_id_dict = dict(zip(input_files, model_ids))

        return self.score_dict, self.model_id_dict

