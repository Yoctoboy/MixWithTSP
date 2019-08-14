## MixWithTSP

A utility to help you to find out the best sequence of songs in a mix using IBM's Cplex optimizer


#### What it is

MixWithTSP takes as input a `.txt` file containing data (BPM, Tonality) about songs as exported by rekordbox. It then computes the best sequence of these songs according to *mixing theory* by trying to minimize a given distance.


#### How to use it

You'll need the CPLEX omptimizer python API installed on your computer to use it.
`git clone` this repo, `cd` into it and run the following command:</br>
`python mixtsp.py <your file> <shifts allowed>`


#### Current Features

- Allow some tracks to be shifted by one or more semitones (is penalized by the objective function)

- Allow the optimizer to not include one or more songs in the output mix


#### More to come

- Finding out the *ambiance* of a given sound, and take it into account for even smoother mixes
- Using AI, Feature Extraction and rhythm detection to actually create a mix, with the transitions (and maybe even some effects)
- Remove proprietary solver CPlex in the dependencies of this project and use GLPK or CVXPY instead
