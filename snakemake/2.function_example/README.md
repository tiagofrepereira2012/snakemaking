# Snakemake simple example using functions


Here I created a very simple DAG with 3 nodes.
Basically the two first nodes open a file `cars.csv` and do a simple poly expansion.
The last node compute models for a n-class classification problem by averaging all the poly expanded features for one class.

**Differently from the one in `../car_example`, here I'm calling functions directly to execute the above functions.**


Follow the code below to reproduce the execution.


```sh
snakemake --snakefile snake-template.rules EXPONENTIAL EXPONENTIAL2 MODELS -f --jobs 2
```

This runs the very stupid example below:


![Alt text](https://g.gravizo.com/source/custom_mark10?https://raw.githubusercontent.com/tiagofrepereira2012/snakemaking/master/2.function_example/README.md)
<details><summary></summary>
custom_mark10
digraph snakemake_dag {
    graph[bgcolor=white, margin=0];
    node[shape=box, style=rounded, fontname=sans,                 fontsize=10, penwidth=2];
    edge[penwidth=2, color=grey];
	0[label = "EXPONENTIAL2", color = "0.00 0.6 0.85", style="rounded"];
	1[label = "EXPONENTIAL", color = "0.22 0.6 0.85", style="rounded"];
	2[label = "CREATE_MODELS", color = "0.44 0.6 0.85", style="rounded"];
	1 -> 2
	0 -> 2
} 
custom_mark10
</details>

