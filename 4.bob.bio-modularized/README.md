# Snakemake integration with Bob - Modularized

In this example I'll try to modularize the previous example `../3.bob.bio`
using `https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#modularization`.

Here I'm imagining one set of rules for each bob.bio.[preprocessor, extractor, algorithm], and those can be anything e.g (python entrypoint scripts, binaries, python functions, ...).
The configuration of the experiment is defined in the `Snakefile` file, where all the rules are binded together.

So far I haven't defined conda envs per rule, hence, you'll need to create the conda env yourself.
Run the code below to execute the experiment.


```sh
conda env create -f envs/env.yml
conda activate snakemaking

snakemake --jobs 100 all
bob bio evaluate ./PCA-experiment/scores-dev
```

Follow the DAG of the experiment:

![Alt text](https://g.gravizo.com/source/custom_mark10?https://raw.githubusercontent.com/tiagofrepereira2012/snakemaking/master/4.bob.bio-modularized/README.md)
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
