# The search for new workflow framework


## Preamble

I'm in a quest to find the most suitable workflow framework for daily usage in the group I work, where we are basically focused in pattern recognition tasks (mostly biometrics related).
We've developed a framework in house called [bob.bio.base](https://gitlab.idiap.ch/bob/bob.bio.base) to handle this task for us, which was very useful and successful while we were handling only with biometric recognition tasks **NOT** deep learning based.
In easy terms, this framework is composed by one single workflow that handles all possible biometric **recognition** related tasks.
It seems very unflexible, but by using a very defined API, it is possible to run all different sorts of biometric recognition experiment.
It has some advantages such as:

 1. Integration with our grid SGE
 2. Transparent paralellization of the inputs
 3. We already have some critical mass of algoritms there.
 4. We have way of handling database protocols that makes it transparent to test our workflow in different databases.

However, the amount of disadvanteges are growing along the years and we are loosing the tool.
For instance we had to:

 1. Branch `bob.bio.base` for new tasks. For instance, we have [bob.pad.base](https://gitlab.idiap.ch/bob/bob.pad.base), [diarization](?), 
 2. Create specific components outside of the tool to handle the training of deep neural networks.
 3. Very few people understand what is going inside of this hard-coded toolchain. This is a blocking for newcomers.
    Basically, the rule of the thumb is; if you don't understand something, you do it from scratch in your own way.


## What are the desired features for a workflow framework ?


We need a way to handle these workflows in a way that: 1-) the legacy of someone that passed by the group is maximized, 2-) easy for people to **COLABORATE** -) easy to build something new and 4-) scalable with the resources we have.
It seems that the direction is to find a third-party workflow framework that handle this stuff for us.
In this direction, follow possible desired features for a new workflow compoents that are desirable for us as a group.
A new workflow framework should:

 1. Be python based (we don't want to manage a tool in another programming language)
 2. Support paralellization of the inputs. Optimized parallelization given the number of resources we have is a plus.
 3. Support distributed execution. SGE first, other cluster engines is a plus.
 4. Be I/O isolated. Would be desirable to have a tool that allows I/O to be handled in a separared component.
 5. Easy to craft any type of workflow (I know, this is very subjective)
 6. Maintained, with: version control, bug-tracker, CI and with some activity
 7. Easy to configure eventual hyperparameters
 8. Easy to reuse components (DRY friendly)
 9. Documentation API


We have looked some tools and follow bellow a longitudinal analysis of some:



| Tool                 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|:--------------------:|---|---|---|---|---|---|---|---|---|
| Snakemake            | Y | C | Y | N | Y | Y | Y | C | C |
| Luigi                | Y | N | N | ? | Y | Y | C | ? | ? |
| Kedro                | Y | N | N | Y | C | C | Y | C | N |
| Parsl                |   |   |   |   |   |   |   |   |   |

**Y** stands for yes, **C** stands for yes, but with some constraints and **N** for no.




## Subjective analisys

### Snakemake

### Luigi

### Kedro

It seems that kedro is better made.
It has a nice I/O isolation.

, but with several level of complications


https://github.com/quantumblacklabs/kedro/issues/123

It's not very sample oriented


DEPENDENCIES VIA KEYWORDS


### Parl



Can I pass any Python object between apps?

No. Unfortunately, only picklable objects can be passed between apps. For objects that can’t be pickled, it is recommended to use object specific methods to write the object into a file and use files to communicate between apps.


