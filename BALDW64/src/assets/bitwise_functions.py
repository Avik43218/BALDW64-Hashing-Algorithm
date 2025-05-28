def rotr(x, n):
    return (x >> n) | (x << (64 - n)) & 0xFFFFFFFFFFFFFFFF

def rotl(x, n):
    return (x << n) | (x >> (64 - n)) & 0xFFFFFFFFFFFFFFFF
 
def fuse(w, x, y, z):
    return ((w & x) | (w & y)) ^ ((z & x) ^ (z & y))

def diffuse(x, y, z):
    return (~(x & ~(x & y)) & ~(z & ~(x & y)))

def destr(x, y, z, k):
    return ((x & rotl((x ^ k) + (y & z), 11)) ^ (y & rotl((y ^ k) + (z & x), 17))\
    ^ (z & rotl((z ^ k) + (x & y), 23)))

def λ0(x):
    return rotr(x, 16) & rotr(x, 54) & (x >> 36)

def λ1(x):
    return rotl(x, 5) & rotl(x, 27) & (x << 7)

def Ψ(b: list , a: list):
    # b = factors
    # a = numbers
    try:
        P = len(b) / len(a)
    except ZeroDivisionError:
        P = 0

    if P > 0 and P < 1:
        return float(P)
    else:
        return 0.0
