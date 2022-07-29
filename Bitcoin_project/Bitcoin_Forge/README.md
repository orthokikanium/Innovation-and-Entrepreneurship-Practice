# Bitcoin_project_Forge
forge a signature to pretend that you are Satoshi

# 项目完成人
李晨漪20.3班

github：orthokikanium
# 代码说明
思路：重新随机生成参数a、b，生成伪造的签名，并检验是否通过验证，是一个概率算法。
### ECDSA签名
![image](https://user-images.githubusercontent.com/91087648/181808010-88cde203-0b11-4127-9407-88ec4f6d1908.png)


### ECDSA验证签名
![image](https://user-images.githubusercontent.com/91087648/181808061-38b08a1e-52fb-424b-a435-c30a12a51f8b.png)


### 伪造签名
概率性算法，通过random.randrange(1, n - 1)随机选择a、b，计算签名r1、s1。

a= random.randrange(1, n - 1)

b = random.randrange(1, n - 1)

r1 = add(mul(a, G), mul(b, P))[0]

e1 = (r1 * a * Euc(b, n)) % n

s1 = (r1 * Euc(b, n)) % n


# 运行指导
可直接运行
# 运行截图
![image](https://user-images.githubusercontent.com/91087648/181807139-982bcbe8-38b9-4c6d-b302-895d40e4a2de.png)

# 参考文献
