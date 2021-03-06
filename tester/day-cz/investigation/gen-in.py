import glob
from os import path
import random

random.seed(439862)

class NameGenerator(object):
    def __init__(self):
        self.set = 0
        self.case = 0

    def next_case(self):
        self.case = self.case+1

    def next_set(self):
        self.set = self.set+1
        self.case = 0

    def name(self):
        if self.set == 0:
            return path.join('test', '00.sample.%s' % (chr(ord('a')+self.case)))
        return path.join('test', '%02d.%s' % (self.set, chr(ord('a')+self.case)))

class Writer(object):
    def __init__(self):
        self.G = NameGenerator();

    def next_case(self):
        self.G.next_case()

    def next_set(self):
        self.G.next_set()

    def open(self):
        print('Generujem: %s' % (self.G.name()))
        self.file = open(self.G.name()+'.in','w')

    def close(self):
        self.file.close()

    def write(self, line):
        self.file.write(line)
        self.file.write('\n')

def w(data):
    W = Writer()
    for set in data:
        for (N, vals) in set:
            W.open()
            W.write('%s' % N)
            W.write(' '.join(map(str, vals)))
            W.close()
            W.next_case()
        W.next_set()

def relabel(vs):
    N = len(vs)+1
    graph = dict((i, []) for i in xrange(N))
    deg = [0] * N
    for i in xrange(len(vs)):
        a, b = i+1, vs[i]
        graph[a].append(b)
        graph[b].append(a)
        deg[a] += 1
        deg[b] += 1

    label = N-1
    mapping = [-1] * N
    next = [-1] * N
    queue = [i for i in xrange(N) if deg[i] == 1]
    visited = [False] * N
    while queue:
        index = random.randint(0, len(queue)-1)
        queue[index], queue[-1] = queue[-1], queue[index]
        node = queue.pop()
        mapping[node] = label
        label -= 1
        visited[node] = True
        for v in graph[node]:
            if not visited[v]:
                next[mapping[node]] = v
                deg[v] -= 1
                if deg[v] == 1:
                    queue.append(v)
    return [mapping[next[i]] for i in xrange(1, N)]


def collect_inputs():
    for fn in glob.glob(path.join('test', '02.*.in')):
        with open(fn, 'r') as f:
            data = map(int, f.read().split())
        yield (data[0], data[1:])

def gen_random(MIN_N, MAX_N):
    N = random.randint(MIN_N, MAX_N)
    vals = [random.randint(0, i-1) for i in xrange(1, N)]
    return (N, relabel(vals))

def gen_star(MIN_N, MAX_N):
    N = random.randint(MIN_N, MAX_N)
    vals = [random.randint(0, i-1)//100 for i in xrange(1, N)]
    return (N, relabel(vals))

def gen_path(MIN_N, MAX_N):
    N = random.randint(MIN_N, MAX_N)
    vals = [random.randint(max(0, i-3), i-1) for i in xrange(1, N)]
    return (N, relabel(vals))


def gen_path_strict(MIN_N, MAX_N):
    N = random.randint(MIN_N, MAX_N)
    vals = [i-1 for i in xrange(1, N)]
    return (N, relabel(vals))

def gen_bt(MIN_N, MAX_N):
    N = random.randint(MIN_N, MAX_N)
    vals = [i//2 for i in xrange(1, N)]
    return (N, relabel(vals))


data = [[], [], []]

for MIN_N, MAX_N in [(500, 1000), (5000, 10000), (100000, 100000)]:
    set_data = [
        gen_random(MIN_N, MAX_N),
        gen_random(MIN_N, MAX_N),
        gen_random(MIN_N, MAX_N),
        gen_star(MIN_N, MAX_N),
        gen_path(MIN_N, MAX_N),
        gen_path_strict(MIN_N, MAX_N),
        gen_bt(MIN_N, MAX_N)]
    set_data.extend(collect_inputs())
    data.append(set_data)

w(data)
