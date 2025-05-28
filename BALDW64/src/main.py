import struct, math, os, unicodedata
from src.assets.constants import Constants as C
from src.assets import bitwise_functions as bit


def padding(message: bytes):
    message_len_bits = len(message) * 8
    message += b'\x80'
    while (len(message)) % 128 != 112:
        message += b'\x00'
    message += struct.pack('>QQ', 0, message_len_bits)

    return message


def get_digest(h0: list, desired_bits: int):

    total_hex_chars = 128   # 512 bits
    size_field_chars = 4    # 16 bits
    available_chars = total_hex_chars - size_field_chars   # 496 bits

    digest_chars = desired_bits // 4

    if digest_chars > available_chars:
        raise ValueError("Desired digest size is too large. Must be <= 496 bits!")
    
    # Generating Digest
    num_words = (digest_chars + 15) // 16
    full_digest = ''.join(f'{x:016x}' for x in h0[:num_words])
    trunc_digest = full_digest[:digest_chars]

    # Adding noise
    num_fake_chars = available_chars - digest_chars
    fake_bits = os.urandom(num_fake_chars // 2).hex() if num_fake_chars > 0 else ''

    digest_size_hex = f'{desired_bits:04x}'

    final_output = digest_size_hex + trunc_digest + fake_bits

    return final_output


def normalize_verf_str(s: str):
    s = s.strip().lower()
    s = unicodedata.normalize("NFKC", s)
    return s


def get_hash_signature(verf_str: str):
    normal_form = normalize_verf_str(verf_str)
    sig = 0

    for c in normal_form:
        sig ^= ((sig << 5) + (sig >> 2) + ord(c)) & 0xFFFFFFFFFFFFFFFF

    return sig


def baldw64(message: bytes, verf_str: str):
    message = padding(message=message)
    h0 = C.H.copy()

    for chunk_start in range(0, len(message), 128):
        chunk = message[chunk_start: chunk_start + 128]

        factors = [f for f in chunk if (f in b'123456789') and 48 % int(chr(f)) == 0]
        numbers = [n for n in chunk if n in b'0123456789']

        P = bit.Ψ(factors, numbers)

        w = list(struct.unpack('>16Q', chunk)) + [1] * 72

        for i in range(16, 88):
            log_term = int(math.log2(w[i - 11] + 3) * 1000000) if w[i - 11] + 3 > 0 else 0

            w.append(int((bit.λ0(w[i - 15]) + bit.rotl(w[i - 16], 12) + log_term\
                           + bit.λ1(w[i - 2]) + w[i - 16] + P)) & 0xFFFFFFFFFFFFFFFF)
            
            
        a, b, c, d, e, f, g, h, i0, j, k, l = h0

        for p in range(88):

    
            φ1 = (int(P) & 0xFFFFFFFFFFFFFFFF) + bit.λ0(j) + bit.diffuse(i0, k, l)
            φ2 = w[p] + bit.destr(a, b, c, C.K[p]) + bit.rotl((e ^ w[p]), 11)
            φ3 = bit.rotr(e, 11) + bit.fuse(a, b, c, l) + C.K[p]
            l = (int(P) & 0xFFFFFFFFFFFFFFFF) + φ2
            k = bit.λ0(l)
            j = l + k + (int(P) & 0xFFFFFFFFFFFFFFFF) + bit.λ0(k)
            i0 = bit.λ1(j) + φ3
            h = (f ^ bit.rotr(φ1 + i0, 7)) + bit.destr(b, c, d, C.K[p])
            g = h + φ2
            f = φ1 + bit.destr(i0, j, k, C.K[p])
            e = (int(P) & 0xFFFFFFFFFFFFFFFF) + φ3
            d = (g + a + bit.rotl(φ2, 13)) ^ bit.λ1(k)
            c = d
            b = d + φ3
            a = φ1 + φ2 + φ3

            # Shuffle variables periodically
            if i % 11 == 0:
                variables_1 = [b, d, a, l, k, e, f, g, i0, h, c, j]
                a, b, c, d, e, f, g, h, i0, j, k, l = variables_1

            elif i % 11 == 1:
                variables_2 = [k, c, i0, a, b, f, h, g, e, d, j, l]
                a, b, c, d, e, f, g, h, i0, j, k, l = variables_2

    sig = get_hash_signature(verf_str=verf_str)

    h0 = [(x + y ^ sig) & 0xFFFFFFFFFFFFFFFF for x, y in zip(h0, [a, b, c, d, e, f, g, h, i0, j, k, l])]

    bit_sizes = [256, 272, 288, 304, 336, 384, 400, 416, 432, 464, 480, 496]

    ord_value = sum(map(ord, list(verf_str)))
    # Normalise ord value for higher inputs
    adjusted_value = (ord_value // 4) if ord_value > 480 else ord_value

    desired_bits = min(bit_sizes, key=(lambda x: abs(x - adjusted_value)))

    final_digest = get_digest(h0=h0, desired_bits=desired_bits)

    return final_digest
