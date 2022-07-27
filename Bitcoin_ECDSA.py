#part1
#pip install pycoin安装python包


#定义散列、ECDSA签名和ECDSA签名验证函数（ECDSA使用secp256k1进行签名,SHA3-256进行验证）
from pycoin.ecdsa import generator_secp256k1, sign, verify
import hashlib, secrets
#哈希函数计算并返回 SHA3-256 哈希，表示为 256 位整数。
def sha3_256Hash(msg):
    hashBytes = hashlib.sha3_256(msg.encode("utf8")).digest()
    return int.from_bytes(hashBytes, byteorder="big")
#该函数获取文本消息和 256 位 secp256k1 私钥，并计算 ECDSA 签名 {r， s} 并将其作为一对 256 位整数返回。
def signECDSAsecp256k1(msg, privKey):
    msgHash = sha3_256Hash(msg)
    signature = sign(generator_secp256k1, privKey, msgHash)
    return signature
#该函数获取文本消息、ECDSA 签名 {r， s} 和 2*256 位 ECDSA 公钥（未压缩），并返回签名是否有效。
def verifyECDSAsecp256k1(msg, signature, pubKey):
    msgHash = sha3_256Hash(msg)
    valid = verify(generator_secp256k1, pubKey, msgHash, signature)
    return valid



# ECDSA sign message (using the curve secp256k1 + SHA3-256)
msg = "Message for ECDSA signing"
privKey = secrets.randbelow(generator_secp256k1.order())
signature = signECDSAsecp256k1(msg, privKey)
print("Message:", msg)
print("Private key:", hex(privKey))
print("Signature: r=" + hex(signature[0]) + ", s=" + hex(signature[1]))

# ECDSA verify signature (using the curve secp256k1 + SHA3-256)
pubKey = (generator_secp256k1 * privKey).pair()
valid = verifyECDSAsecp256k1(msg, signature, pubKey)
print("\nMessage:", msg)
print("Public key: (" + hex(pubKey[0]) + ", " + hex(pubKey[1]) + ")")
print("Signature valid?", valid)

# ECDSA verify tampered signature (using the curve secp256k1 + SHA3-256)
msg = "Tampered message"
valid = verifyECDSAsecp256k1(msg, signature, pubKey)
print("\nMessage:", msg)
print("Signature (tampered msg) valid?", valid)

#Result
Message: Message for ECDSA signing
Private key: 0x79afbf7147841fca72b45a1978dd7669470ba67abbe5c220062924380c9c364b
Signature: r=0xb83380f6e1d09411ebf49afd1a95c738686bfb2b0fe2391134f4ae3d6d77b78a, s=0x6c305afcac930a3ea1721c04d8a1a979016baae011319746323a756fbaee1811

Message: Message for ECDSA signing
Public key: (0x3804a19f2437f7bba4fcfbc194379e43e514aa98073db3528ccdbdb642e240, 0x6b22d833b9a502b0e10e58aac485aa357bccd1df6ec0fa4d398908c1ac1920bc)
Signature valid? True

Message: Tampered message
Signature (tampered msg) valid? False
