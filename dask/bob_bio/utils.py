"""
Some util functions
"""
import numpy


def read_biofiles(objects, loader, split_by_client = False, allow_missing_files = False):
  """read_features(file_names, extractor, split_by_client = False) -> extracted

  Reads the extracted features from ``file_names`` using the given ``extractor``.
  If ``split_by_client`` is set to ``True``, it is assumed that the ``file_names`` are already sorted by client.

  **Parameters:**

  file_names : [str] or [[str]]
    A list of names of files to be read.
    If ``split_by_client = True``, file names are supposed to be split into groups.

  extractor : py:class:`bob.bio.base.extractor.Extractor` or derived
    The extractor, used for reading the extracted features.

  split_by_client : bool
    Indicates if the given ``file_names`` are split into groups.

  allow_missing_files : bool
    If set to ``True``, extracted files that are not found are silently ignored.

  **Returns:**

  extracted : [object] or [[object]]
    The list of extracted features, in the same order as in the ``file_names``.
  """
  #file_names = utils.filter_missing_files(file_names, split_by_client, allow_missing_files)

  if split_by_client:
      return [[extractor.read_feature(f) for f in client_files] for client_files in file_names]
  else:
      return numpy.vstack([loader(s.make_path(s.current_directory, s.current_extension)).astype("float64") if s.sample is None else s.sample for o in objects for s in o.samples  ])



def amend_path(objects, path, extension):
    for o in objects:
        o.current_directory = path
        o.current_extension = extension
        o.sample = None
    return objects



def split_data(input_data, n_groups):
    """
    Given a list of elements, split them in a particular number of groups
    This is useful for paralellization
    """

    offset=0
    # Number of elements per groups
    step = len(input_data)//n_groups

    output_data = []
    for i in range(n_groups):
        output_data.append(input_data[offset:offset+step])
        offset += step
    

    return output_data

