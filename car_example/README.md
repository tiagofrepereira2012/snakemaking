# Simple snakemake EXAMPLE

Here I created a very simple DAG with 3 nodes.
Basically the two first nodes open a file `cars.csv` and do a simple poly expansion.
The last node compute models for a n-class classification problem by averaging all the poly expanded features for one class.

Follow the code below to reproduce the execution.


```sh
snakemake --snakefile snake-template.rules EXPONENTIAL EXPONENTIAL2 MODELS -f --jobs 2
```
