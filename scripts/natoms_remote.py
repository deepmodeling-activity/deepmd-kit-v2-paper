from contextlib import contextmanager
import subprocess
import json
import os
import argparse


def run(cmd: list, f_out: str):
    with open(f_out, 'w') as f:
        subprocess.run(cmd, stdout=f, stderr=f, check=True)


def run_dp_compress(ori_model: str, frz_model: str, f_out: str):
    run(['dp', 'compress', '-i', ori_model, '-o', frz_model], f_out=f_out)

def run_lmp(input: str, f_out: str):
    run(['lmp', '-in', input], f_out=f_out)


@contextmanager
def chdir(directory: str):
    """With statement to change the current working directory."""
    cwd = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(cwd)

def change_replicate(input, output, model: str, replicate: int):
    with open(input, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('pair_style'):
            lines[i] = f'pair_style deepmd {model}\n'
        if line.startswith('replicate'):
            lines[i] = f'replicate 1 1 {replicate}\n'
        if line.startswith('run'):
            lines[i] = f'run 0\n'
    with open(output, 'w') as f:
        f.writelines(lines)


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
        min_replicate = 16  # min working
        max_replicate = 1e6 # max not working
        # benchmark MD
        while True:
            if max_replicate < 1e6:
                current_replicate = (min_replicate + max_replicate) // 2
            else:
                current_replicate = min_replicate * 2
            change_replicate(input=lmp_file, output='benchmark.lmp', model=frozen_model, replicate=current_replicate)
            try:
                run_lmp(input='benchmark.lmp', f_out='bench_md.log')
            except subprocess.CalledProcessError:
                max_replicate = current_replicate
            else:
                min_replicate = current_replicate
            if max_replicate - min_replicate <= 1:
                break
        uncompress = min_replicate
        if compress:
            run_dp_compress(ori_model=frozen_model, frz_model='compressed_model.pb', f_out='compress.log')
            max_replicate = 1e6 # max not working
            while True:
                if max_replicate < 1e6:
                    current_replicate = (min_replicate + max_replicate) // 2
                else:
                    current_replicate = min_replicate * 2
                change_replicate(input=lmp_file, output='benchmark.compress.lmp', model='compressed_model.pb', replicate=current_replicate)
                try:
                    run_lmp(input='benchmark.compress.lmp', f_out='bench_md_compress.log')
                except subprocess.CalledProcessError:
                    max_replicate = current_replicate
                else:
                    min_replicate = current_replicate
                if max_replicate - min_replicate <= 1:
                    break
            compress = min_replicate
        else:
            compress = None
        print(f'uncompressed, compressed: {uncompress} {compress}')

if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help='The directory to store the benchmark results.')
    parser.add_argument('lmp_file', type=str, help='The LAMMPS input file for MD.')
    parser.add_argument('--compress', action='store_true', help='Whether to benchmark the compressed model.')
    args = parser.parse_args()
    benchmark(directory=args.directory, lmp_file=args.lmp_file, compress=args.compress)