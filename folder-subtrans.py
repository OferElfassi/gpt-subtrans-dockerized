import json
import os
import subprocess
import sys

root_dir = sys.argv[1]
other_args = sys.argv[2:]


def load_meta(directory):
    if os.path.exists(os.path.join(directory, "meta.json")):
        with open(os.path.join(directory, "meta.json"), "r") as f:
            meta = json.load(f)
            return meta
    return None


# load top level meta
top_level_meta = load_meta(root_dir) or {}

# dict of all discovered .srt files and their metadata
discovered_files = {}  # {"/folder/path": [{"filename": "file.srt", "subtrans_args": {"moviename": "name"}},...],...}

# traverse all directories and files
for subdir, dirs, files in os.walk(root_dir):
    metadata = load_meta(subdir) or top_level_meta
    for file in files:
        if file.endswith(".srt"):
            if subdir not in discovered_files:
                discovered_files[subdir] = []
            # check if metadata exists for this file in the current directory or top level directory
            if file in metadata:
                discovered_files[subdir].append(metadata[file])
            else:  # if metadata does not exist, use the filename as the moviename
                discovered_files[subdir].append({"filename": file, "subtrans_args": {"moviename": file.split(".")[0]}})

# run gpt-subtrans.py for each file with its metadata
for folder, metadatas in discovered_files.items():
    for metadata in metadatas:
        src_file = os.path.join(folder, metadata["filename"])
        cmd = ["python3", "/app/scripts/gpt-subtrans.py", src_file]
        subtrans_args = [cmd.extend([f"--{k}", v]) for k, v in metadata["subtrans_args"].items()]
        cmd.extend([*other_args])
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd)
