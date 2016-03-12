import xor_crypto
from utils import chunkify, readfile


def to_byte(data):
    for line in data:
        yield ''.join(chr(int(c,16)) for c in chunkify(line.strip(),2))


if __name__ == '__main__':
    data = to_byte(readfile('testdata/4.txt'))
    best = (0,'')

    for d in data:
        key = xor_crypto.find_key(d,1,2)
        decrypted = xor_crypto.decrypt(d, key)
        score = xor_crypto.calculate_score(decrypted)
        best_score,_ = best
        if score > best_score:
            best = (score,decrypted)

    _, decrypted = best
    print(decrypted)

