import aes
import base64
from utils import chunkify, readfile

if __name__ == '__main__':
    data = ''.join(readfile('testdata/7.txt'))
    data = base64.decode(data)
    data = chunkify(data,16)
    key = 'YELLOW SUBMARINE'
    decrypted = ''
    for d in data: 
        decrypted += aes.decrypt(d, key)
    print(decrypted)


