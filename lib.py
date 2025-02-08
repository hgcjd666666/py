"""
这是一个代码库
调用方法：
import lib
使用方法：
lib.get_md5(123)
意思是获取字符串“123”的md5

不要使用exec函数运行，否则save和load不收支持
"""
import datetime
import getpass
import hashlib
import os
import platform
import random
import string
import subprocess
import sys
from ast import literal_eval as eval_safe

import psutil

import time

eval_safe("124527")


def multiplication_table():
	for a in range(1, 10):
		for b in range(1, 10):
			if b <= a:
				print("%sx%s=%s" % (a, b, a * b), end="  ")


def current_time():
	while True:
		sys.stdout.write(time.strftime("\r%Y/%m/%d %H:%M:%S"))


def md5(data: bytes):
	# if isinstance(data, bytes):
	md5 = hashlib.md5()
	md5.update(data)
	return md5.hexdigest()


# 之前写的密钥，现在发现密钥可以填任意的字符串
'''
def key():
	key_type = input("请输入密钥类型，可以输入的有(正整数)(非数字)：")
	while True:
		if key_type == "正整数":
			print("如果输入的不是正整数将会忽略小数点后的数字")
			key_type = 1
			break
		elif key_type == "非数字":
			print("非数字的长度只能为1，安全性低，确认要使用吗？")
			while True:
				temp = input("(Y/N)：")
				if temp == "N" or temp == "n":
					key_type = 1
					print("已为您切换到正整数模式")
					break
				elif temp == "Y" or temp == "y":
					break
				else:
					temp = input("输入内容有误，请重新输入(不区分大小写)：")
				break
			key_type = 2
			break
		else:
			key_type = input("您输入的密钥类型有误，请重新输入：")
	key = input("请输入密钥内容：")
	while True:
		if key_type == 1:
			try:
				key = int(key)
				break
			except:
				if key == "":
					key = input("您输入的密钥是空的，请重新输入：")
				key = input("您输入的密钥里包含非数字内容，请重新输入：")
		elif key_type == 2:
			try:
				key = ord(key)
				break
			except:
				if key == "":
					key = input("您输入的密钥是空的，请重新输入：")
				key = input("您输入的密钥里包含数字或长度大于1，请重新输入：")
	return key
'''


def clear():
	if platform.platform().split("-")[0] == "Windows":
		os.system("cls")
	elif platform.platform().split("-")[0] == "macOS" or platform.platform().split("-")[0] == "Linux":
		os.system("clear")


def timer_math(time):
	if time == "":
		time = random.randint(1, 2333)
		return ("使用方法：\n直接调用即可\n例子：\nprint(timer_math(timer_math(" +
		        time + ")))\n输出：\n" + timer_math(timer_math(time)))
	if time > 60:
		minute = int(time / 60)
		if minute > 60:
			hour = int(minute / 60)
			if hour > 24:
				day = int(hour / 24)
				# 月就算不出来了，应为有的月是30天，有的月是31天
				back = f"{day}天{hour}时{minute}分{time}秒"
			else:
				back = f"{hour}时{minute}分{time}秒"
		else:
			back = f"{minute}分{time}秒"
	else:
		back = f"{time}秒"
	return str(back)


def error_code(data):
	print("程序出现问题，请联系作者，错误码：\n" + str(data) + "\n")


def error(data):
	print("程序出现问题，请联系作者，错误内容：\n" + str(data) + "\n")


def strencrypt(texto, key):
	# def encrypt(texto):
	if key == "null":
		key = "áéíóúÁÉÍÚÓàèìòùÀÈÌÒÙäëïöüÄËÏÖÜñÑ´"
	abecedario = string.printable + key
	abecedario2 = []
	nummoves = random.randint(1, len(abecedario))
	indexs = []
	
	texttoenc = []
	
	for l in range(0, len(abecedario)):
		abecedario2.append(abecedario[l])
	
	for let in range(0, len(texto)):
		texttoenc.append(texto[let])
	
	for letter in texto:
		indexs.append(abecedario2.index(letter))
	
	for move in range(0, nummoves):
		abecedario2 += abecedario2.pop(0)
	
	texto = []
	
	for i in range(0, len(indexs)):
		texto.append(abecedario2[indexs[i]])
		texto.append(".")
	
	fintext = ""
	
	for letter2 in range(0, len(texto), 2):
		fintext += texto[letter2]
	
	fintext = str(nummoves) + "." + fintext
	
	return fintext


def strdecrypt(texto, key):
	# def decrypt(texto):
	texto = texto.split(".")
	if key == "null":
		key = "áéíóúÁÉÍÚÓàèìòùÀÈÌÒÙäëïöüÄËÏÖÜñÑ´"
	abecedario = string.printable + key
	abecedario2 = []
	nummoves = int(texto[0])
	indexs = []
	finalindexs = []
	textode1 = texto[1]
	textode2 = []
	
	for l in range(0, len(abecedario)):
		abecedario2.append(abecedario[l])
	
	for letter in range(0, len(textode1)):
		textode2.append(textode1[letter])
	
	for index in range(0, len(textode1)):
		indexs.append(abecedario.index(textode1[index]))
	
	for move in range(nummoves, 0):
		abecedario2 += abecedario2.pop(27)
	
	for value in indexs:
		newval = value - nummoves
		finalindexs.append(newval)
	
	textofin = ""
	
	for i in range(0, len(finalindexs)):
		textofin += abecedario2[finalindexs[i]]
	
	return textofin


# 检测中英文字符
def is_all_chinese(strs: str):
	# 检验是否全是中文字符
	for _char in strs:
		if not '\u4e00' <= _char <= '\u9fa5':
			return False
	return True


def is_contains_chinese(strs: str):
	# 检验是否含有中文字符
	for _char in strs:
		if '\u4e00' <= _char <= '\u9fa5':
			return True
	return False


def is_all_english(strs: str):
	# 检测是否全是英文字符
	for i in strs:
		if i not in string.ascii_lowercase + string.ascii_uppercase:
			return False
	return True


def is_contains_english(strs: str):
	# 检测是否含有英文字符
	if (u'\u0041' <= strs <= u'\u005a') or (u'\u0061' <= strs <= u'\u007a'):
		return True
	else:
		return False


def get_system():
	# “Windows”“Linux”“macOS”
	return platform.platform().split("-")[0]


"""
def save(variable_name, variable_data=None):
	is_self = False
	try:
		globals()[variable_name]
	except KeyError:
		if variable_data == None:  # 是私有变量并且未传人值则抛出异常
			raise ValueError("变量为私有的并且为传入值")
		is_self = True
	folder_name = sys.argv[0] + ".save"
	file_name = os.path.join(folder_name, variable_name)
	os.makedirs(folder_name, exist_ok=True)
	with open(file_name, "w") as f:
		if is_self:
			f.write(variable_data)
		else:
			f.write(globals()[variable_name])
"""


def save(*args, **kwargs):
	folder_name = sys.argv[0] + ".data"  # 获取脚本名称并添加.data后缀
	if len(args) == 2 and len(kwargs) == 0:
		# 传入两个参数（"a", 1）：第一个为变量名，第二个为变量值
		variable_name, variable_data = args
	elif len(args) == 0 and len(kwargs) == 1:
		# 传入一个参数（a=1）：自动获取变量名和值
		variable_name, variable_data = list(kwargs.items())[0]
	else:
		raise ValueError("参数格式不正确。请传入一个关键字参数或两个位置参数（变量名和变量值）。")
	
	file_name = os.path.join(folder_name, variable_name)
	# 创建保存数据的文件夹
	os.makedirs(folder_name, exist_ok=True)
	# 构造文件路径
	file_name = os.path.join(folder_name, variable_name)
	# 将数据写入文件
	with open(file_name, "w", encoding="UTF-8") as f:
		f.write(str(variable_data))


def load(variable_name):
	folder_name = sys.argv[0] + ".data"
	file_name = os.path.join(folder_name, variable_name)
	os.makedirs(folder_name, exist_ok=True)
	try:
		with open(file_name, "r", encoding="UTF-8") as f:
			return f.read()
	except FileNotFoundError:
		print("Error：读取保存的变量时出现问题 文件不存在")
		return None


def log(data):
	date = datetime.datetime.now()
	time = date.strftime("%H:%M:%S")
	date = date.strftime("%Y-%m-%d")
	
	log_folder = sys.argv[0] + f".log"
	
	log_file = os.path.join(log_folder, f"{date}.log")
	os.makedirs(log_folder, exist_ok=True)
	
	with open(log_file, "a", encoding="UTF-8") as f:
		f.write(f"{time}\t{data}\n")


def debug():
	python_version = sys.version  # 获取python信息
	machine = platform.machine()  # 获取系统类型
	print(f"Python {python_version} on {machine.lower()}")  # 拼接成想python命令的字符串
	print("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.")  # 帮助信息
	while True:
		try:
			code = input(">>> ")  # 获取命令
			if len(code):  # 命令不为空就执行，否则再次获取，不然抛出“SyntaxError：invalid syntax (<string>, line 0)”与原版不符
				run = eval(code)  # 运行命令（因为eval比exec多个返回才用它）
				if run != None:  # 命令返回不为空才输出命令的返回值
					if type(run) == str:
						print(f"'{run}'")  # 是字符串就加个引号
					else:
						print(run)  # 不是字符串直接输出
		except KeyboardInterrupt:
			print("KeyboardInterrupt")  # 捕获特殊异常：^C按键
		except EOFError:  # 捕获特殊异常：^D按键
			exit()
		except SystemExit as e:  # 捕获退出
			exit()
		except Exception as e:  # 捕获其他异常并打印
			print(f"{str(type(e))[8:-2]}：{e}")


def Error(e: Exception):
	return f"{str(type(e))[8:-2]}：{e}"


def get_command_input():
	command_input = list()
	for i in sys.argv:
		command_input.append(i)
	return command_input


def gci():
	return get_command_input()


def rootrun(
		cmd: str,
		getmeg="Password:",
		failmsg="Sorry, try again.",
		failendmsg="sudo: 3 incorrect password attempts"):
	for i in range(4):
		password = getpass.getpass(getmeg)
		sudo_cmd = ["sudo", "-S", "-v"]
		password += "\n"  # 末尾添加换行符
		index = subprocess.run(sudo_cmd,
		                       input=password.encode(),
		                       stdout=subprocess.DEVNULL,
		                       stderr=subprocess.DEVNULL
		                       )
		
		# 密码正确
		if not index.returncode:
			if cmd:
				sudo_cmd = ["sudo", "-S"] + [cmd]
				password += "\n"  # 末尾添加换行符
				index = subprocess.run(sudo_cmd, input=password.encode())
				print(sudo_cmd)
				print(index)
			return 1
		
		print(failmsg)
		# 没机会了（重试次数达到3次）
		if i == 2:
			print(failendmsg)
			return 0


def check_root(msg: str):
	# 获取当前进程的用户ID
	uid = os.getuid()
	if uid != 0:
		raise SystemError(msg)


def pr(data):
	if get_parent_process_name() == "pycharm":  # Mac上的pycharm的运行功能使用sys.stdout.write会看不见输出（windows上是pycharm32/64.exe）
		print(data)
	else:
		sys.stdout.write(f"\r{data}")  # sys.stdout.flush()  # 刷新缓冲区，确保立即打印


def get_parent_process_name():  # 获取父进程名称
	current_process = psutil.Process()
	parent_process = current_process.parent()
	if parent_process:
		return parent_process.name()
	else:
		return None


def get_null_device():
	if os.name == "nt":  # 'nt' 表示 Windows 操作系统
		return "NUL"
	else:
		return "/dev/null"


def get_filename():
	return sys.argv[0]


def file_md5(file_path):
	"""计算文件的MD5哈希值"""
	md5 = hashlib.md5()
	try:
		with open(file_path, 'rb') as f:
			for chunk in iter(lambda: f.read(4096), b''):
				md5.update(chunk)
		return md5.hexdigest()
	except OSError as e:
		print(f"无法读取文件 {file_path}: {e}")
		return None
