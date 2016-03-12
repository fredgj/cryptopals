import xor_crypto
from utils import chunkify

if __name__ == '__main__':
    data = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    # hex -> byte string
    data = ''.join(chr(int(c,16)) for c in chunkify(data,2))

    key = xor_crypto.find_key(data, 1, 2)
    print(xor_crypto.decrypt(data,key))

