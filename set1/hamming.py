from utils import chunkify, srange


def bytes_to_bin(byteseq):
    return ''.join(format(ord(b), '08b') for b in byteseq)


def hamming_distance(a, b):
    seq1 = bytes_to_bin(a)
    seq2 = bytes_to_bin(b)
    if len(seq1) != len(seq2):
        n = len(seq1)-len(seq2)
        seq2 += '0'*n
    return sum(1 for bit1, bit2 in zip(seq1, seq2) if bit1 != bit2)


def normalize_hamming_distance(data, n):
    chunks1 = chunkify(data, n)
    chunks2 = chunkify(data[1:], n)
    length = len(data)/n
    return sum(hamming_distance(c1,c2)/n for c1,c2 in zip(chunks1, chunks1))/length

