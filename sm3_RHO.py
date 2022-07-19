#Rho
import random
import sm3_birthdayattack

def RHO(t):
    num = int(t/4)                # 16进制位数
    x = hex(random.randint(0, 2**(t+1)-1))[2:]
    m= sm3.SM3(x)                # m= x1
    n = sm3.SM3(m)              # n = x2
    i = 1
    while m[:num] != n[:num]:
        i += 1
        m = sm3.SM3(m)              #m = x_i
        n = sm3.SM3(sm3.SM3(n))     # n = x_2i
    n = m          
    m = x             
    for j in range(i):
        if sm3.SM3(m)[:num] == sm3.SM3(n)[:num]:
            return sm3.SM3(x_a)[:num], m,n
        else:
            m = sm3.SM3(m)
            n = sm3.SM3(n)


if __name__ == '__main__':
    col, m1, m2 = RHO(4)
    print(m1)
    print(m2)
    print(col)
