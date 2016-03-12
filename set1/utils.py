import re


def chunkify(data, n):
    for i in range(0, len(data), n):
        yield data[i:i+n]


def srange(pattern, step=1):
    ranges = re.findall('([A-Za-z0-9])', pattern)
    for i in chunkify(ranges,2):
        start, stop = i
        start = ord(start)
        stop = ord(stop)+1
        for i in range(start, stop, step):
            yield i

# Rotates a vector left so [a,b,c,d] => [b,c,d,a]
def rotate(vector):
    tmp = vector[0]

    for i in range(len(vector)-1):
        vector[i] = vector[i+1]

    vector[len(vector)-1] = tmp
    return vector


def readfile(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

