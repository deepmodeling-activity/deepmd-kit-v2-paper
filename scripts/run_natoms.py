from pathlib import Path

from dpdispatcher import Machine, Resources, Task, Submission


# all data files should be put under the models directory
system_configs = [
    {"name": "01", "lmp_file": "water.in", "compress": False, "data": ["water.lmp"]},
    {"name": "02", "lmp_file": "water.in", "compress": False, "data": ["water.lmp"]},
    {"name": "03", "lmp_file": "water.in", "compress": True, "data": ["water.lmp"]},
    {"name": "04", "lmp_file": "water.in", "compress": True, "data": ["water.lmp"]},
    {"name": "05", "lmp_file": "water.in", "compress": True, "data": ["water.lmp"]},
    {"name": "06", "lmp_file": "water.in", "compress": True, "data": ["water.lmp"]},
    {"name": "07", "lmp_file": "water.in", "compress": True, "data": ["water.lmp"]},
    {"name": "08", "lmp_file": "water.in", "compress": True, "data": ["water.lmp"]},
    {"name": "09", "lmp_file": "water.in", "compress": False, "data": ["water.lmp"]},
    {"name": "10", "lmp_file": "water.in", "compress": False, "data": ["water.lmp"]},
    {"name": "11", "lmp_file": "copper.in", "compress": False, "data": ["copper.lmp"]},
    {"name": "12", "lmp_file": "copper.in", "compress": False, "data": ["copper.lmp"]},
    {"name": "13", "lmp_file": "copper.in", "compress": True, "data": ["copper.lmp"]},
    {"name": "14", "lmp_file": "copper.in", "compress": True, "data": ["copper.lmp"]},
    {"name": "15", "lmp_file": "copper.in", "compress": True, "data": ["copper.lmp"]},
    {"name": "16", "lmp_file": "copper.in", "compress": True, "data": ["copper.lmp"]},
    {"name": "17", "lmp_file": "copper.in", "compress": True, "data": ["copper.lmp"]},
    {"name": "18", "lmp_file": "copper.in", "compress": True, "data": ["copper.lmp"]},
    {"name": "19", "lmp_file": "copper.in", "compress": False, "data": ["copper.lmp"]},
    {"name": "20", "lmp_file": "copper.in", "compress": False, "data": ["copper.lmp"]},
    {"name": "33", "lmp_file": "hea.in", "compress": True, "data": ["hea.lmp"]},
    {"name": "34", "lmp_file": "hea.in", "compress": True, "data": ["hea.lmp"]},
    {"name": "35", "lmp_file": "hea.in", "compress": True, "data": ["hea.lmp"]},
    {"name": "36", "lmp_file": "hea.in", "compress": True, "data": ["hea.lmp"]},
    {"name": "37", "lmp_file": "hea.in", "compress": True, "data": ["hea.lmp"]},
    {"name": "38", "lmp_file": "hea.in", "compress": True, "data": ["hea.lmp"]},
    {"name": "39", "lmp_file": "hea.in", "compress": False, "data": ["hea.lmp"]},
    {"name": "40", "lmp_file": "hea.in", "compress": False, "data": ["hea.lmp"]},
]

local_root = Path(__file__).parent.parent.absolute()

machine = Machine(
    # fill in your machine specific information here
    batch_type="slurm",
    context_type="ssh",
    local_root=str(local_root),
    remote_root="/mnt/beegfs/scratch/jzzeng/dpgen_workdir",
    remote_profile={
    }
)

resources = Resources(
    # fill in your resources information here
    number_node=1,
    cpu_per_node=1,
    gpu_per_node=1,
    queue_name="4CN512C32G4H_4IB_MI250_Ubuntu20",
    group_size=1,
    envs={
        "OMP_NUM_THREADS": "1",
        "TF_INTRA_OP_PARALLELISM_THREADS": "1",
        "TF_INTER_OP_PARALLELISM_THREADS": "1",
    },
)

tasks = []
for config in system_configs:
    if config["name"] not in ("37", "39"):
        continue
    if config["lmp_file"] is not None:
        if config["compress"]:
            command = "python ../../scripts/natoms_remote.py . ../{} --compress".format(config["lmp_file"])
        else:
            command = "python ../../scripts/natoms_remote.py . ../{}".format(config["lmp_file"])
    else:
        continue
    forward_files=[
        "frozen_model.pb",
        *[str(Path("..") / dd) for dd in config["data"]],
    ]
    if config["lmp_file"] is not None:
        forward_files.append(str(Path("..") / config["lmp_file"]))
    task = Task(
        command=command,
        task_work_path=str(Path("models") / config["name"]),
        forward_files=forward_files,
        backward_files=["benchmark.out"],
        outlog="benchmark.out",
        errlog="benchmark.err",
    )
    tasks.append(task)

print("number of tasks: ", len(tasks))
submission = Submission(
    work_base=str(local_root),
    machine=machine,
    resources=resources,
    forward_common_files=["scripts/natoms_remote.py"],
    backward_common_files=[],
    task_list=tasks,
)

submission.run_submission()
