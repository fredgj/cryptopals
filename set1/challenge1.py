import base64
from utils import chunkify

if __name__ == '__main__':
    hex_ = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    correct = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    b64 = base64.encode(hex_, format_type='x')
    print(b64)
    print(b64 == correct)

