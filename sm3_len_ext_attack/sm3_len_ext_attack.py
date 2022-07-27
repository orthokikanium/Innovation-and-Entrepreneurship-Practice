from gmssl import sm3
import struct
import my_sm3

def convert(msg_str):
    '''
    将字符串类型消息转换成对应ASCII码组成的列表
    '''
    msg = []
    for item in msg_str:
        msg.append(ord(item))
    return msg

def len_ext_hash(known_hash, org_msg_len, exten_msg):
    """
    指定附加消息的 SM3 长度扩展攻击
    known_hash: 获取的hash值
    org_msg_len: 原消息长度
    exten_msg: 附加的消息
    """
    iv_new = []
    message = ""
    # 将known_hash分组，每组8个字节, 并转换为十进制整数
    for r in range(0, len(known_hash), 8):
        iv_new.append(int(known_hash[r:r + 8], 16))

    # 用相同长度的 9 伪造消息
    if org_msg_len > 64:
        for i in range(0, org_msg_len // 64 * 64):
            message += '9'
    for i in range(0, org_msg_len % 64):
        message += '9'

    # padding，添附加消息
    message = padding(convert(message))
    message.extend(convert(exten_msg))
    msg = convert(exten_msg)
    return my_sm3.sm3_hash(message, iv_new)


def padding(msg):
    '''
    实现padding
    '''
    msg_len = len(msg)
    
    # 添 1
    msg.append(0x80)
    msg_end = (msg_len + 1) % 64
    range_end = 56
    if msg_end > range_end:
        range_end = range_end + 64

    # 添 0
    for i in range(msg_end, range_end):
        msg.append(0x00)

    # 添比特长度
    bit_len = msg_len * 8
    msg.extend([int(x) for x in struct.pack('>q', bit_len)])

    # 处理全局 pad
    for j in range(msg_len, len(msg)):
        global pad
        global pad_str
        pad.append(msg[j])
        pad_str += str(hex(msg[j]))
    return msg

# 自定义原始待hash消息
org_msg = "Hello SDU CST!20220718"

# 利用库函数完成原始hash
org_msg_hash = sm3.sm3_hash(convert(org_msg))
org_msg_len = len(org_msg)

# 附加消息
ext_msg = "202000210008"
pad_str = ""
pad = []

# 长度扩展攻击实例,hash内容为 random_msg||padding||ext_msg
guess_hash = len_ext_hash(org_msg_hash, org_msg_len, ext_msg)

# new_msg = org_msg||padding||ext_msg
new_msg = convert(org_msg)
new_msg.extend(pad)
new_msg.extend(convert(ext_msg))

new_msg_str = org_msg + pad_str + ext_msg

# 使用库函数完成新消息hash
new_hash = sm3.sm3_hash(new_msg)

print("原始消息org_msg:\n{}".format(org_msg))
print("原始消息长度:",len(org_msg))
print("原始hash值:",org_msg_hash)
print("附加消息ext_msg:\n{}".format(ext_msg))

print("*" * 100)
print("ext_msg的hash值:",guess_hash)

print("*" * 100)
print("new_msg = org_msg||padding||ext_msg:\n{}".format(new_msg_str))
print("new_msg 的hash值:",new_hash)

if new_hash == guess_hash:
    print("长度扩展攻击成功!")
else:
    print("攻击失败")
