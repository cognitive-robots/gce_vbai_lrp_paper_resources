#!/usr/bin/python3

import argparse
import os
import shutil
import csv
import json
import numpy as np

minimum_time_window_threshold = 10.0
maximum_convoy_distance_headway_threshold = 10.0
minimum_clearance_distance_headway_threshold = 20.0
velocity_proportional_diff_threshold = 0.2



def output_to_file_csv(first_frame, last_frame, followed_frames, follower_frames, independent_frames_dict, output_file_path, velocity_variables, all_kinematic_variables):
    print(f"Generating output for {output_file_path}")

    if all_kinematic_variables:
        field_names = ["c0.a", "c0.v", "c0.p", "c1.a", "c1.v", "c1.p"]
        for i in range(len(independent_frames_dict)):
            field_names.append(f"i{i}.a")
            field_names.append(f"i{i}.v")
            field_names.append(f"i{i}.p")
    elif velocity_variables:
        field_names = ["c0.v", "c1.v"]
        for i in range(len(independent_frames_dict)):
            field_names.append(f"i{i}.v")
    else:
        field_names = ["c0.a", "c1.a"]
        for i in range(len(independent_frames_dict)):
            field_names.append(f"i{i}.a")

    with open(output_file_path, "w") as output_file:
        field_names = ["time_index"] + field_names
        csv_writer = csv.DictWriter(output_file, fieldnames=field_names)
        csv_writer.writeheader()

        followed_distance_travelled = None
        follower_distance_travelled = None
        independent_distance_travelled = None
        for i, (followed_frame, follower_frame) in enumerate(zip(followed_frames, follower_frames)):
            row = { "time_index": i }

            if all_kinematic_variables:
                row["c0.a"] = float(followed_frame["xAcceleration"])
                row["c1.a"] = float(follower_frame["xAcceleration"])
                for j, independent_id in enumerate(independent_frames_dict.keys()):
                    row[f"i{j}.a"] = float(independent_frames_dict[independent_id][i]["xAcceleration"])

                row["c0.v"] = float(followed_frame["xVelocity"])
                row["c1.v"] = float(follower_frame["xVelocity"])
                for j, independent_id in enumerate(independent_frames_dict.keys()):
                    row[f"i{j}.v"] = float(independent_frames_dict[independent_id][i]["xVelocity"])

                followed_position = np.array((float(followed_frame["x"]), float(followed_frame["y"])))
                if followed_distance_travelled is None:
                    followed_distance_travelled = 0
                else:
                    followed_distance_travelled += np.linalg.norm(followed_position - followed_previous_position)
                row["c0.p"] = followed_distance_travelled
                followed_previous_position = followed_position

                follower_position = np.array((float(follower_frame["x"]), float(follower_frame["y"])))
                if follower_distance_travelled is None:
                    follower_distance_travelled = 0
                else:
                    follower_distance_travelled += np.linalg.norm(follower_position - follower_previous_position)
                row["c1.p"] = follower_distance_travelled
                follower_previous_position = follower_position

                for j, independent_id in enumerate(independent_frames_dict.keys()):
                    independent_position = np.array((float(independent_frames_dict[independent_id][i]["x"]),
                                                     float(independent_frames_dict[independent_id][i]["y"])))
                    if independent_distance_travelled is None:
                        independent_distance_travelled = 0
                    else:
                        independent_distance_travelled += np.linalg.norm(independent_position - independent_previous_position)
                    row[f"i{j}.p"] = independent_distance_travelled
                    independent_previous_position = independent_position
            elif velocity_variables:
                row["c0.v"] = float(followed_frame["xVelocity"])
                row["c1.v"] = float(follower_frame["xVelocity"])
                for j, independent_id in enumerate(independent_frames_dict.keys()):
                    row[f"i{j}.v"] = float(independent_frames_dict[independent_id][i]["xVelocity"])
            else:
                row["c0.a"] = float(followed_frame["xAcceleration"])
                row["c1.a"] = float(follower_frame["xAcceleration"])
                for j, independent_id in enumerate(independent_frames_dict.keys()):
                    row[f"i{j}.a"] = float(independent_frames_dict[independent_id][i]["xAcceleration"])

            csv_writer.writerow(row)



def output_to_file_json_meta(scene_id, convoy_head_id, convoy_tail_id, independent_ids, output_file_path):
    print(f"Generating output for {output_file_path}")

    json_dict = {
        "scene_id": scene_id,
        "convoy_head_id": convoy_head_id,
        "convoy_tail_id": convoy_tail_id,
        "independent_ids": independent_ids
    }

    with open(output_file_path, "w") as output_file:
        json.dump(json_dict, output_file)


arg_parser = argparse.ArgumentParser(description="Extracts two agent convoy scenes from the High-D dataset")
arg_parser.add_argument("input_directory_path")
arg_parser.add_argument("output_directory_path")

arg_parser.add_argument("--csv", action="store_true")
arg_parser.add_argument("--json-meta", action="store_true")

arg_parser.add_argument("--trimmed-scene-output-path")

arg_parser.add_argument("--velocity-variables", action="store_true")
arg_parser.add_argument("--all-kinematic-variables", action="store_true")
args = arg_parser.parse_args()

if not os.path.isdir(args.input_directory_path):
    raise ValueError(f"Input directory path {args.input_directory_path} is not a valid directory")

if not os.path.isdir(args.output_directory_path):
    raise ValueError(f"Output directory path {args.output_directory_path} is not a valid directory")

if args.trimmed_scene_output_path is not None and not os.path.isdir(args.trimmed_scene_output_path):
    raise ValueError(f"Trimmed scene output directory path {args.trimmed_scene_output_path} is not a valid directory")

if not args.csv and not args.json_meta:
    raise ValueError("Please select either CSV or JSON meta output mode")

scene_count = int(len(os.listdir(args.input_directory_path)) / 4)

for i in range(1, scene_count + 1):
    print(f"Processing scene {i} of {scene_count}")

    recording_meta = None

    recording_meta_file_path = os.path.join(args.input_directory_path, f"{i}_recordingMeta.csv")

    with open(recording_meta_file_path, "r") as recording_meta_file:
        recording_meta_reader = csv.DictReader(recording_meta_file)

        for row in recording_meta_reader:
            recording_meta = row
            break

    if recording_meta is None:
        print(f"Missing recording metadata for scene {i}")
        continue

    tracks_meta_fieldnames = None
    valid_tracks = {}
    valid_convoy_tracks = {}

    tracks_meta_file_path = os.path.join(args.input_directory_path, f"{i}_tracksMeta.csv")

    with open(tracks_meta_file_path, "r") as tracks_meta_file:
        tracks_meta_reader = csv.DictReader(tracks_meta_file)

        for row in tracks_meta_reader:
            if tracks_meta_fieldnames is None:
                tracks_meta_fieldnames = list(row.keys())
            if int(row["numLaneChanges"]) == 0 \
            and float(row["numFrames"]) / float(recording_meta["frameRate"]) >= minimum_time_window_threshold:
                valid_tracks[int(row["id"])] = row

                if abs(float(row["maxXVelocity"]) - float(row["minXVelocity"])) / abs(float(row["maxXVelocity"])) >= velocity_proportional_diff_threshold:
                    valid_convoy_tracks[int(row["id"])] = -1

    print(f"Found {len(valid_tracks.keys())} valid agents and {len(valid_convoy_tracks.keys())} valid convoy agents")

    if len(valid_convoy_tracks.keys()) == 0:
        continue

    tracks_fieldnames = None
    track_frames = {}

    tracks_file_path = os.path.join(args.input_directory_path, f"{i}_tracks.csv")

    with open(tracks_file_path, "r") as tracks_file:
        tracks_reader = csv.DictReader(tracks_file)

        current_id = None

        for row in tracks_reader:
            if tracks_fieldnames is None:
                tracks_fieldnames = list(row.keys())
            if int(row["id"]) == current_id:
                frames.append(row)
            elif current_id is None:
                frames = [row]
                current_id = int(row["id"])
            else:
                track_frames[current_id] = frames
                frames = [row]
                current_id = int(row["id"])

        if current_id is not None:
            track_frames[current_id] = frames

    used_tracks = {}

    success_count = 0
    no_following_count = 0
    preceding_count = 0
    following_is_not_valid_convoy_count = 0
    following_is_too_far = 0
    too_short_before_other_count = 0
    no_suitable_other_count = 0
    for valid_convoy_track in valid_convoy_tracks.keys():
        following_id = None
        metadata = valid_tracks[valid_convoy_track]
        frames = track_frames[valid_convoy_track]

        if 0.0 <= float(metadata["minDHW"]) < minimum_clearance_distance_headway_threshold:
            preceding_count += 1
            continue

        for frame in frames:
            if following_id is None:
                lane_id = int(frame["laneId"])
                if int(frame["followingId"]) > 0:
                    following_id = int(frame["followingId"])
            else:
                if int(frame["followingId"]) > 0 and int(frame["followingId"]) != following_id:
                    following_id = None
                    break

        if following_id is None:
            no_following_count += 1
            continue

        if valid_convoy_tracks.get(following_id) is None:
            following_is_not_valid_convoy_count += 1
            continue

        following_metadata = valid_tracks[following_id]
        following_frames = track_frames[following_id]

        if (float(following_metadata["minDHW"]) < 0.0 or
                float(following_metadata["minDHW"]) >= maximum_convoy_distance_headway_threshold):
            following_is_too_far += 1
            continue

        latest_initial_frame = max(float(metadata["initialFrame"]), float(following_metadata["initialFrame"]))
        earliest_final_frame = min(float(metadata["finalFrame"]), float(following_metadata["finalFrame"]))

        if (earliest_final_frame - latest_initial_frame) / float(recording_meta["frameRate"]) < minimum_time_window_threshold:
            too_short_before_other_count += 1
            continue

        used_lanes = [lane_id]
        independent_frames_dict = {}
        updated_latest_initial_frame = latest_initial_frame
        updated_earliest_final_frame = earliest_final_frame
        for valid_track in valid_tracks.keys():
            if used_tracks.get(valid_track) is not None:
                continue

            other_lane_id = None
            other_metadata = valid_tracks[valid_track]
            other_frames = track_frames[valid_track]

            prospective_updated_latest_initial_frame = max(updated_latest_initial_frame, float(other_metadata["initialFrame"]))
            prospective_updated_earliest_final_frame = min(updated_earliest_final_frame, float(other_metadata["finalFrame"]))

            if ((prospective_updated_earliest_final_frame - prospective_updated_latest_initial_frame) /
                    float(recording_meta["frameRate"]) < minimum_time_window_threshold):
                continue

            for frame in other_frames:
                if other_lane_id is None:
                    other_lane_id = int(frame["laneId"])
                    break

            if other_lane_id is None or other_lane_id in used_lanes:
                continue

            updated_latest_initial_frame = prospective_updated_latest_initial_frame
            updated_earliest_final_frame = prospective_updated_earliest_final_frame

            used_lanes.append(other_lane_id)

            independent_frames_dict[valid_track] = other_frames

            used_tracks[valid_track] = -1
            used_tracks[valid_convoy_track] = -1
            used_tracks[following_id] = -1

        if len(used_lanes) == 1:
            no_suitable_other_count += 1
            continue
        else:
            success_count += 1

        updated_frames = []
        for frame in frames:
            frame_num = int(frame["frame"])
            if updated_latest_initial_frame <= frame_num <= updated_earliest_final_frame:
                updated_frames.append(frame)

        updated_following_frames = []
        for frame in following_frames:
            frame_num = int(frame["frame"])
            if updated_latest_initial_frame <= frame_num <= updated_earliest_final_frame:
                updated_following_frames.append(frame)

        updated_independent_frames_dict = {}
        for independent_id in independent_frames_dict.keys():
            updated_independent_frames_dict[independent_id] = []
            for frame in independent_frames_dict[independent_id]:
                frame_num = int(frame["frame"])
                if updated_latest_initial_frame <= frame_num <= updated_earliest_final_frame:
                    updated_independent_frames_dict[independent_id].append(frame)

        if args.csv:
            output_to_file_csv(
            updated_latest_initial_frame,
            updated_earliest_final_frame,
            updated_frames,
            updated_following_frames,
            updated_independent_frames_dict,
            os.path.join(args.output_directory_path, f"scene-{i}-{following_id}_follows_{valid_convoy_track}-{len(independent_frames_dict)}_independent.csv"),
            args.velocity_variables,
            args.all_kinematic_variables)

        if args.json_meta:
            output_to_file_json_meta(
            i,
            valid_convoy_track,
            following_id,
            list(independent_frames_dict.keys()),
            os.path.join(args.output_directory_path, f"scene-{i}-{following_id}_follows_{valid_convoy_track}-{len(independent_frames_dict)}_independent.json"))

        if args.trimmed_scene_output_path is not None:
            shutil.copy(recording_meta_file_path, os.path.join(args.trimmed_scene_output_path, f"scene-{i}-{following_id}_follows_{valid_convoy_track}-{len(independent_frames_dict)}_independent-recordingMeta.csv"))

            present_ids = []

            with open(tracks_meta_file_path, "r") as tracks_meta_file:
                tracks_meta_reader = csv.DictReader(tracks_meta_file)
                with open(os.path.join(args.trimmed_scene_output_path, f"scene-{i}-{following_id}_follows_{valid_convoy_track}-{len(independent_frames_dict)}_independent-tracksMeta.csv"), "w") as tracks_meta_output_file:
                    tracks_meta_csv_writer = csv.DictWriter(tracks_meta_output_file, fieldnames=tracks_meta_fieldnames)
                    tracks_meta_csv_writer.writeheader()
                    for row in tracks_meta_reader:
                        if float(row["initialFrame"]) < updated_earliest_final_frame \
                        and float(row["finalFrame"]) > updated_latest_initial_frame:
                            present_ids.append(row["id"])
                            tracks_meta_csv_writer.writerow(row)

            with open(tracks_file_path, "r") as tracks_file:
                tracks_reader = csv.DictReader(tracks_file)
                with open(os.path.join(args.trimmed_scene_output_path, f"scene-{i}-{following_id}_follows_{valid_convoy_track}-{len(independent_frames_dict)}_independent-tracks.csv"), "w") as tracks_output_file:
                    tracks_csv_writer = csv.DictWriter(tracks_output_file, fieldnames=tracks_fieldnames)
                    tracks_csv_writer.writeheader()
                    for row in tracks_reader:
                        if row["id"] in present_ids:
                            tracks_csv_writer.writerow(row)

    print(f"{success_count} Successes, {preceding_count} Failures due to preceding agent, {no_following_count} Failures"
          f" due to no following agent, {following_is_not_valid_convoy_count} Failures due to following agent not being"
          f" a valid convoy agent, {following_is_too_far} Failures due to following agent being too far away, "
          f"{too_short_before_other_count} Failures due to too small of a time frame (prior to adding other agent), "
          f"{no_suitable_other_count} Failures due to not being able to find suitable other agent")
