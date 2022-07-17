# -*- coding: utf-8 -*-
# @Time : 2022-07-16 19:15
# @Author : Hyan1ce
# @Email : Hyanice_2502@outlook.com
# @File : SM3.py
# @Project : SM3


def _to_bits_bin(length: int, in_hex: hex) -> str:
    temp: str = bin(in_hex)[2:]
    temp = '0' * (length - len(temp)) + temp
    return temp


def _byte2hex(in_str: str) -> str:
    temp: str = hex(int(in_str, 2))[2:]
    last_str: str = '0' * (8 - len(temp)) + temp
    return last_str


def _32bits_xor(_32bits_1: str, _32bits_2: str) -> str:
    temp: str = ""
    for i in range(32):
        if _32bits_1[i] == _32bits_2[i]:
            temp += '0'
        else:
            temp += '1'
    return temp


def _32bits_not(_32bits: str) -> str:
    temp: str = ''
    for i in range(32):
        if _32bits[i] == '0':
            temp += '1'
        else:
            temp += '0'
    return temp


def _32bits_and(_32bits_1: str, _32bits_2: str) -> str:
    temp: str = ""
    for i in range(32):
        _1bit: str = ''
        if _32bits_1[i] == _32bits_2[i] == '1':
            temp += '1'
        else:
            temp += '0'
    return temp


def _32bits_or(_32bits_1: str, _32bits_2: str) -> str:
    temp: str = ""
    for i in range(32):
        _1bit: str = ''
        if _32bits_1[i] == _32bits_2[i] == '0':
            temp += '0'
        else:
            temp += '1'
    return temp


def round_left(num: int, in_str: str) -> str:
    temp: str = in_str
    for i in range(num):
        temp = temp[1:] + temp[0]
    return temp


def _32bits_mod2Add(_32bits_1: str, _32bits_2: str) -> str:
    cin: int = 0
    _sum: str = ''
    for i in range(32):
        temp: int = cin + int(_32bits_1[31 - i]) + int(_32bits_2[31 - i])
        _sum = str(temp % 2) + _sum
        if temp >= 2:
            cin = 1
        else:
            cin = 0
    return _sum


def _p0(x: str) -> str:
    temp = x
    _9move = ''
    _17move = ''
    for i in range(9):
        temp = temp[1:] + temp[0]
        _9move = temp
    temp = x

    for j in range(17):
        temp = temp[1:] + temp[0]
        _17move = temp
    return _32bits_xor(x, _32bits_xor(_9move, _17move))


def _p1(x: str) -> str:
    temp = x
    _15move = ''
    _23move = ''
    for i in range(15):
        temp = temp[1:] + temp[0]
        _15move = temp
    temp = x

    for j in range(23):
        temp = temp[1:] + temp[0]
        _23move = temp
    return _32bits_xor(x, _32bits_xor(_15move, _23move))


def Tj(j: int) -> str:
    hex_tj: hex
    if 0 <= j <= 15:
        hex_tj = 0x79cc4519
    else:
        hex_tj = 0x7a879d8a

    temp = _to_bits_bin(32, hex_tj)
    return temp


def FFj(j: int, x: str, y: str, z: str) -> str:
    if 0 <= j <= 15:
        return _32bits_xor(x, _32bits_xor(y, z))
    else:
        return _32bits_or(_32bits_or(_32bits_and(x, y),
                                     _32bits_and(x, z)), _32bits_and(y, z))


def GGj(j: int, x: str, y: str, z: str) -> str:
    if 0 <= j <= 15:
        return _32bits_xor(x, _32bits_xor(y, z))
    else:
        return _32bits_or(_32bits_and(x, y), _32bits_and(_32bits_not(x), z))


def sm3_padding_to_512bits(in_plaintext: str) -> str:
    temp: str = in_plaintext
    temp += '1'
    while len(temp) % 512 != 448:
        temp += '0'

    length: int = len(in_plaintext)
    bin_length: str = bin(length)[2:]
    head: str = '0' * (64 - len(bin_length))
    tail: str = head + bin_length
    _padded: str = temp + tail

    # show result
    print("Padded message:")
    num: int = 0
    for i in range(len(temp + tail) // 32):
        num += 1
        print(_byte2hex(_padded[32 * i:32 * i + 32]), end=' ')
        if num == 8:
            num = 0
            print('')
    return _padded


result_list: list = ["01110011100000000001011001101111", "01001001000101001011001010111001",
                     "00010111001001000100001011010111", "11011010100010100000011000000000",
                     "10101001011011110011000010111100", "00010110001100010011100010101010",
                     "11100011100011011110111001001101", "10110000111110110000111001001110"]  # store middle result

iv0: list = ["01110011100000000001011001101111", "01001001000101001011001010111001",
             "00010111001001000100001011010111", "11011010100010100000011000000000",
             "10101001011011110011000010111100", "00010110001100010011100010101010",
             "11100011100011011110111001001101", "10110000111110110000111001001110"]  # iv0


def sm3_iterate(in_str: str) -> list:
    n: int = len(in_str) // 512
    for i in range(n):
        iv: list = result_list
        sm3_compress(iv, in_str[512 * i:512 * i + 512])
    return result_list


def sm3_extend(bi: str) -> list:
    _Wj1 = []
    _Wj2 = []
    temp: str = bi
    for i in range(16):
        _Wj1 += [temp[32 * i:32 * i + 32]]
    for j in range(16, 68):
        _Wj1 += [_32bits_xor(_p1(_32bits_xor(_32bits_xor(_Wj1[j - 16], _Wj1[j - 9]), round_left(15, _Wj1[j - 3]))),
                             _32bits_xor(round_left(7, _Wj1[j - 13]), _Wj1[j - 6]))]

    for k in range(64):
        _Wj2 += [_32bits_xor(_Wj1[k], _Wj1[k + 4])]
    temp_list: list = [_Wj1, _Wj2]
    return temp_list


def sm3_compress(in_v: list, in_b: str) -> list:
    _v: list = in_v
    _b: str = in_b
    _Wj1: list = sm3_extend(_b)[0]
    _Wj2: list = sm3_extend(_b)[1]

    print('\n\nInitial IV of this round:')
    for x in range(8):
        print(_byte2hex(result_list[x]), end=' ')
    print('\n\nProcess of compression:', end=' ')

    for j in range(64):
        _SS1: str = round_left(7, _32bits_mod2Add(
            _32bits_mod2Add(round_left(12, _v[0]), _v[4]), round_left(j, Tj(j))))
        _SS2: str = _32bits_xor(_SS1, round_left(12, _v[0]))
        _TT1: str = _32bits_mod2Add(_32bits_mod2Add(FFj(j, _v[0], _v[1], _v[2]), _v[3]),
                                    _32bits_mod2Add(_SS2, _Wj2[j]))
        _TT2: str = _32bits_mod2Add(_32bits_mod2Add(GGj(j, _v[4], _v[5], _v[6]), _v[7]),
                                    _32bits_mod2Add(_SS1, _Wj1[j]))

        _v[3] = _v[2]
        _v[2] = round_left(9, _v[1])
        _v[1] = _v[0]
        _v[0] = _TT1
        _v[7] = _v[6]
        _v[6] = round_left(19, _v[5])
        _v[5] = _v[4]
        _v[4] = _p0(_TT2)

        # show compress result of each round
        print('')
        print(j, ': ', end=' ')
        for m in range(8):
            print(_byte2hex(_v[m]), end=' ')

    for s in range(8):
        result_list[s] = _32bits_xor(iv0[s], result_list[s])
        iv0[s] = result_list[s]
    _viPlus: list = []
    for i in range(8):
        _viPlus += [_32bits_xor(in_v[i], _v[i])]
    return _viPlus


if __name__ == "__main__":
    plaintext: str = input("Input the plaintext:")
    padded_plaintext: str = sm3_padding_to_512bits(bin(int(plaintext, 16))[2:].zfill(len(plaintext) * 4))

    # test1:
    # plaintext: str = "616263"  # abc
    # right answer: 66c7f0f4 62eeedd9 d1f2d46b dc10e4e2 4167c487 5cf2f7a2 297da02b 8f4ba8e0
    #
    # test2:
    # plaintext: str = "61626364" * 16
    # right answer: debe9ff9 2275b8a1 38604889 c18e5a4d 6fdb70e5 387e5765 293dcba3 9c0c5732

    ciphertext: list = sm3_iterate(padded_plaintext)

    print("\n\nResult of SM3 encrypt:")
    for tmp in range(8):
        temp_str: str = _byte2hex(ciphertext[tmp])
        print(temp_str, end=' ')
