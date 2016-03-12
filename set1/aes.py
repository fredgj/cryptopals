from utils import chunkify, rotate, readfile

class KeySizeError(Exception):
    pass


class BlockSizeError(Exception):
    pass


S = (0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
     0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
     0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
     0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
     0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
     0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
     0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
     0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
     0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
     0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
     0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
     0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
     0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
     0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
     0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
     0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16)


# used by inverted sub bytes
INV_S = (0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
         0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
         0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
         0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
         0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
         0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
         0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
         0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
         0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
         0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
         0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
         0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
         0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
         0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
         0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
         0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D)


# used to expand key
RCON = (0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d)


def sbox(i):
    return S[i]


def inv_sbox(i):
    return INV_S[i]


# each byte in the state is replaces with
# a value from a fixed table
def __sub_bytes(state,box):
    for i in range(4):
        for j in range(4):
            state[i][j] = box(state[i][j])
    return state


# wrapper for __sub_bytes, used for encryption
def sub_bytes(state):
    return __sub_bytes(state, sbox)


# wrapper for __sub_bytes, used for decryption
def inv_sub_bytes(state):
    return __sub_bytes(state, inv_sbox)


# each row in the state is shifted to left
# with its rownumber.
def shift_rows(state):
    tmp = state[0][1]
    state[0][1] = state[1][1]
    state[1][1] = state[2][1]
    state[2][1] = state[3][1]
    state[3][1] = tmp

    tmp = state[0][2]
    state[0][2] = state[2][2]
    state[2][2] = tmp
    tmp = state[1][2]
    state[1][2] = state[3][2]
    state[3][2] = tmp

    tmp = state[0][3]
    state[0][3] = state[3][3]
    state[3][3] = state[2][3]
    state[2][3] = state[1][3]
    state[1][3] = tmp

    return state


# each row in the state is shifted to right
# with its rownumber.
def inv_shift_rows(state):
    tmp = state[3][1]
    state[3][1] = state[2][1]
    state[2][1] = state[1][1]
    state[1][1] = state[0][1]
    state[0][1] = tmp

    tmp = state[0][2]
    state[0][2] = state[2][2]
    state[2][2] = tmp
    tmp = state[1][2]
    state[1][2] = state[3][2]
    state[3][2] = tmp

    tmp = state[0][3]
    state[0][3] = state[1][3]
    state[1][3] = state[2][3]
    state[2][3] = state[3][3]
    state[3][3] = tmp

    return state


# adds round n's roundkey to the state
def add_roundkey(n, roundkey, state):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= roundkey[n*16+i*4+j]
    return state


# Galois multiplication, returns the product of
# a and b in a finite field.
def gmul(a,b):
    p = 0
    while b:
        if b&1:
            p^=a
        hi_bit = a&0x80
        a <<= 1
        if hi_bit:
            a ^= 0x11b
        b >>= 1

    return p


def __mix_columns(state,vector):
    for i in range(4):
        a,b,c,d = state[i]
        v1,v2,v3,v4 = vector

        state[i][0] = gmul(a,v1) ^ gmul(b,v2) ^ gmul(c,v3) ^ gmul(d,v4)
        state[i][1] = gmul(a,v4) ^ gmul(b,v1) ^ gmul(c,v2) ^ gmul(d,v3)
        state[i][2] = gmul(a,v3) ^ gmul(b,v4) ^ gmul(c,v1) ^ gmul(d,v2)
        state[i][3] = gmul(a,v2) ^ gmul(b,v3) ^ gmul(c,v4) ^ gmul(d,v1)

    return state


# multiplies each columns with the polynomial c(x) = 3x^3 + x^2 + x + 2
def mix_columns(state):
    vector = [2,3,1,1]
    return __mix_columns(state,vector)


# multiplies each columns with the polynomial c(x) = 11x^3 + 13x^2 + 9x + 14
def inv_mixcolumns(state):
    vector = [14,11,13,9]
    return __mix_columns(state, vector)


# expands key into a (nr+1)*16 table, so there are (nr+1)*4 roundkeys.
# Each roundkey is used with each function to encrypt/decrypt the state
# for each round. Supports 128, 192 and 256 bit keys.
def key_expand(key, nr, nk):
    expanded = [k for k in key]
    tmp = [0]*4
    rcon_iter = 1

    # size is either 16, 24 or 42 byte
    size = nk*4

    # length of the expended keysize is either
    # 176, 208 or 240, depending on the keysize
    expanded_keysize = (nr+1)*16
    currentsize = size

    while currentsize < expanded_keysize:

        for i in range(4):
            tmp[i] = expanded[(currentsize-4)+i]

        if currentsize%size == 0:
            tmp = rotate(tmp)
            for i in range(4):
                tmp[i] = S[tmp[i]]

            tmp[0] = tmp[0]^RCON[rcon_iter]
            rcon_iter += 1

        # Add an extra s-box for 256 bit keys
        if currentsize%size == 16 and size==32:
            for i in range(4):
                tmp[i] = S[tmp[i]]

        for i in range(4):
            expanded.append(expanded[currentsize-size]^tmp[i])
            currentsize += 1

    return expanded


def valid_key(key, keysize):
    return keysize==128 or keysize==192 or keysize==256


# initialize state and roundkey
def init(block, key, format_):
    if format_ == 'x':
        key = [chr(int(k,16)) for k in chunkify(key,2)]
        block = [chr(int(b,16)) for b in chunkify(block,2)]

    key = [ord(k) for k in key]
    keysize=len(key)*8

    if len(block) != 16:
        raise BlockSizeError('Block must be of length 16 bytes')
    if not valid_key(key,keysize):
        raise KeySizeError('Key must be either 128, 192 or 256 bit')

    state = [ord(b) for b in block]
    state = [state[i:i+4] for i in range(0, len(state)-3, 4)]

    nk = keysize//32
    nr = nk+6

    roundkey = key_expand(key, nr, nk)

    return state,roundkey,nr


# takes a state as input and returns the state as a string
def strify(state, format_):
    state = (b for s in state for b in s)

    if format_ == 'x':
        return ''.join(format(e,'02x') for e in state)

    return ''.join(chr(e) for e in state)


# Takes a 128 bit block of plaintext and a key (128, 192 or 256 bit)
# and returns ciphertext.
# Format is either b for byte or x for hex
def encrypt(block, key, format_='b'):
    state, roundkey, nr = init(block, key, format_)
    state = add_roundkey(0, roundkey, state)
    
    # round 1..nr
    for i in range(1,nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_roundkey(i, roundkey, state)

    #final round
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_roundkey(nr, roundkey, state)

    return strify(state, format_)


# Takes a 128 bit block of ciphertext and a key (128, 192 or 256 bit)
# and returns plaintext
# Format is either b for byte or x for hex
def decrypt(block, key, format_='b'):
    state, roundkey, nr = init(block, key, format_)
    state = add_roundkey(nr, roundkey, state)

    # round nr-1..0
    for i in range(nr-1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_roundkey(i, roundkey, state)
        state = inv_mixcolumns(state)

    # final round
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_roundkey(0, roundkey, state)

    return strify(state, format_)


