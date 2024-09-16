#!/usr/bin/python3

import copy
import os
import argparse
import json
import glob
import statistics


def calculate_scene_performance(causal_links, total_possible_links):
    tp_count = 0
    fp_count = 0
    fn_count = 0

    tp_links = {}
    fp_links = {}

    for cause_str in causal_links:
        cause_id = int(cause_str)
        effect_ids = causal_links[cause_str]
        for effect_str in effect_ids:
            effect_id = int(effect_str)
            if ((cause_id == convoy_head_id or cause_id == convoy_tail_id) and
                    (effect_id == convoy_head_id or effect_id == convoy_tail_id)):
                if tp_links.get(effect_id) is not None and tp_links[effect_id].get(cause_id) is not None:
                    tp_links[effect_id][cause_id] += 1
                else:
                    tp_links[cause_id] = { effect_id: 1 }
            else:
                if fp_links.get(effect_id) is not None and fp_links[effect_id].get(cause_id) is not None:
                    fp_links[effect_id][cause_id] += 1
                else:
                    fp_links[cause_id] = {effect_id: 1}

    for cause in tp_links:
        for effect in tp_links[cause]:
            tp_count += 1

    for cause in fp_links:
        for effect in fp_links[cause]:
            fp_count += 1

    if tp_count == 0:
        fn_count += 1

    tn_count = total_possible_links - (tp_count + fp_count + fn_count)

    return tp_count, fp_count, fn_count, tn_count


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("input_path_expr")
arg_parser.add_argument("output_file_path")
args = arg_parser.parse_args()

total_tp_count = 0
total_fp_count = 0
total_fn_count = 0
total_tn_count = 0

execution_times = []

for input_file_path in glob.glob(args.input_path_expr):
    input_file_basename = os.path.basename(input_file_path)

    with open(input_file_path, "r") as input_file:
        causal_discovery_json = json.load(input_file)

        convoy_head_id = causal_discovery_json["convoy_head_id"]
        convoy_tail_id = causal_discovery_json["convoy_tail_id"]
        independent_ids = causal_discovery_json["independent_ids"]

        n = 2 + len(independent_ids)
        total_possible_links = int((n * (n - 1)) / 2)

        current_causal_links = causal_discovery_json["causal_links"]

        current_tp_count, current_fp_count, current_fn_count, current_tn_count = calculate_scene_performance(current_causal_links, total_possible_links)

        total_tp_count += current_tp_count
        total_fp_count += current_fp_count
        total_fn_count += current_fn_count
        total_tn_count += current_tn_count

        execution_times.append(causal_discovery_json["time_elapsed_in_microseconds"] / 1.0e6)


if total_tp_count + total_fp_count == 0:
    precision = 0
else:
    precision = total_tp_count / (total_tp_count + total_fp_count)

fallout = total_fp_count / (total_fp_count + total_tn_count)

recall = total_tp_count / (total_tp_count + total_fn_count)

f1_score = (2 * total_tp_count) / (2 * total_tp_count + total_fp_count + total_fn_count)

execution_times_mean = statistics.mean(execution_times)
execution_times_stdev = statistics.stdev(execution_times)


with open(args.output_file_path, "w") as output_file:
    performance_evaluation_json = {
        "precision": precision,
        "fallout": fallout,
        "recall": recall,
        "f1_score": f1_score,
        "execution_time": {
            "mean": execution_times_mean,
            "stdev": execution_times_stdev
        }
    }
    json.dump(performance_evaluation_json, output_file)
