#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from subprocess import check_output

# Get Slurm variables. All of them are supposed to be set by the Slurm controller according to '$ man sbatch'. Hence,
# the default values are set correctly, if running under slurm. Otherwise they will result in a single worker setup.
# Compressed list of nodes, e.g. 'node[0-2],node5' for ['node0', 'node1', 'node2', 'node5']
slurm_nodelist = os.getenv("SLURM_JOB_NODELIST", "localhost")
# Compressed list of number of tasks on all nodes, e.g. '2(x2), 1' for [2, 2, 1]. Same order as in SLURM_JOB_NODELIST.
slurm_tasks_per_node = os.getenv("SLURM_TASKS_PER_NODE", "1")
# Zero-based index of the current node in SLURM_JOB_NODELIST, e.g. '0'.
slurm_node_id = int(os.getenv("SLURM_NODEID", "0"))
# Zero-based index of the current task on the current node, e.g. '0'.
slurm_local_id = int(os.getenv("SLURM_LOCALID", "0"))

# Unpack the nodelist and export it to SLURM_JOB_HOSTNAMES environment variable.
try:
    hostnames = check_output(["scontrol", "show", "hostnames", slurm_nodelist]).decode().split()
    os.environ["SLURM_JOB_HOSTNAMES"] = ",".join(hostnames)
except Exception as e:
    raise RuntimeError(f"Failed to unpack SLURM_JOB_NODELIST node list: {e}")

# Unpack the list of number of tasks into tasks_per_node and reexport it to SLURM_TASKS_PER_NODE environment variable.
tasks_per_node = []
pattern = re.compile(r"(\d+)(?:\(x(\d+)\))?")
parts = slurm_tasks_per_node.split(',')
for part in parts:
    part = part.strip()
    match = pattern.match(part)

    if match:
        num = int(match.group(1))
        if match.group(2):
            repeat = int(match.group(2))
        else:
            repeat = 1
    tasks_per_node.extend([num] * repeat)
os.environ["SLURM_TASKS_PER_NODE"] = ",".join(map(str, tasks_per_node))

# Construct the workers list for TF_CONFIG.
port_offset = 12345
workers = []
for (i, host) in enumerate(hostnames):
    for j in range(tasks_per_node[i]):
        port = base_offset + j
        workers.append(f"{host}:{port}")

# Calculate of index.
current_worker_index = sum(tasks_per_node[:slurm_node_id]) + slurm_local_id

# Construct and export TF_CONFIG
tf_config = {
    "cluster": {
        "worker": workers  # List of all worker addresses with unique ports
    },
    "task": {
        "type": "worker",
        "index": current_worker_index
    }
}
os.environ["TF_CONFIG"] = json.dumps(tf_config)

print(f"TF_CONFIG set for worker {current_worker_index}: {json.dumps(tf_config, indent=2)}")
print(f"For comparison: our global id is {os.environ['SLURM_PROCID']} and our calculated index is {current_worker_index}")
