# Snakemake integration with Bob dbs

This example contains a possible integration between Bob and [Snakemake](https://snakemake.readthedocs.io).
The main point of this example is to reuse [bob.dbs](https://www.idiap.ch/software/bob/docs/bob/docs/stable/#database-interfaces>) to provide data for generic rules.
This integration is crafted [here](https://github.com/tiagofrepereira2012/snakemaking/blob/master/5.bob.bio.dbs/snakemakedb.py).

Here we are using the following Snakemake features:

  - [Configuration files](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html) to parametrize an experiment
  - [Wildcards](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#wildcards) to abstract and distribute one rule into several jobs
  - [Wrappers](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#wrappers) to modularized better re-use rules.

 
The usage plan for someone that is interested to use Snakemake+Bob would be:

  1. Each one create its own Snakefile with their own rules either by crafting it from scratch or by branching it from a template. We could have a repository of Snakefiles.

  2. Users are encouraged to craft rules as simple as possible by implementing the logic of the rules using Snakemake wrappers.

  3. Whatever necessary parametrization can be crafted using configurations using the `config.yml` file.



To run this example do the following steps


```sh
conda env create -f envs/env.yml
conda activate snakemaking
snakemake all --configfile config.yaml
```

This represents the following toolchain:


![Alt text](https://g.gravizo.com/source/custom_mark10?https://raw.githubusercontent.com/tiagofrepereira2012/snakemaking/master/5.bob.bio.dbs/README.md)
<details><summary></summary>
custom_mark10
digraph snakemake_dag {
    graph[bgcolor=white, margin=0];
    node[shape=box, style=rounded, fontname=sans,                 fontsize=10, penwidth=2];
    edge[penwidth=2, color=grey];
	0[label = "all", color = "0.28 0.6 0.85", style="rounded"];
	1[label = "SCORE", color = "0.17 0.6 0.85", style="rounded"];
	2[label = "ENROLL", color = "0.11 0.6 0.85", style="rounded"];
	3[label = "PROJECT", color = "0.44 0.6 0.85", style="rounded"];
	4[label = "TRAIN", color = "0.33 0.6 0.85", style="rounded"];
	5[label = "EXTRACTOR", color = "0.50 0.6 0.85", style="rounded"];
	6[label = "PREPROCESSING", color = "0.06 0.6 0.85", style="rounded"];
	1 -> 0
	4 -> 1
	2 -> 1
	3 -> 1
	3 -> 2
	5 -> 3
	4 -> 3
	5 -> 4
	6 -> 5
}
custom_mark10
</details>


## Drawbacks of the current way to approach things

There are two main drawbacks on the way that snakemake handled things.

The **first** main drawback is the way that parallelization is handled.
Data parallelization in snakemake is handled with wildcards and with respect to this feature, there are two major things that can create problems in the future.
 1. Intuition of such feature. Although wildcards is a powerfull feature, to craft one for our needs is not very intuitive. We would need lots of examples to make this clear to every one.

 2. Efficiency. As soon as you have a match (regular expression match) using wildcards, snakemake creates a `Job`. If you have 1000 matches, you'll have 1000 jobs and if your job has some overhead (like loading a heavy model) this can be very inneficient. Would be nice to be able to approach it like `bob.bio.base` does.

The **second** main drawback is the way inputs and output are handled.
Everything is "path" based.
For instance, it's not possible to send a "samples" to a rule.
We could branch Snakemake.rules to introduce the concept of sample.
A sample could be anything, such as, numpy.arrays, pandas data frames, and many other things.
This would make snakemake more robust.






