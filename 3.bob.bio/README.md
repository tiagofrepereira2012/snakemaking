# Snakemake integration with Bob

This is the first example on how to use snakemake with bob.bio.base components.
It's still experimental, but we can have the same output as `verify.py`


```sh
snakemake --snakefile pca.snakemake.py --jobs 100
bob bio evaluate ./PCA-experiment/scores-dev
```


![Alt text](https://g.gravizo.com/source/custom_mark10?https://raw.githubusercontent.com/tiagofrepereira2012/snakemaking/master/3.bob.bio/README.md)
<details><summary></summary>
custom_mark10
digraph snakemake_dag {
    graph[bgcolor=white, margin=0];
    node[shape=box, style=rounded, fontname=sans,                 fontsize=10, penwidth=2];
    edge[penwidth=2, color=grey];
	0[label = "CONCATENATE", color = "0.22 0.6 0.85", style="rounded"];
	1[label = "SCORE", color = "0.56 0.6 0.85", style="rounded"];
	2[label = "ENROLL", color = "0.28 0.6 0.85", style="rounded"];
	3[label = "PROJECT", color = "0.06 0.6 0.85", style="rounded"];
	4[label = "TRAIN", color = "0.61 0.6 0.85", style="rounded"];
	5[label = "EXTRACTOR", color = "0.33 0.6 0.85", style="rounded"];
	6[label = "PREPROCESSING", color = "0.17 0.6 0.85", style="rounded"];
	1 -> 0
	3 -> 1
	2 -> 1
	4 -> 1
	3 -> 2
	5 -> 3
	4 -> 3
	5 -> 4
	6 -> 5
}   
custom_mark10
</details>
