# SM2_Project_ECMH 
Implement the above ECMH scheme

# 项目完成人
李晨漪20.3班

github：orthokikanium
# 代码说明
## 实验内容
ECMH SM2椭圆曲线公钥加密算法

## 主要函数

(1)ext_gcd(a,b)。扩展欧几里得算法，即 a mod b的逆元，返回的第一个值为结果。

(2) sameAdd(xl,y1)。计算椭圆曲线上2*(x1,y1)。

(3)NsameA dd(x1,y1,x_G,y_G)。返回(x3,y3)=(x1,y1)+(x_G,y_G)。

(4)multiply(x1,y1,k,x_G,y_G)。调用函数(2)(3)，使用类似快速模指数算法，计算(x1,y1)=k(x_G,y_G)。

(5)Point_bit(x1,y1)。选用未压缩格式，将(x1,y1)化为比特串。

(6)SHA256(str)。利用hashlib.sha256()将str加密。

(7)KDF(x,klen)。调用SHA256函数进行密钥扩展。

(8)xor(bit_M,t)。进行逐比特异或。

(9)bit_Point(hexC1)。将16进制字符串转为点坐标。

(10)Point_Cl_in(Point_C1)。判断这个点是否在方程上。
# 运行指导
可直接运行python文件
# 运行截图
<img width="416" alt="image" src="https://user-images.githubusercontent.com/91087648/181784927-8a0a7306-9025-49eb-ba07-ab55940b3581.png">

# 参考文献
https://blog.csdn.net/joker_clown/article/details/101114356?spm=1001.2014.3001.5506
