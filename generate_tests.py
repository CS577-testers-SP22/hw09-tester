from subprocess import Popen, PIPE
from random import random, seed, shuffle
from tqdm import tqdm
from pprint import pprint
import json
import time

SMALL_TEST_COUNT = 100
MEDIUM_TEST_COUNT = 100
LARGE_TEST_COUNT = 100
SEED = 0
TEST_FILE = 'tests.json'

seed(SEED)

class Timer():
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f'{self.name}: {time.time() - self.t0:.2f}')

def generate_random_input(max_instances=10, min_nodes=3, max_nodes=20, min_edges=2, max_edges=100):
    '''returns a string that is valid input'''
    instances = int(random() * (max_instances)) + 1
    test = f'{instances}'

    for _ in range(instances):
        node_count = int(random() * (max_nodes - min_nodes)) + min_nodes
        edge_count = int(random() * (max_edges - min_edges)) + min_edges

        test += f'\n{node_count} {edge_count}'
        for i in range(edge_count):
            a = int(random() * node_count) + 1
            b = int(random() * node_count) + 1
            c = int(random() * 10) + 1
            test += f'\n{a} {b} {c}'

    return test + '\n'

def shell(cmd, stdin=None):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out, err = p.communicate(input=stdin.encode() if stdin else None)
    return out.decode('utf8'), err.decode('utf8')

commands = ['python3 FF.py', 'python3 FF2.py']

print('Building:')
buildOutput, buildError = shell('make build')
if buildOutput:
    print(buildOutput)
if buildError:
    print('Error running `make build`:\n')
    print(buildError)
    exit()

tests = dict()

# manual tests
tests['given-test-0'] = {'note':'test is provided by canvas', 'input':'2\n3 2\n2 3 4\n1 2 5\n6 9\n1 2 9\n1 3 4\n2 4 1\n2 5 6\n3 4 4\n3 5 5\n4 6 8\n5 6 5\n5 6 3\n', 'output':"4\n11\n"}

tests['edge-test-0'] = {'note':'single edge from s to t', 'input':"1\n2 1\n1 2 5\n", 'output':"5\n"}
tests['edge-test-1'] = {'note':'2 edges between same nodes', 'input':"1\n2 2\n1 2 5\n1 2 3\n", 'output':"8\n"}
tests['edge-test-2'] = {'note':'no path from s to t', 'input':"1\n3 2\n2 3 5\n3 2 1\n", 'output':"0\n"}
tests['edge-test-3'] = {'note':'flow may need to be pushed back', 'input':"1\n4 5\n1 2 5\n1 3 5\n2 4 5\n3 4 5\n2 3 1\n", 'output':"10\n"}

for name, data in tests.items():
    results = [shell(x, stdin=data['input']) for x in commands]
    if not all(x[0] == data['output'] for x in results) or len(results[0][0]) < 1:
        print(f'{name} - {data["note"]}')
        for name, (out, err) in zip(commands, results):
            print(f'{name}\n{out}\n')
            print(f'{name}\n{err}')
        print(f'Input\n{data["input"]}')
        exit()

# random tests

for i in tqdm(range(SMALL_TEST_COUNT)):
    test = generate_random_input(max_instances=1, min_nodes=3, max_nodes=4, min_edges=2, max_edges=5)
    results = [shell(x, stdin=test) for x in commands]
    if not all(x[0] == results[0][0] for x in results) or len(results[0][0]) < 1:
        for name, (out, err) in zip(commands, results):
            print(f'{name} output:\n{out}\n')
            print(f'{name} error:\n{err}')
        print(f'Input\n{test}')
        exit()
    tests[f'small-test-{i}'] = {'input':test, 'output':results[0][0]}

for i in tqdm(range(MEDIUM_TEST_COUNT)):
    test = generate_random_input(max_instances=1, min_nodes=3, max_nodes=8, min_edges=5, max_edges=15)
    results = [shell(x, stdin=test) for x in commands]
    if not all(x[0] == results[0][0] for x in results) or len(results[0][0]) < 1:
        for name, (out, err) in zip(commands, results):
            print(f'{name} output:\n{out}\n')
            print(f'{name} error:\n{err}')
        print(f'Input\n{test}')
        exit()
    tests[f'medium-test-{i}'] = {'input':test, 'output':results[0][0]}

for i in tqdm(range(LARGE_TEST_COUNT)):
    test = generate_random_input(max_instances=10, min_nodes=10, max_nodes=20, min_edges=20, max_edges=100)
    results = [shell(x, stdin=test) for x in commands]
    if not all(x[0] == results[0][0] for x in results) or len(results[0][0]) < 1:
        for name, (out, err) in zip(commands, results):
            print(f'{name} output:\n{out}\n')
            print(f'{name} error:\n{err}')
        print(f'Input\n{test}')
        exit()
    tests[f'large-test-{i}'] = {'input':test, 'output':results[0][0]}

# pprint(tests)
with open(TEST_FILE, 'w+') as f:
    json.dump(tests, f, indent=4)
