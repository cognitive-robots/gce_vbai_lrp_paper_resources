# Qualitative Experiments
Here we provide videos of the three scenarios discussed in the qualitative experiments. The file naming convention is as follows:
```
{type}_{dataset}_{scene}_{start}_{end}_{causing_agent}_{causing_action}_{affected_agent}_{affected_action}_{other_causing_agents}.mp4
```
where each variable --- indicated via braces --- is substituted as described here:
- type: "vis", "sim", "alt", or "combined" to reflect the video depicting either the raw observation, simulation with causing action, simulation without causing action, or all three combined respectively.
- dataset: "highd", "ind", or "exid" depending upon the dataset the depicted scene is taken from.
- scene: The recording id of the scene depicted.
- start: The start frame of the scene depicted.
- end: The end frame of the scene depicted.
- causing_agent: The agent id of the causing agent in the scene depicted.
- causing_action: The causing action of the causing agent in the scene depicted.
- affected_agent: The agent id of the affected agent in the scene depicted.
- affected_action: The affected action of the affected agent in the scene depicted.
- other_causing_agents: Ids of other agents that have some causal effect upon the affected agent. Each id is separated by an underscore. This is just used for visualisation purposes and is entirely optional.
