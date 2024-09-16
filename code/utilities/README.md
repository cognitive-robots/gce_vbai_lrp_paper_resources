# Utilities
Contains scripts that fulfil an auxillary function within the context of the paper.

## Evaluate Performance
Calculates performance metrics for each causal scene based upon the links discovered for it before calculating statistics for these metrics.
```
usage: evaluate_performance.py [-h] input_path_expr output_file_path
```
Parameters:
- input_path_expr: Path expression that describes the selection of JSON output files to take as input. Can contain wildcards.
- output_file_path: File path to output performance statistics JSON file to.
- -h: Displays the help message for the script.

## Extract Two Agent Convoy Scenes
Extracts two agent convoy scenes from the highD dataset. Uses a set of conditions in order to determine when two vehicles are in a convoy-like situation and likely to exhibit causal behaviour. The script then randomly selects vehicles in other lanes to act as independent agents.
```
extract_two_agent_convoy_scenes.py [-h] [--csv] [--json-meta] [--trimmed-scene-output-path TRIMMED_SCENE_OUTPUT_PATH] [--velocity-variables] [--all-kinematic-variables] input_directory_path output_directory_path
```
Parameters:
- input_directory_path: Specifies path to directory containing highD data to take as input.
- output_directory_path: Specifies path to directory to output two agent convoy scenario scenes to.
- -h: Displays the help message for the script.
- --csv: Outputs the causal scenarios as CSV formatted timeseries data.
- --json-meta: Outputs the causal scenarios as JSON file with meta data.
- --trimmed-scene-output-path: Outputs the causal scenarios as trimmed versions of the base highD format to the specified output directory.
- --all-kinematic-variables: Includes distance travelled and velocity for all scenario agents as variables in the output scenario. By default only includes acceleration for all scenario agent.
