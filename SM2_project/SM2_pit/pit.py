import random

#ECDSA
#gcd   Relatively_Prime
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b
#扩展欧几里得求模逆
def Euc(a, m):
    if gcd(a, m) != 1 and gcd(a, m) != -1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    if u1 > 0:
        return u1 % m
    else:
        return (u1 + m) % m

#椭圆曲线加法、乘法
def add(m, n):
    if (m == 0):
        return n
    if (n == 0):
        return m
    he = []
    if (m != n):
        if (gcd(m[0] - n[0], p) != 1 and gcd(m[0] - n[0], p) != -1):
            return 0
        else:
            k = ((m[1] - n[1]) * Euc(m[0] - n[0], p)) % p
    else:
        k = ((3 * (m[0] ** 2) + a) * Euc(2 * m[1], p)) % p
    x = (k ** 2 - m[0] - n[0]) % p
    y = (k * (m[0] - x) - m[1]) % p
    he.append(x)
    he.append(y)
    return he

def mul(n, l):
    if n == 0:
        return 0
    if n == 1:
        return l
    t = l
    while (n >= 2):
        t = add(t, l)
        n = n - 1
    return t

def ECDSA_sig(m, n, G, d,k):
    e = hash(m)
    R = mul(k, G)
    r = R[0] % n
    s = (Euc(k, n) * (e + d * r)) % n
    return r, s

def ECDSA_ver(m, n, G, r, s, P):
    e = hash(m)
    w = Euc(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = add(mul(v1, G), mul(v2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % n == r):
            print('true')
            return True
        else:
            print('false')
            return False



#SM2-pitfalls
def Leaking_K_of_Leaking_d(r,n,k,s,m):
    r_reverse=Euc(r,n)
    e=hash(m)
    d=r_reverse * (k*s-e)%n
    return d

def Reuse_K_of_Leaking_d(r1,s1,m1,r2,s2,m2,n):
    e1=hash(m1)
    e2=hash(m2)
    d=((s1 * e2 - s2 * e1) * Euc((s2 * r1 - s1 * r1), n)) % n
    return d

def Using_Same_K(s1,m1,s2,m2,r,d1,d2,n):
    e1=hash(m1)
    e2=hash(m2)
    d2_1 = ((s2 * e1 - s1 * e2 + s2 * r * d1) * Euc(s1 * r, n)) % n
    d1_1 = ((s1 * e2 - s2 * e1 + s1 * r * d2) * Euc(s2 * r, n)) % n
    if(d2==d2_1 and d1_1==d1):
        print("成功")
        return 1
    else:
        return 

def Verify_without_m(e, n, G, r, s, P):
    w = Euc(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = add(mul(v1, G), mul(v2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % n == r):
            print('true')
            return True
        else:
            print('false')
            return False
            
def Pretend(r, s, n, G, P):
    u = random.randrange(1, n - 1)
    v = random.randrange(1, n - 1)
    r1 = add(mul(u, G), mul(v, P))[0]
    e1 = (r1 * u * Euc(v, n)) % n
    s1 = (r1 * Euc(v, n)) % n
    Verify_without_m(e1, n, G, r1, s1, P)

def Schnorr_Sign(m, n, G, d,k):
    R = mul(k, G)
    e = hash(str(R[0]) + m)
    s = (k + e * d) % n
    return R, s

def Schnorr_and_ECDSA(r1, s1, R, s2, m, n):
    e1 = int(hash(m))
    e2 = int(hash(str(R[0]) + m))
    d = ((s1 * s2 - e1) * Euc((s1 * e2 + r1), n)) % n
    return d
if __name__ == '__main__':

    m = '2022'
    m_1="xxxx"
    x=5
    y=1
    G = [5, 1]
    a = 2
    b = 2
    p = 17
    n = 19
    k=2
    d = 5
    P = mul(d, G)


    print("k泄露")
    if (d == Leaking_K_of_Leaking_d(r,n,k,s,m)):
        print("成功")

    print("k重用")
    r_1,s_1=ECDSA_sig(m_1,n,G,d,k)
    r_2,s_2=ECDSA_sig(m,n,G,7,k)
    if (d == Reuse_K_of_Leaking_d(r,s,m,r_1,s_1,m_1,n)):
        print("成功")
        
    print("相同k")
    Using_Same_K(s_1,m_1,s_2,m,r,5,7,n)

    #  r,-s同样为有效签名
    print("5. 测试 r,-s是否为有效签名---------------------------------------------")
    print("测试结果为：")
    Ecdsa_Verify(m,n,G,r,-s,P)
    print("#------------------------------------------------------------#")
    #——————————————————————————————————————————test_VERSION 1.2—————————————————————————————————————————————#
    # 伪装中本聪
    print("6. 伪装中本聪---------------------------------------------")
    print("伪装是否成功：")
    Pretend(r,s,n,G,P)
    print("#------------------------------------------------------------#")
    #——————————————————————————————————————————test_VERSION 1.2—————————————————————————————————————————————#
    # Schnorr_Sign签名、ecdsa签名使用相同的d，k，导致密钥泄露
    print("6. Schnorr_Sign签名、ecdsa签名使用相同的d，k，导致密钥泄露---------------------------------------------")
    r3,s3=Schnorr_Sign(m,n,G,d,k)#第六问
    d2=Schnorr_and_ECDSA(r,s,r3,s3,m,n)
    print("破解是否成功：")
    print(d == d2)
    print("#------------------------------------------------------------#")




