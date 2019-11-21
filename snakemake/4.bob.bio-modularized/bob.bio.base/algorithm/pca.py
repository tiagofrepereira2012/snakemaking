import bob.bio.base
import re

BACKGROUND_MODEL_FILE = "projector.hdf5"

algorithm = bob.bio.base.algorithm.PCA(subspace_dimension=0.95)


################
# TRAIN BACKGROUND
################


rule TRAIN:
    input:        
        input_file = TRAINING_EXTRACTED_DATA
    output:
        output_file = BACKGROUND_MODEL_FILE
    run:
        features = load(input.input_file, extractor)
        algorithm.train_projector(features, output.output_file)



###########
# PROJECT
###########


projected_dict = dict(zip(ENROLL_PROJECTED_DATA+PROBE_PROJECTED_DATA, ENROLL_EXTRACTED_DATA+PROBE_EXTRACTED_DATA))

# define the preprocessor
wildcard_constraints:
    z = '|'.join(re.escape(z) for z in ENROLL_PROJECTED_DATA+PROBE_PROJECTED_DATA)


rule project_all:
    input:
        expand('{z}', z=ENROLL_PROJECTED_DATA+PROBE_PROJECTED_DATA)


rule PROJECT:
    input: 
        input_file = lambda wc: projected_dict[wc.z],
        projected_file = BACKGROUND_MODEL_FILE
    output:
        output_file='{z}',
    run:
        
        algorithm.load_projector(input.projected_file)
        compute(algorithm.project,input.input_file, output.output_file)




###########
# ENROLL
##########


wildcard_constraints:
    k = '|'.join(re.escape(k) for k in MODELS)


rule enroll_all:
    input:
        expand('{k}', k=MODELS)

rule ENROLL:
    input: 
        input_file = lambda wc: ENROLL_DATA[wc.k]
    output:
        output_file='{k}'
    run:
        features = load(input.input_file, extractor)        
        model = algorithm.enroll(features)
        bob.io.base.save(model, output.output_file)


#############
# SCORING
############


scores_dict = dict(zip(SCORES, MODELS))

wildcard_constraints:
    y = '|'.join(re.escape(y) for y in SCORES)


rule score_all:
    input:
        expand('{y}', y=SCORES)

rule SCORE:
    input: 
        input_file = lambda wc: scores_dict[wc.y],
        probe_files = PROBE_PROJECTED_DATA,
        projected_file = BACKGROUND_MODEL_FILE
    output:
        output_file='{y}'
    run:
        algorithm.load_projector(input.projected_file)
        model = algorithm.read_model(input.input_file)
        probes = load(input.probe_files, extractor)        
        scores = [algorithm.score(model, p) for p in probes]

        f = open(output.output_file, 'w')

        # write scores in four-column format as string
        for i, probe_file in enumerate(input.probe_files):
            # TODO: hacking here
            model_id = os.path.splitext(input.input_file)[0].split("/")[-1]
            probe_id = os.path.splitext(probe_file)[0].split("/")[-2]
            f.write("%s %s %s %3.8f\n" % (str(model_id), str(probe_id), str(probe_file), scores[i]))


### MAIN RULE
rule all:
    input: 
        input_file = SCORES
    output:
        output_file=f'scores-{group}'
    run:
        f = open(output.output_file, 'w')
        for i in input.input_file:
            f.write(open(i).read())

