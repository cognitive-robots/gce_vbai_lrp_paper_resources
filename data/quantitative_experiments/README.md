# Quantitative Experiments
Here we provide the output data and results from the quantitative experiments carried out on the extracted highD scenes. The proposed methods was intentionally designed to take similar input and give similar output to SimCARS and thus these two methods share a similar file structure here. All the other approaches were evaluated upon a fork of another repository (https://github.com/ckassaad/causal_discovery_for_time_series) with additional extensions, and thus follow a different file structure. Note that we will include a reference to this forked repository as a submodule of the GitHub repository mentioned in the top-level README.

## Proposed Method / SimCARS
These directories have the following structure:
- {threshold}/scene-{scene}-{follower}_follows_{followed}-{independent}_independent.json: A file containing the output data comprised of causal links. The naming convention is based upon the following variables:
    * threshold: The threshold utilised for this set of experiments. This corresponds to the action distance threshold for the proposed method and the reward difference threshold for SimCARS.
    * scene: The recording id of the scene.
    * follower: The rear vehicle in the two convoy scenario of the scene.
    * followed: The front vehicle in the two convoy scenario of the scene.
    * independent: The number of independent vehicles included in the scene.
- {threshold}_evaluation.json: Provides the precision, recall, fallout, F1 score, and execution time statistics across all the scene output data contained in the correspondingly named subdirectory. The variable "threshold" is determined as above.

## Other Methods
These directories have the following structure:
- graphs/{var}/{max_time_lag}/{p_val}/{method}_{i}: The output data in the form of a graph, represented via networkx and stored to file via pickling. The naming convention is based upon the following variables:
    * var: The variable of the vehicles utilised with the method. Either "acceleration" or "velocity".
    * max_time_lag: The maximum time lag value used for the method.
    * p_val: The p-value used in the method.
    * method: The method used. Either "GrangerMV", "Dynotears", "TiMINo", or "Random".
    * i: The number of the scene.
- performance_average/{var}/{max_time_lag}/{p_val}.txt: Provides the precision, recall, fallout, F1 score, and execution time statistics across all the scenes. Variables are determined as above.
- performance_detail/{var}/{max_time_lag}/{p_val}.txt: Provides the precision, recall, fallout, F1 score, and execution time statistics across each scene --- with one scene per row / line. Variables are determined as above.

Lastly, given that the "Random" method does not rely upon any parameters its directory structure has been simplified accordingly. The above description should prove sufficient in navigating its contents however.
