import bob.bio.face
import bob.bio.base

path = "/idiap/group/biometric/databases/biometrics/face2D/orl/"
db = bob.bio.face.database.AtntBioDatabase()

group = "dev"

TRAIN_DATA = [f.make_path(directory=path, extension=".pgm") for f in db.training_files()]

DATA_ENROLL = dict()
for m in db.model_ids(groups=group):
    DATA_ENROLL[m] = db.enroll_files(model_id=m)

 DATA_PROBE = db.probe_files(groups=group)


