# 网络空间安全创新创业实践

---

包含**SM2,SM3,SM4,Bitcoin**相关功能与攻击的实现



> **作业提交**
> 时间：2022.7.31 下午3:00前
>
> 提交内容：Git仓库的网页地址，仓库设置公开，且包含README文件，需要明确几个内容(内容不全会影响成绩)
>
> 1. 小组成员，以及对应的git账户名称，用于对应个人贡献
> 2. 所做项目的简介、项目名称、完成人
> 3. 每个小组需要列一个清单，包含完成的项目、未完成的项目、有问题的项目及问题
> 4. 对每个项目：
>    A.具体的项目代码说明
>    B.运行指导(跑不起来的不算成功)
>    C.代码运行全过程截图(无截图无说明的代码不给分)
>    D.每个人的具体贡献说明及贡献排序(复制的代码需要标出引用)
> 5. 其他问题，联系助教或者写在仓库的明显位置均可
>
> 提交方式：各班成员交给班长，班长制作一个excel表格，总结一下布置的所有项目，并把每个小组提交仓库地址和包含的小组成员整理一下，在ddl之前发送给我即可
>
> 仓库中push时间超过ddl的不予考虑，短时间出现大量雷同push的会影响成绩，出现不合理的雷同，认定push时间靠后的项目违规



## 1.成员

|  姓名  |     学号     |                     Github id                     |
| :----: | :----------: | :-----------------------------------------------: |
| 李晨漪 |202000210103 | [orthokikanium](https://github.com/orthokikanium) |
| 李丽娜 |              |         [l921n](https://github.com/l921n)         |
| 赵欣宇 |              |                                                   |
| 胡焱彬 | 202000210013 |       [Hyan1ce](https://github.com/Hyan1ce)       |



## 2.项目简介

> ==修改格式：文件名、简介、完成人==

1. **SM3.py**

   SM3算法的实现(Python)

   > 完成人：Hyan1ce  胡焱彬

2. **MerkleTree.cpp**

   Merkle Tree的模拟实现与简单验证(c++)

   > 完成人：Hyan1ce  胡焱彬

3. **sm3_len_ext_attack**

   SM3 长度扩展攻击实现(Python)

   `my_sm3.py` 参照https://www.cnblogs.com/wcwnina/p/13604915.html 编写过程中使用的指定iv的sm3简单实现；

   `sm3_len_ext_attack.py` 实现初始消息为“Hello SDU CST!20220718”、附加消息为“202000210008”的长度扩展攻击。
   > 完成人：l921n  李丽娜
   > 
4.**Project: implement the naïve birthday attack of reduced SM3**
   > 完成人：orthokikanium  李晨漪


5.**Project: implement the Rho method of reduced SM3**
   > 完成人：orthokikanium  李晨漪


6.**Project: report on the application of this deduce technique in Ethereum with ECDSA**
   > 完成人：orthokikanium  李晨漪


7.**Project: impl sm2 with .RFC6979**
   > 完成人：orthokikanium  李晨漪


8.**Project: verify the above pitfalls with proof-of-concept code**
   > 完成人：orthokikanium  李晨漪


9.**Project: Implement the above ECMH scheme**
   > 完成人：orthokikanium  李晨漪


10.**Project: forge a signature to pretend that you are Satoshi**
   > 完成人：orthokikanium  李晨漪


11.**Project: send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself**
   > 完成人：orthokikanium  李晨漪


12.**Project: research report on MP**
   > 完成人：orthokikanium  李晨漪

## 3.项目清单

### 完成的项目

#### SM3.py
https://github.com/Hyan1ce/Innovation-and-Entrepreneurship-Practice/blob/main/SM3.py
#### SM3_len_ext_attack
https://github.com/Hyan1ce/Innovation-and-Entrepreneurship-Practice/tree/main/sm3_len_ext_attack
#### Bitcoin_Forge
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/Bitcoin_project/Bitcoin_Forge
#### Bitcoin_public_send_tx
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/Bitcoin_project/Bitcoin_public_send_tx
#### MPT
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/Bitcoin_project/MPT
#### Deduce
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/Deduce
#### ECMH_SM2
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/ECMH_SM2
#### impl_SM2_RFC6979
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/impl_SM2_RFC6979
#### SM2_pit
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/SM2_pit
#### SM3_Birthday_Attack
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM3_project/SM3_Birthday_Attack
#### SM3_Rho_Attack
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM3_project/SM3_Rho_Attack
### 有问题的项目

- [MerkleTree.cpp](https://github.com/Hyan1ce/Innovation-and-Entrepreneurship-Practice/blob/main/MerkleTree.cpp)

  **问题**：成功模拟Merkle Tree，但运行结果（root hash值）似乎与预期不符



## 4.项目具体说明

> ==统一格式：文件名（三级标题）、**A.代码说明  B.运行指导（输入范例） C.运行结果截图  D.贡献者（id+名字）**==



### **SM3.py**

**A.代码说明**：**实现SM3加密算法**，并列举两个例子验证运行结果，原理详见[国密算法标准SM3](http://www.oscca.gov.cn/sca/xxgk/2010-12/17/1002389/files/302a3ada057c4a73830536d03e683110.pdf)

- `sm3_iterate`：迭代函数
- `sm3_extend`：扩展函数
- `sm3_compress`：压缩函数
- `sm3_padding_to_512bits`：填充至512bits的整数倍
- 其他函数功能与函数名相同故不再赘述，如`_32bits_mod2Add`为mod2的32bit加法，`_32bits_xor`为32bits异或

**B.运行指导**：输入：616263（abc的ASCII码值，即求abc的Hash值）

​					   结果：66c7f0f4 62eeedd9 d1f2d46b dc10e4e2 4167c487 5cf2f7a2 297da02b 8f4ba8e0

> 注：运行指导已标注在主函数的注释中
>
>  	   其他输出项分别为填充结果、每轮压缩前的初始iv、迭代过程的中间值

**C.运行结果截图**：

![SM3result](https://github.com/Hyan1ce/image/blob/main/SM3%20result.png "SM3result")

**D.贡献者**：[Hyan1ce](https://github.com/Hyan1ce)  胡焱彬



### **MerkleTree.cpp**

**A.代码说明:Project: Impl Merkle Tree following RFC6962**

1. 首先定义Block结构体，作为区块；之后**利用随机数函数生成区块的内容(int)，用来模拟待Hash的值**

   > 叶子节点过多会导致栈溢出，故选择叶子节点个数为10000

2. 利用一个二维数组存储树中各个节点的Hash值

3. 利用`std::hash<int>`模拟hash过程，其中为方便起见，用**相加替代了级联**作为hash函数的输入，不过效果是相同的

4. 最后随机选取一个数，沿着Merkle Tree的hash路径计算出根hash值并比较，验证结果

**B.运行指导**：直接运行即可

**C.运行结果截图**：

![MerkleTree](https://github.com/Hyan1ce/image/blob/main/Merkle%20Tree.png "MerkleTree")

**D.贡献者**：[Hyan1ce](https://github.com/Hyan1ce)  胡焱彬



### **sm3_len_ext_attack**

**A.代码说明**：

任意M1，已知其长度len1与对应的hash值，可以构造合法的消息M = M2||padding||M3，其中M2、M3为任意消息，且可以满足SM3（M1||padding||M3）= SM3（M）

#### my_sm3.py 

1. 定义rotl函数，实现SM3过程中循环左移操作；

2. 将常数T_j内容存储在列表中；

3. 依次完成SM3中FF函数` sm3_ff_j `、GG函数` sm3_gg_j `、置换函数 `sm3_p_0` 与 `sm3_p_1` 、压缩函数` sm3_cf` 定义；

4. 编写可以实现自定义初始变量的SM3函数：

   ```python
   传入列表类参数 msg 与 指定初始变量 new_v，首先确定 msg 长度，实现消息填充：在 msg 末端添 1，添 k 个 0 至满足 len(msg) + 1 + k (mod 64) = 56，最后填充比特长度，此处利用struct模块中pack函数实现['>q'表示大端模式long long类型]
   
   实现迭代压缩时，由于伪造消息只需要对附加的消息进行加密，因此加密次数要比之前少一次，从消息的第64字节开始加密，即可得到hash值。
   
   最后完成格式化输出 result 即可完成 hash 。
   ```

   

#### sm3_len_ext_attack.py

1. 由于定义 sm3 函数传入参数为 list 类型且 库函数中 sm3 对 int 型数据进行处理，因此定义`convert`函数，完成 str 转换为对应 ASCII 码值组成的列表；代码如下：

   ```python
   def convert(msg_str):
       """
       将字符串类型消息转换成对应ASCII码组成的列表
       """
       msg = []
       for item in msg_str:
           msg.append(ord(item))
       return msg
   ```

2. 定义 padding 函数完成 padding ，过程与 my_sm3.py 中一致；但为便于后续处理 msg，需要完成全局 pad 处理，定义 pad 列表与对应` pad_str` 变量后，函数进行 global 声明即可。

3. 定义长度扩展攻击函数`len_ext_hash(known_hash, org_msg_len, exten_msg)`：

   ```python
   将known_hash分组，每组8个字节, 并转换为十进制整数，便于调入 sm3_hash 中；
   
   构造相同长度的随机消息 M2，这里选择构造相同长度的'9'，再进行padding以及附加消息的添加，将上述向量与添加完成的消息传入 my_sm3.sm3_hash 中完成hash。
   ```

4. 声明消息变量并确定内容，调用函数完成各消息的 hash ，比较得到的hash值是否可以满足SM3（M1||padding||M3）= SM3（M2||padding||M3），相同则攻击成功，否则失败。

**B.运行指导**：变量已定义完成，直接运行代码即可进行攻击检验

**C.运行结果截图**：结果如下：
![01.png](https://github.com/l921n/chaos/blob/main/01.png "SM3长度扩展攻击展示") 

**D.贡献者**：[l921n](https://github.com/l921n)  李丽娜

### 项目具体说明见链接各README文件
完成人：orthokikanium  李晨漪

注：实验提交时间比较集中，是重新整理了一遍所有的截图和README文件，用git push一直报错，就重新git clone提交了一遍。。
#### Bitcoin_Forge
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/Bitcoin_project/Bitcoin_Forge
#### Bitcoin_public_send_tx
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/Bitcoin_project/Bitcoin_public_send_tx
#### MPT
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/Bitcoin_project/MPT
#### Deduce
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/Deduce
#### ECMH_SM2
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/ECMH_SM2
#### impl_SM2_RFC6979
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/impl_SM2_RFC6979
#### SM2_pit
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM2_project/SM2_pit
#### SM3_Birthday_Attack
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM3_project/SM3_Birthday_Attack
#### SM3_Rho_Attack
https://github.com/orthokikanium/Innovation-and-Entrepreneurship-Practice/tree/main/SM3_project/SM3_Rho_Attack


