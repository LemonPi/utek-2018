#!/usr/bin/env python3

# run with python3 tester.py

import subprocess
import shutil
import os
import re
import time
from collections import defaultdict

import argparse

parser = argparse.ArgumentParser(description='Test your program for UTEK 2018.')
parser.add_argument('--ref', default='./', help='path to the ref and input folders')
parser.add_argument('--out', default='./', help='path to the output folder')
args = parser.parse_args()


def process(lines):
    lines = [line.strip() for line in lines]
    return [re.sub(r'\s*\|\s*', '|', line) for line in lines if line != '']

input_path = os.path.join(args.ref, 'input')
ref_path = os.path.join(args.ref, 'ref')
output_path = os.path.join(args.out, 'output')

os.system('cp -rf {}/* input'.format(input_path))
shutil.rmtree('output', ignore_errors=True)
os.mkdir('output')

# execute script
t = time.time()

# use this to suppress stdout and stderr
# with open(output_path + '/stdout.txt', 'w') as stdout, open(output_path + '/stderr.txt', 'w') as stderr:
#     subprocess.call('sh ./run', stdout=stdout, stderr=stderr, timeout=5*60)   # add the executable name for Git bash (sh ./run for the example)
subprocess.call('sh ./run', timeout=5*60)
print('Took {} seconds'.format(time.time() - t))

os.system('cp -rf {}/* ref'.format(ref_path))

# diff against outputs to compute score
max_scores = {
    '1a.out': 5,
    '1b.out': 5,
    '1c.out': 5,
    '2a.out': 5,
    '2b.out': 10,
    '3a.out': 5,
    '3b.out': 10,
    '3c.out': 10,
    '3d.out': 10
}

score = defaultdict(int)

for filename in os.listdir('ref'):
    try:
        with open(output_path + '/' + filename) as out_file, open('ref/' + filename) as ref_file:
            out_lines = process(out_file.readlines())
            ref_lines = process(ref_file.readlines())

            for out, ref in zip(out_lines, ref_lines):
                if out == ref:
                    score[filename] += 1

            score[filename] *= max_scores[filename] / len(out_lines)   # max score / total test cases

    except FileNotFoundError:
        print("WARNING: could not read file", filename)
        # file not created

# print out scores
print('======= SCORES ========')
for k in sorted(max_scores.keys()):
    print(k + ',', score[k])

print('total,', sum(score.values()))