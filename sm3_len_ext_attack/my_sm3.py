import binascii
import struct
from math import ceil

def rotl(x,n):
    return ((x<<n) & 0xffffffff)|((x>>(32 - n)) & 0xffffffff)

T_j = [
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042
]

# SM3 实现
def sm3_ff_j(x, y, z, j):
    if j >= 0 and j < 16:
        ret = x ^ y ^ z
    elif j >= 16 and j < 64:
        ret = (x & y) | (x & z) | (y & z)
    return ret

def sm3_gg_j(x, y, z, j):
    if j >= 0 and j < 16:
        ret = x ^ y ^ z
    elif j >= 16 and j < 64:
        ret = (x & y) | ((~ x) & z)
    return ret

def sm3_p_0(x):
    return x ^ (rotl(x, 9)) ^ (rotl(x, 17))

def sm3_p_1(x):
    return x ^ (rotl(x, 15)) ^ (rotl(x, 23))

# SM3压缩函数
def sm3_cf(v_i, b_i):
    w = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i * 4,(i + 1) * 4):
            data = data + b_i[k] * weight
            weight = weight // 0x100
        w.append(data)

    for j in range(16, 68):
        w.append(0)
        w[j] = sm3_p_1(w[j-16] ^ w[j-9] ^ (rotl(w[j-3], 15))) ^ (rotl(w[j-13], 7)) ^ w[j-6]
        str1 = "%08x" % w[j]
    w_1 = []
    for j in range(0, 64):
        w_1.append(0)
        w_1[j] = w[j] ^ w[j+4]
        str1 = "%08x" % w_1[j]

    # 解包赋值
    a, b, c, d, e, f, g, h = v_i

    for j in range(0, 64):
        ss_1 = rotl(
            ((rotl(a, 12)) +
            e +
            (rotl(T_j[j], j % 32))) & 0xffffffff, 7
        )
        ss_2 = ss_1 ^ (rotl(a, 12))
        tt_1 = (sm3_ff_j(a, b, c, j) + d + ss_2 + w_1[j]) & 0xffffffff
        tt_2 = (sm3_gg_j(e, f, g, j) + h + ss_1 + w[j]) & 0xffffffff
        d = c
        c = rotl(b, 9)
        b = a
        a = tt_1
        h = g
        g = rotl(f, 19)
        f = e
        e = sm3_p_0(tt_2)

        a, b, c, d, e, f, g, h = map(
            lambda x:x & 0xFFFFFFFF ,[a, b, c, d, e, f, g, h])

    v_j = [a, b, c, d, e, f, g, h]
    return [v_j[i] ^ v_i[i] for i in range(8)]

def sm3_hash(msg, new_v):
    len1 = len(msg)
    reserve1 = len1 % 64

    # 添1
    msg.append(0x80)
    reserve1 = reserve1 + 1
    
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    # 添0
    for i in range(reserve1, range_end):
        msg.append(0x00)
        
    # 填充比特长度
    bit_length = len1 * 8
    msg.extend([int(x) for x in struct.pack('>q', bit_length)])

    group_count = round(len(msg) / 64) - 1
    
    B = []
    for i in range(0, group_count):
        B.append(msg[(i + 1) * 64:(i + 2) * 64])

    V = []
    V.append(new_v)
    for i in range(0, group_count):
        V.append(sm3_cf(V[i], B[i]))
    
    y = V.pop()
    
    result = ""
    # 格式化输出
    for i in y:
        result = '%s%08x' % (result, i)
    return result
