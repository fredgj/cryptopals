from collections import Counter
from utils import readfile, chunkify

def find_repetitions(ciphers):
    for cipher in ciphers:
        chunks = [c for c in chunkify(cipher,32)]
        counter = Counter(chunks)
        block, repetitions = counter.most_common()[0]
        if repetitions > 1:
            return repetitions, block, cipher


ciphers = readfile('testdata/8.txt')

repetitions, block, cipher = find_repetitions(ciphers)
print('{} repeated {} times in {}'.format(block, repetitions, cipher))

