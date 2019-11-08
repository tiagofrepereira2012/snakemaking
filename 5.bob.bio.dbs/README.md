# Snakemake integration with Bob dbs

This example contains a possible integration between Bob and [Snakemake](https://snakemake.readthedocs.io).
The main point of this example is to reuse [bob.dbs](https://www.idiap.ch/software/bob/docs/bob/docs/stable/#database-interfaces>) to provide data for generic rules.
This integration is crafted [here](https://github.com/tiagofrepereira2012/snakemaking/blob/master/5.bob.bio.dbs/snakemakedb.py).

Here we are using the following Snakemake features:

  - [Configuration files](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html) to parametrize an experiment
  - [Wildcards](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#wildcards) to abstract and distribute one rule into several jobs
  - [Wrappers](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#wrappers) to modularized better re-use rules.

 
The usage plan for someone that is interested to use Snakemake+Bov would be:

  1. Each one create its own Snakefile with their own rules either by crafting it from scratch or by branching it from a template. We could have a repository of Snakefiles.

  2. Users are encouraged to craft rules as simple as possible by implementing the logic of the rules using Snakemake wrappers.

  3. Whatever necessary parametrization can be crafted using configurations using the `config.yml` file.



To run this example do the following steps


```sh
conda env create -f envs/env.yml
conda activate snakemaking
snakemake all --configfile config.yaml
```


