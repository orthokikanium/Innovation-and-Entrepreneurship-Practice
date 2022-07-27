# 创新创业实践

包含SM2,SM3,SM4,Bitcoin相关功能与攻击的实现



## 文件内容

1. **SM3.py**

   SM3算法的实现(Python)

2. **MerkleTree.cpp**

   Merkle Tree的模拟实现与简单验证(c++)
   
3. **sm3_len_ext_attack**
   
   SM3 长度扩展攻击实现(python)

   my_sm3.py 参照https://www.cnblogs.com/wcwnina/p/13604915.html 编写过程中使用的指定iv的sm3简单实现；

   sm3_len_ext_attack.py 实现初始消息为“Hello SDU CST!20220718”、附加消息为“202000210008”的长度扩展攻击。




## 实验原理

### **SM3.py**

按部就班实现SM3加密算法，并列举两个例子验证运行结果，原理略，详见国密算法标准SM3



### **MerkleTree.cpp**

1. 首先定义Block结构体，作为区块；之后利用随机数函数生成区块的内容(int)，用来模拟待Hash的值

   > 叶子节点过多会导致栈溢出，故选择叶子节点个数为10000

2. 利用一个二维数组存储树中各个节点的Hash值

3. 利用`std::hash<int>`模拟hash过程，其中为方便起见，用**相加替代了级联**作为hash函数的输入，不过效果是相同的

4. 最后随机选取一个数，沿着Merkle Tree的hash路径计算出根hash值并比较，验证结果



### **sm3_len_ext_attack**

任意M1，已知其长度len1与对应的hash值，可以构造合法的消息M = M2||padding||M3，其中M2、M3为任意消息，且可以满足SM3（M1||padding||M3）= SM3（M）

## 实验过程

### 长度扩展攻击实现细节

#### my_sm3.py 

1）定义rotl函数，实现SM3过程中循环左移操作；

2）将常数T_j内容存储在列表中；

3）依次完成SM3中FF函数 sm3_ff_j 、GG函数 sm3_gg_j 、置换函数 sm3_p_0 与 sm3_p_1 、压缩函数 sm3_cf 定义；

4）编写可以实现自定义初始变量的SM3函数：

    传入列表类参数 msg 与 指定初始变量 new_v，首先确定 msg 长度，实现消息填充：在 msg 末端添 1，添 k 个 0 至满足 len(msg) + 1 + k (mod 64) = 56，最后填充比特长度，此处利用struct模块中pack函数实现['>q'表示大端模式long long类型]
    
    实现迭代压缩时，由于伪造消息只需要对附加的消息进行加密，因此加密次数要比之前少一次，从消息的第64字节开始加密，即可得到hash值。
    
    最后完成格式化输出 result 即可完成 hash 。
    
#### sm3_len_ext_attack.py

1）由于定义 sm3 函数传入参数为 list 类型且 库函数中 sm3 对 int 型数据进行处理，因此定义convert函数，完成 str 转换为对应 ASCII 码值组成的列表；代码如下：

    def convert(msg_str):
    '''
    将字符串类型消息转换成对应ASCII码组成的列表
    '''
    msg = []
    for item in msg_str:
        msg.append(ord(item))
    return msg

2）定义 padding 函数完成 padding ，过程与 my_sm3.py 中一致；但为便于后续处理 msg，需要完成全局 pad 处理，定义 pad 列表与对应 pad_str 变量后，函数进行 global 声明即可。

3）定义长度扩展攻击函数len_ext_hash(known_hash, org_msg_len, exten_msg)：

    将known_hash分组，每组8个字节, 并转换为十进制整数，便于调入 sm3_hash 中；
    
    构造相同长度的随机消息 M2，这里选择构造相同长度的'9'，再进行padding以及附加消息的添加，将上述向量与添加完成的消息传入 my_sm3.sm3_hash 中完成hash。

4）声明消息变量并确定内容，调用函数完成各消息的 hash ，比较得到的hash值是否可以满足SM3（M1||padding||M3）= SM3（M2||padding||M3），相同则攻击成功，否则失败。

### 长度扩展攻击结果展示
变量已定义完成，直接运行代码即可进行攻击检验；代码运行结果如下：
![图片未加载](https://github.com/l921n/chaos/blob/main/01.png "SM3长度扩展攻击展示")
