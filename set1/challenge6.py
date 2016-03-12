from collections import Counter
from itertools import cycle

import base64
import xor_crypto
from utils import chunkify, readfile


if __name__ == '__main__':
    data = readfile('testdata/6.txt')
    data = ''.join(base64.decode(d) for d in data)

    key = xor_crypto.find_key(data, 2, 41)
    print('Key: {key}\n'.format(key=key))
    decrypted = xor_crypto.decrypt(data, key)
    print(decrypted)

