import time
import datetime
import binascii
from Crypto.Cipher import DES

# DES加密
def encrypt(plain_text, key):
	# 确保密钥长度为8字节
	key = key[:8]
	des = DES.new(key.encode(), DES.MODE_ECB)
	padded_text = plain_text + (8 - len(plain_text) % 8) * chr(8 - len(plain_text) % 8)
	encrypted_text = des.encrypt(padded_text.encode())
	return binascii.hexlify(encrypted_text).decode()

# 生成激活码
def generate_activation_code(device_id, key, duration=[0, 0, 0, 0, 1, 0, 0]):
	# 计算哈希值
	# code_hash_ = int(((device_id + 2023) * 1997) / 2 - 824)
	# code_hash = int((1997*d+(2023*1997-824*2))/2)
	# code_hash = int((1997*d+4038283)/2)
	code_hash = int(998.5*device_id+2019141.5)
	# print(code_hash)
	# code_hash = int(code_hash)
	# print(code_hash==code_hash_)
	# print(code_hash,code_hash_)
	# 当前时间
	now = datetime.datetime.now()
	
	# 计算失效时间
	days, hours, minutes, seconds, milliseconds = duration
	expiration_time = now + datetime.timedelta(
		days=days,
		hours=hours,
		minutes=minutes,
		seconds=seconds,
		milliseconds=milliseconds
	)
	
	# 转换为时间戳（毫秒）
	activation_time = int(expiration_time.timestamp() * 1000)
	
	# 激活码内容
	activation_code_content = f"{code_hash:013d}{activation_time:013d}"
	print(activation_code_content)
	# 加密激活码
	encrypted_code = encrypt(activation_code_content, key)
	return encrypted_code

# 示例
device_id = int(input("输入设备ID："))
key = "IFuoZezG"  # 密钥
# 天、时、分、秒、毫秒
# duration = [1, 0, 0, 0, 0]  # 一天
duration = [0, 1, 0, 0, 0]  # 一小时
# print(duration)
activation_code = generate_activation_code(device_id, key, duration)
print(activation_code)