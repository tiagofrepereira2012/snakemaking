#### DEFINITION OF THE EXPERIMENT
workflow.configfile( "config.yaml"
)
workflow.workdir( "PCA-experiment"
)


### SOME BASE FUNCTIONS

import bob . io . base
import bob . bio . base
import bob . bio . face
import numpy

def load ( file_names , extractor ) :
				return bob . bio . base . tools . extractor . read_features ( file_names ,
				extractor ,
				split_by_client = False
				)

				####
				# Database
				####

db = bob . bio . face . database . AtntBioDatabase ( )


## Creating my input function

def input_fn ( reading_function , path , extension ) :
				return reading_function ( )
				#return [ f.make_path(path, extension) for f in reading_function() ]


				###################
				# PREPROCESSING
				###################


test_dict = dict ( zip (
input_fn ( db . training_files , "preprocessed" , ".hdf5" ) +
input_fn ( db . probe_files , "preprocessed" , ".hdf5" ) ,

input_fn ( db . training_files , config [ "database_path" ] , config [ "database_extension" ] ) +
input_fn ( db . probe_files , config [ "database_path" ] , config [ "database_extension" ] )
) )

workflow.global_wildcard_constraints(
				output_card = '|' + '|' . join ( input_fn ( db . training_files , "preprocessed" , ".hdf5" ) ) +
																		'|' + '|' . join ( input_fn ( db . probe_files , "preprocessed" , ".hdf5" ) )

)
@workflow.rule(name='all', lineno=53, snakefile='/local/scratch/tpereira/github/snakemaking/5.bob.bio.dbs/Snakefile')

@workflow.input(
				input_fn ( db . training_files , "preprocessed" , ".hdf5" ) +
				input_fn ( db . probe_files , "preprocessed" , ".hdf5" )


)
@workflow.norun()
@workflow.run
def __rule_all(input, output, params, wildcards, threads, resources, log, version, rule, conda_env, singularity_img, singularity_args, use_singularity, bench_record, jobid, is_shell, bench_iteration, shadow_dir):
	pass
@workflow.rule(name='PREPROCESSING', lineno=65, snakefile='/local/scratch/tpereira/github/snakemaking/5.bob.bio.dbs/Snakefile')

@workflow.input(
				input_file = lambda wc : test_dict [ wc . output_card ]

)

@workflow.output(
				output_file = '{output_card}'

)
@workflow.wrapper (
# define the preprocessor
#
				"file://../wrappers/bob.bio.face/preprocessor/base/"


)
@workflow.run
def __rule_PREPROCESSING(input, output, params, wildcards, threads, resources, log, version, rule, conda_env, singularity_img, singularity_args, use_singularity, bench_record, jobid, is_shell, bench_iteration, shadow_dir):
	wrapper ( "file://../wrappers/bob.bio.face/preprocessor/base/" , input, output, params, wildcards, threads, resources, log, config, rule, conda_env, singularity_img, singularity_args, bench_record, workflow.wrapper_prefix, jobid, bench_iteration, shadow_dir
) 

