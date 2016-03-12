from utils import chunkify, srange


base64_table = ''.join(chr(s) for s in srange('A-Za-z0-9')) + '+/'


def decode_base64_byte(byte1, byte2, lshifts, rshifts=0):
    decoded = format(byte1<<lshifts | byte2>>rshifts, '08b')[-8:]
    decoded = chr(int(decoded, 2))
    return decoded


def decode(data):
    decoded = ''
    for i in range(0, len(data), 4):
        ch1, ch2, ch3, ch4 = data[i:i+4]
        a = base64_table.find(ch1)
        b = base64_table.find(ch2)
        decoded += decode_base64_byte(a, b, 2, 4)
        if ch3 != '=':
            a = b
            b = base64_table.find(ch3)
            decoded += decode_base64_byte(a, b, 4, 2)
            if ch4 != '=':
                a = b
                b = base64_table.find(ch4)
                decoded += decode_base64_byte(a, b, 6)
    return decoded


def encode_byte(byte, format_type, a,b,c, b1=0):
    byte = int(byte,16) if format_type == 'x' else ord(byte)
    b1 |= byte >> a
    b2 = (byte & b) << c
    ch1 = base64_table[b1]
    ch2 = base64_table[b2]
    return ch1,ch2, b2


def indexes(format_type):
    if format_type =='x':
        return (2,4,6)
    return (1,2,3)

def encode(data, format_type='b'):
    index2, index3, index4 = indexes(format_type)
    chunk_size = 6 if format_type == 'x' else 3
    b64 = ''
    chunks = [c for c in chunkify(data, chunk_size)]
    for chunk in chunks:
        byte1 = chunk[0:index2]
        byte2 = chunk[index2:index3]
        byte3 = chunk[index3:index4]
        ch1=ch2=ch3=ch4=''
        ch1, ch2,bb1 = encode_byte(byte1, format_type, 2,3,4)
        
        if byte2:
            ch2,ch3,bb1 = encode_byte(byte2, format_type, 4,15,2,b1=bb1)
            if byte3:
                ch3,ch4,_ = encode_byte(byte3, format_type, 6,63, 0, b1=bb1)
            else:
                ch4 = '='
        else:
            ch3 = '=='
        b64 += ch1+ch2+ch3+ch4
    return b64

