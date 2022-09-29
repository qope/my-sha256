# Ref: https://blog.boot.dev/cryptography/how-sha-2-works-step-by-step-sha-256/

import hashlib

message = "hello world"

# Pre-processing
b = []
for letter in message:
    b.append(bin(ord(letter))[2:].zfill(8))
length = len(b)*8
b.append("10000000")
to_add_num = 64 - (len(b) % 64)
b.extend(["00000000"]*to_add_num)
b[-1] = bin(length)[2:].zfill(8)
w = []
for i in range(0, len(b), 4):
    w.append(b[i]+b[i+1]+b[i+2]+b[i+3])
to_add_num = 64 - len(w)
w.extend(["0"*32]*to_add_num)

# Define helper functions
def xor(a, b):
    r = ""
    for i in range(len(a)):
        r = r + str(int(bool(int(a[i])) ^ bool(int(b[i]))))
    return r
def and_(a, b):
    r = ""
    for i in range(len(a)):
        r = r + str(int(bool(int(a[i])) and bool(int(b[i]))))
    return r
def not_(a):
    r = ""
    for i in range(len(a)):
        r = r + str(int(not bool(int(a[i]))))
    return r
def rotr(x, n): return x[-n:] + x[:-n]
def shr(x, n): return n * "0" + x[:-n]
def add(a, b): return bin(int(a, 2) + int(b, 2))[2:].zfill(32)[-32:]

# Define constants
k_ = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4','0xab1c5ed5', '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe','0x9bdc06a7', '0xc19bf174', '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f','0x4a7484aa', '0x5cb0a9dc', '0x76f988da', '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7','0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967', '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc','0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', '0xa2bfe8a1', '0xa81a664b','0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', '0x19a4c116','0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3','0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7','0xc67178f2']
k = [bin(int(x, 16))[2:].zfill(32) for x in k_]

h0 = "01101010000010011110011001100111"
h1 = "10111011011001111010111010000101"
h2 = "00111100011011101111001101110010"
h3 = "10100101010011111111010100111010"
h4 = "01010001000011100101001001111111"
h5 = "10011011000001010110100010001100"
h6 = "00011111100000111101100110101011"
h7 = "01011011111000001100110100011001"

# Create Message Schedule
for i in range(16, 64):
    s0 = xor(rotr(w[i-15], 7), xor(rotr(w[i-15], 18), shr(w[i-15], 3)))
    s1 = xor(rotr(w[i-2], 17), xor(rotr(w[i-2], 19), shr(w[i-2], 10)))
    w[i] = add(w[i-16], add(s0, add(w[i-7], s1)))

#  Compression
a = h0
b = h1
c = h2
d = h3
e = h4
f = h5
g = h6
h = h7

for i in range(64):
    S1 = xor(rotr(e, 6), xor(rotr(e, 11), rotr(e, 25)))
    ch = xor(and_(e, f), and_(not_(e), g))
    temp1 = add(h, add(S1, add(ch, add(k[i], w[i]))))
    S0 = xor(rotr(a, 2), xor(rotr(a, 13), rotr(a, 22)))
    maj = xor(and_(a,b), xor(and_(a,c), and_(b,c)))
    temp2 = add(S0, maj)
    h = g
    g = f
    f = e
    e = add(d, temp1)
    d = c
    c = b
    b = a
    a = add(temp1, temp2)

h0 = add(h0 , a)
h1 = add(h1 , b)
h2 = add(h2 , c)
h3 = add(h3 , d)
h4 = add(h4 , e)
h5 = add(h5 , f)
h6 = add(h6 , g)
h7 = add(h7 , h)

# Digest
result = hex(int(h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7, 2))[2:]
assert result == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

def test_hashlib():
    m = hashlib.sha256()
    m.update(b"hello world")
    r = m.digest().hex()
    assert r == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

test_hashlib()