import json
import os
import subprocess
import sys
import concurrent.futures

root_dir = sys.argv[1]
other_args = sys.argv[2:]



def get_max_workers():
    if "--max_workers" in other_args:
        max_workers = int(other_args[other_args.index("--max_workers") + 1])
        other_args.pop(other_args.index("--max_workers") + 1)
        other_args.remove("--max_workers")
        return max_workers
    return 1

def load_meta(directory):
    if os.path.exists(os.path.join(directory, "meta.json")):
        with open(os.path.join(directory, "meta.json"), "r") as f:
            meta = json.load(f)
            return meta
    return {}


def generate_cmd(folder, metadata):
    src_file = os.path.join(folder, metadata["filename"])
    cmd = ["python3", "/app/scripts/gpt-subtrans.py", src_file]
    [cmd.extend([f"--{k}", v]) for k, v in metadata["subtrans_args"].items()]
    cmd.extend([*other_args])
    return cmd


def find_meta_info(data_tree, level, file):
    for i in range(level, -1, -1):
        if file in data_tree[i]:
            return data_tree[i][file]
    return {"filename": file, "subtrans_args": {"moviename": file.split(".")[0]}}

def run_job(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)

max_workers = get_max_workers()
print(f"Max workers: {max_workers}")
meta_tree = {}
jobs = []
# traverse all directories and files
for subdir, dirs, files in os.walk(root_dir):
    depth = len(os.path.normpath(subdir).split(os.path.sep)) - len(os.path.normpath(root_dir).split(os.path.sep))
    meta_tree[depth] = load_meta(subdir)
    for file in files:
        if file.endswith(".srt"):
            meta_info = find_meta_info(meta_tree, depth, file)
            cmd = generate_cmd(subdir, meta_info)
            jobs.append(cmd)

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(run_job, jobs)

'''
rewrite the the readme.md file to include the following updates:
- the folder-subtrans.py script now supports multi-threading using the --max_workers optional argument to specify the number of concurrent files to process,
- the folder-subtrans.py script now search the metadata from the meta.json file starting from the current directory and traversing up to the root directory,
    if the meta.json file is not found in the current directory, it will search in the parent directory until it reaches the root directory,
    and if the meta.json file is not found in any of the directories, it will use the default metadata values which are the filename as the moviename without the extension, and no description.
'''
