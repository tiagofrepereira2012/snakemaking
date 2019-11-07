#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


class SnakemakeDb(object):
    """
    Map bob.db databases to the snakefile files
    """

    def __init__(self, db, groups=["dev"]):
        """
        **Parameters**
           database:

        """
        self.preproc_dict = dict()
        self.extract_dict = dict()
        self.project_dict = dict()
        self.enroll_dict = dict()
        self.score_dict = dict()

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
            for f in db.training_files() + db.enroll_files() + db.probe_files()
        ]

        output_files = [
            f.make_path(directory=output_dir, extension=output_extension)
            for f in db.training_files() + db.enroll_files() + db.probe_files()
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



