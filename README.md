## MixWithTSP

A utility for finding out the best sequence of songs in a mix using IBM's Cplex optimizer


#### What it is

MixWithTSP takes as input a `.txt` file containing data (BPM, Tonality) about songs as exported by rekordbox. It then computes the best sequence of these songs according to *mixing theory* by trying to minimize a given distance.


#### Current Features

- Allow some tracks to be shifted by one or more semitones (is penalized by the objective function)

- [IN PROGRESS] Allow the optimizer to not include one or more songs in the output mix


#### More to come

- Finding out the *ambiance* of a given sound, and take into account for even smoother mixes
- Using AI, Feature Extraction and rhythm detection to actually create a mix, with the transitions (and maybe even some effects)
