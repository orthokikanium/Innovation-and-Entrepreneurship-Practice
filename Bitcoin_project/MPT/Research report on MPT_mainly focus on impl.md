Research Report on MPT

# 前言

我们小组在回看了Introduction to Ethereum这一节的录屏后，对Merkle Tree这一新奇的概念产生了极大的好奇。遂上网查阅相关资料，根据博客对Merkle Patricia Trie实现的代码进行一个复现。

本文首先简要介绍一些相关知识作为实验准备。

由于中文写作一些专业词汇翻译过来可能有些许奇怪=_=...

# 以太坊中的Merkling

Merkle树是使区块链发挥作用的基本组成部分。如果在没有Merkle树的情况下制作区块链，所有不可信地使用区块链的能力都无法实现。多亏了Merkle树，才可以构建在所有计算机和大大小小的笔记本电脑，智能手机，甚至物联网设备上运行的以太坊节点。

首先，定义。在最一般的意义上，Merkle树是一种将大量数据“块”（“chunks” ）散列在一起的方法，它依赖于将块拆分为桶（buckets），其中每个桶仅包含几个块，然后获取每个桶的哈希值并重复相同的过程，继续这样做，直到剩余的哈希总数成为只有一个： 根哈希（root hash）。

Merkle树最常见和最简单的形式是二进制Mekle树，其中桶总是由两个相邻的块或哈希组成;它可以描述如下：

<img src="https://blog.ethereum.org/wp-content/uploads/2015/11/merkle.png" alt="img" style="zoom: 50%;" />

这种算法为什么不将所有块连接在一起形成一个大块，并使用常规的哈希算法呢？请接着往下看。因为它允许一种称为Merkle proofs的证明机制：

<img src="https://blog.ethereum.org/wp-content/uploads/2015/11/merkle2.png" alt="img" style="zoom:50%;" />

Merkle proofs由一个块、树的根哈希和“分支”组成，该“分支”由从块到根的路径上向上的所有哈希组成。可以验证哈希，至少对于该分支，是一直沿着树向上移动的，因此给定的块实际上位于树中的该位置。

应用程序很简单：假设有一个大型数据库，并且数据库的全部内容都存储在Merkle树中，其中Merkle树的根是公开和可信的（例如，它由足够多的受信任方进行数字签名，或者有很多工作证明）。然后，想要对数据库进行键值查找的用户（例如。“告诉我位置85273中的对象”）可以要求Merkle证明，并在收到证明时验证它是正确的，因此收到的值*实际上*位于具有该特定根的数据库中的位置85273。它允许扩展用于对*少量*数据（如哈希）进行身份验证的机制，以对可能未限大小的*大型*数据库进行身份验证。

### Merkle Proofs in Bitcoin

Merkle proofs的原始应用是在比特币中，在中本聪区块链中，使用Merkle proofs来存储每个区块中的交易：

<img src="https://blog.ethereum.org/wp-content/uploads/2015/11/mining.jpg" alt="img" style="zoom: 50%;" />

这样的好处是中本聪描述为“简化的支付验证”的概念：“轻量级客户端”只能下载*区块头*链（不是下载*每个交易和*每个区块），即每个区块的80字节数据块，仅包含五个内容：

- A hash of the previous header上一个标头的哈希
- A timestamp时间戳
- A mining difficulty value挖矿难度值
- A proof of work nonce工作证明
- A root hash for the Merkle tree containing the transactions for that block.Merkle 树的根哈希，其中包含该块的事务。

如果轻量级客户端想要确定交易的状态，它可以要求一个Merkle proofs，表明一个特定的交易在Merkle树中的一个，其根在主链的块头中。

但是比特币中定义的轻量级客户端也存在局限性。譬如，虽然它们可以证明包含交易，但它们不能证明当前状态的任何内容（例如，数字资产的持有，名称注册，金融合同的状态等）。如果交易效果取决于几个先前交易的效果，也就是说，这些交易本身取决于以前的交易，因此最终我们就必须对整个链中的每笔交易进行身份验证。为了解决这个问题，以太坊基于Merkle树的概念，进一步拓展了它的功能。

### Merkle Proofs in Ethereum

以太坊中的每个区块标题不仅包含一个Merkle树，还包含三种对象的*三*棵树：

- Transactions交易
- Receipts (essentially, pieces of data showing the *effect* of each transaction)收据（本质上是显示每笔交易*效果*的数据片段）
- State状态

<img src="https://blog.ethereum.org/wp-content/uploads/2015/11/ethblockchain_full.png" alt="img" style="zoom: 67%;" />

这允许轻量级客户端获得多种查询的可验证答案，譬如：

- 此交易是否已包含在特定区块中？
- 告诉客户过去30天内此地址发出的某类交易或事件的所有实例
- 我的账户当前余额是多少？
- 此帐户是否存在？
- 假设在此合约上运行此事务。输出会是什么？

第一个由交易树处理;第三个和第四个由状态树处理，第二个由收据树处理。前四个计算起来相当简单;服务器只需找到对象，获取 Merkle 分支（从对象向上到树根的哈希列表），然后用分支回复回轻量级客户端。

第五个也由状态树处理，但计算方式更复杂。在这里，我们需要构建**Merkle state transition proof**。这里直接引用博客对概念进行解释：Essentially, it is a proof which make the claim “if you run transaction on the state with root , the result will be a state with root , with log and output ” (“output” exists as a concept in Ethereum because every transaction is a function call; it is not theoretically necessary).“如果你在具有root的状态上运行事务，结果将是具有root，log和输出的状态”（“输出”在以太坊中作为一个概念存在，因为每个事务都是一个函数调用;这在理论上是没有必要的）。`T``S``S'``L``O`

以下也是引用直接翻译的:

为了计算证明，服务器在本地创建一个假块，将状态设置为 S，并在应用事务时假装是轻量级客户端。也就是说，如果应用交易的过程需要客户端确定账户的余额，则轻量级客户端会进行余额查询。如果轻量级客户端需要检查特定合约存储中的特定项目，则轻量级客户端会对此进行查询，依此类推。服务器正确“响应”自己的所有查询，但会跟踪它发回的所有数据。然后，服务器向客户端发送来自所有这些请求的组合数据作为证明。然后，客户执行完全相同的程序，但*使用提供的证据作为其数据库*;如果其结果与服务器声明的结果相同，则客户端接受证明。

<img src="https://blog.ethereum.org/wp-content/uploads/2015/11/lightproof.png" alt="img" style="zoom: 33%;" />

### Patricia Trees

上面提到，最简单的默克尔树是二叉默克尔树;但是，以太坊中使用的树更复杂也就是“Merkle Patricia tree”。

二进制默克尔树可以用于验证“list”格式的信息;从本质上讲，一系列块接一个地出现。对于交易树来说，这一数据结构也很好，因为一旦创建树，*编辑*需要多少时间并不重要，因为树只需要创建一次。

但是，对于状态树，情况会更复杂。以太坊中的状态基本上由键值映射组成，其中密钥是地址，值是帐户声明，列出每个帐户的余额，随机数，代码和存储（其中存储本身就是一棵树）。以下给出一个例子the Morden testnet genesis state：

```
{
    "0000000000000000000000000000000000000001": {
        "balance": "1"
    },
    "0000000000000000000000000000000000000002": {
        "balance": "1"
    },
    "0000000000000000000000000000000000000003": {
        "balance": "1"
    },
    "0000000000000000000000000000000000000004": {
        "balance": "1"
    },
    "102e61f5d8f9bc71d0ad4a084df4e65e05ce0e1c": {
        "balance": "1606938044258990275541962092341162602522202993782792835301376"
    }
}
```

然而，与交易历史记录不同的是，状态需要经常更新：帐户的余额和随机数经常更改，而且经常插入新帐户，并且经常插入和删除存储中的密钥。因此，我们需要一个数据结构，可以实现在插入，更新编辑或删除操作后快速计算新的树根，而无需重新计算整个树。

同时还具有以下两个理想的特性：

- 树的深度是有界的。否则，攻击者可以通过操纵树变得如此之深以至于每个单独的更新变得非常慢来执行拒绝服务攻击。
- 树的根仅取决于数据，而不取决于进行更新的顺序。以不同的顺序进行更新，甚至从头开始重新计算树，都不应该更改根目录。

# 参考文献

- [以太坊|以太坊基金会博客 (ethereum.org)](https://blog.ethereum.org/2015/11/15/merkling-in-ethereum/)
- [Implementing Merkle Tree and Patricia Trie | by Kashish Khullar | Coinmonks | Medium](https://medium.com/coinmonks/implementing-merkle-tree-and-patricia-trie-b8badd6d9591)
- [以太坊的Merkle Patricia Trees - Rockwater Web](https://rockwaterweb.com/ethereum-merkle-patricia-trees-javascript-tutorial/)
- [Trie, Merkle, Patricia: A Blockchain Story (kronosapiens.github.io)](http://kronosapiens.github.io/blog/2018/07/04/patricia-trees.html)Merkle 树的根哈希，其中包含该块的事务。