"""
Some util functions
"""



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
      return [loader(o.make_path(o.current_directory, o.current_extension)) for o in objects]

