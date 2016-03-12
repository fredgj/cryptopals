from collections import Counter
from itertools import cycle
import re

from hamming import normalize_hamming_distance
from utils import chunkify, srange


def decrypt(data, key):
    xor = lambda x,y: ord(x)^ord(y)
    return ''.join(chr(xor(d,k)) for d,k in zip(data, cycle(key)))


def encrypt(data, key):
    xor = lambda x,y: ord(x)^ord(y)
    return ''.join(chr(xor(d,k)) for d,k in zip(data, cycle(key)))


def transpose(data, keysize):
    return (data[i::keysize] for i in range(keysize))


def find_keysize(data, start, stop):
    best_keysize = 2
    keysizes = []
    for keysize in range (start,stop):
        norm_ham = normalize_hamming_distance(data, keysize)
        #keysizes.append((keysize, norm_ham))
        #if norm_ham < best_norm_ham:
        #    best_norm_ham = norm_ham
        #    best_keysize = keysize
        yield (keysize, norm_ham)


def generate_key(data, ch):
    key = ''
    for d in data:
        c = Counter(d)
        char,_ = c.most_common()[0]
        char = ord(char)
        char = chr(char^ch)
        key += char
    return key


def valid_key(key):
    if len(key) == 0:
        return False

    for ch, next_ch in zip(key, key[1:]):
        # implemeneting some language logic,
        # two spaces in a row is probably not the key
        if ch == ' ' and next_ch == ' ':
            return False
        # if ch is a charcter we just continue
        # to the next iteration
        if 32 <= ord(ch) <= 126:
            continue
        # the chracter is not valid, so this
        # is not the key
        return False
    
    return True


def find_key_candidates(data):
    # loops over all characters
    for ch in range(32,127):
        candidate = True
        cur_key = generate_key(data, ch)
        if not valid_key(cur_key):
            continue
        
        yield cur_key


def calculate_score(key):
    score = 0
    if len(key) == 0:
        return score
    most_frequent = 'etaoin'
    other_frequent = 'shrdlu'
    for ch in key:
        if ord(ch) < 48 and ch != ' ':
            score -= 5
        if ch in most_frequent:
            score += 5
        elif ch in other_frequent:
            score += 4
        elif ord(ch) in srange('A-Za-z'):
            score += 2
        elif ord(ch) in srange('0-9'):
            score += 2

    score /= len(key)    
    return score


def find_key(data, start, stop):
    
    keysizes = find_keysize(data, start, stop)
    best = (0,'')
    
    for keysize,_ in keysizes:
    
        tr = transpose(data, keysize)
        for key in find_key_candidates(tr):
            best_score, _ = best
            score = calculate_score(key)

            if score > best_score:
                best = (score,key) 

    _,key = best
    return key

