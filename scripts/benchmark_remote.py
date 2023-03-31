from contextlib import contextmanager
import subprocess
import json
import os
import argparse


def run(cmd: list, f_out: str):
    with open(f_out, 'w') as f:
        subprocess.run(cmd, stdout=f, stderr=f)


def run_dp_compress(ori_model: str, frz_model: str, f_out: str):
    run(['dp', 'compress', '-i', ori_model, '-o', frz_model], f_out=f_out)


def run_dp_train(input: str, init_frz_model: str, f_out: str):
    run(['dp', 'train', input, '--skip-neighbor-stat', '-f', init_frz_model], f_out=f_out)


def run_lmp(input: str, f_out: str):
    run(['lmp', '-in', input], f_out=f_out)


def change_training_steps(input: str, output:str, training_steps: int):
    with open(input, 'r') as f:
        data = json.load(f)
    data['training']['numb_steps'] = training_steps
    data['training']['disp_freq'] = 100
    with open(output, 'w') as f:
        json.dump(data, f, indent=4)

def change_lmp_model(input: str, output: str, model: str):
    with open(input, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('pair_style'):
            lines[i] = f'pair_style deepmd {model}\n'
    with open(output, 'w') as f:
        f.writelines(lines)


@contextmanager
def chdir(directory: str):
    """With statement to change the current working directory."""
    cwd = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(cwd)


def read_train_speed(f_out: str):
    with open(f_out, 'r') as f:
        for line in f:
            if line.startswith('DEEPMD INFO    average training time'):
                return float(line.split()[5])
    raise RuntimeError('Cannot find the training speed in the output file.')

def read_md_speed(f_out: str):
    with open(f_out, 'r') as f:
        for line in f:
            if line.startswith('Loop time of'):
                # Loop time of 0.127946 on 1 procs for 20 steps with 192 atoms
                return float(line.split()[3]) / float(line.split()[8]) / float(line.split()[11])
    raise RuntimeError('Cannot find the MD speed in the output file.')


def benchmark(directory: str, lmp_file: str, compress: bool, input_file: str = 'input.json', frozen_model: str = 'frozen_model.pb'):
    """Benchmark the training and MD process, including the compressed model if applicable.

    The directory is expected to contain the following files:
    - input.json: the input file for dp train
    - frozen_model.pb: the frozen model for dp train
    
    Parameters
    ----------
    directory : str
        The directory to store the benchmark results.
    lmp_file : str
        The LAMMPS input file for MD.
    compress : bool
        Whether to benchmark the compressed model.
    """
    with chdir(directory=directory):
        # benchmark training
        # first, reset the training steps
        change_training_steps(input=input_file, output='benchmark.json', training_steps=10000)
        run_dp_train(input='benchmark.json', init_frz_model=frozen_model, f_out='bench_train.log')
        train_speed = read_train_speed(f_out='bench_train.log')
        # benchmark MD
        if lmp_file is not None:
            change_lmp_model(input=lmp_file, output='benchmark.lmp', model=frozen_model)
            run_lmp(input='benchmark.lmp', f_out='bench_md.log')
            md_speed = read_md_speed(f_out='bench_md.log')
        else:
            md_speed = None

        if compress:
            # benchmark compressed model
            run_dp_compress(ori_model=frozen_model, frz_model='compressed_model.pb', f_out='compress.log')
            run_dp_train(input='benchmark.json', init_frz_model='compressed_model.pb', f_out='bench_train_compressed.log')
            train_compress_speed = read_train_speed(f_out='bench_train_compressed.log')
            # benchmark MD with compressed model
            if lmp_file is not None:
                change_lmp_model(input=lmp_file, output='benchmark.compress.lmp', model='compressed_model.pb')
                run_lmp(input='benchmark.compress.lmp', f_out='bench_md_compressed.log')
                md_compress_speed = read_md_speed(f_out='bench_md_compressed.log')
            else:
                md_compress_speed = None
        else:
            train_compress_speed = None
            md_compress_speed = None

        # now we have four results
        print(f'Training, Compressed training, MD, compressed MD: {train_speed} {train_compress_speed} {md_speed} {md_compress_speed}')


if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help='The directory to store the benchmark results.')
    parser.add_argument('--lmp_file', type=str, help='The LAMMPS input file for MD.')
    parser.add_argument('--compress', action='store_true', help='Whether to benchmark the compressed model.')
    args = parser.parse_args()
    benchmark(directory=args.directory, lmp_file=args.lmp_file, compress=args.compress)
