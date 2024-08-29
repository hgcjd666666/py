"""
这是一个代码库
调用方法：
import lib
使用方法：
lib.get_md5(123)
意思是获取字符串“123”的md5
"""
# from ast import literal_eval as eval
def save(variable_name, variable_data=None):
	is_self = False
	try:
		globals()[variable_name]
	except KeyError:
		if variable_data == None:  # 是私有变量并且未传人值则抛出异常
			raise ValueError("变量为私有的并且为传入值")
		is_self = True
	import sys
	folder_name = sys.argv[0] + ".save"
	import os
	file_name = os.path.join(folder_name, variable_name)
	os.makedirs(folder_name, exist_ok=True)
	with open(file_name, "w") as f:
		if is_self:
			f.write(variable_data)
		else:
			f.write(globals()[variable_name])


def load(variable_name):
	import sys
	folder_name = sys.argv[0] + ".save"
	import os
	file_name = os.path.join(folder_name, variable_name)
	os.makedirs(folder_name, exist_ok=True)
	try:
		with open(file_name, "r") as f:
			return f.read()
		# globals()[variable_name] = f.read()
	except FileNotFoundError:
		# print("Error：读取保存的变量时出现问题 文件不存在")
		# globals()[variable_name] = str()
		return None


def log(data):
	from datetime import datetime

	date = datetime.now()
	time = date.strftime("%H:%M:%S")
	date = date.strftime("%Y-%m-%d")
	import sys

	log_folder = sys.argv[0] + f".log"
	import os

	log_file = os.path.join(log_folder, f"{date}.log")
	os.makedirs(log_folder, exist_ok=True)

	with open(log_file, "a") as f:
		f.write(f"{time}\t{data}\n")


def debug():
	import sys
	import platform
	python_version = sys.version  # 获取python信息
	machine = platform.machine()  # 获取系统类型
	print(f"Python {python_version} on {machine.lower()}")  # 拼接成想python命令的字符串
	print("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.")  # 帮助信息
	while True:
		try:
			code = input(">>> ")  # 获取命令
			if len(code):  # 命令不为空就执行，否则再次获取，不然抛出“SyntaxError：invalid syntax (<string>, line 0)”与原版不符
				run = eval(code)  # 运行命令
				if run != None:  # 命令返回不为空才输出命令的返回值
					if type(run) == str:
						print(f"'{run}'")  # 是字符串就加个引号
					else:
						print(run)  # 不是字符串直接输出
		except KeyboardInterrupt:
			print("KeyboardInterrupt")  # 捕获特殊异常：^C按键
		except EOFError:  # 捕获特殊异常：^D按键
			# exit()
			break
		except SystemExit as e:  # 捕获其他异常并打印
			break
		except Exception as e:  # 捕获其他异常并打印
			print(f"{str(type(e))[8:-2]}：{e}")


def Error(e):
	return f"{str(type(e))[8:-2]}：{e}"


def multiplication_table():
	for a in range(1, 10):
		for b in range(1, 10):
			if b <= a:
				print("%sx%s=%s" % (a, b, a * b), end="  ")


def current_time():
	import time
	import sys
	while True:
		sys.stdout.write(time.strftime("\r%Y/%m/%d %H:%M:%S"))


def QRcode(QRcode_data, fill_color, back_color, path):
	QRcode_data = str(QRcode_data)
	fill_color = str(fill_color)
	back_color = str(back_color)
	path = str(path)
	# QRcode_data是二维码内容；fill_color是二维码颜色；back_color是二维码的背景颜色；path是文件保存路径
	import qrcode
	from PIL import Image
	# QRCode 类名
	qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=1)
	qr.add_data(str(QRcode_data))
	qr.make()
	# fill_color = "black" back_color = "white"
	img = qr.make_image(fill_color=fill_color, back_color=back_color)
	img.show()

	# 获取img尺寸
	width = img.size[0] // 4

	height = img.size[1] // 4
	icon = Image.open(path)

	# 获取icon的尺寸
	icon_w = icon.size[0]
	icon_h = icon.size[1]

	if icon_w > width:
		icon_w = width
	if icon_h > height:
		icon_h = height

	# resize()重新定义尺寸
	icon = icon.resize((icon_w, icon_h))

	x = (img.size[0] - icon_w) // 2
	y = (img.size[1] - icon_h) // 2

	# paste(obj, (x,y)) 粘贴
	img.paste(icon, (x, y))
	img.show()


def get_md5(data):
	data = str(data)
	import hashlib
	if isinstance(data, str):
		data = data.encode("utf-8")
		md = hashlib.md5()
		md.update(data)
		return md.hexdigest()


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


def time_sleep(second):  # emmmmmmmmmm，现在发现可以用多线程。。。
	if second == "":
		return "作者的话：\n  这是一个样本，内容看代码\n  不看代码的话就把这个当成普通的等待来用\n\n用法：\n  print(time_sleep(second))\n  可以打印成功或者失败\n\nby~"
	try:
		int(second + second)
	except:
		print("传入参数“second”错误！")
		print("“second”仅支持数字")

	import time
	present_time = time.time()
	#############################################
	#										   #
	# 代码写在这，不要在这写等待，不要写太耗费时间的代码 #
	#										   #
	#############################################
	'''
	if
		time.sleep(second - (present_time - time.time()))
	'''
	while True:
		if time.time() == present_time + second:
			return "运行完毕"  # 运行成功就返回“运行完毕”
			break
		elif time.time() > present_time + second:
			return "错误：当前时间大于目标时间，可能是执行时的写了等待"  # 运行失败就返回错误
			break


def clear():
	import platform
	import os
	if platform.platform().split("-")[0] == "Windows":
		os.system("cls")
	elif platform.platform().split("-")[0] == "macOS" or platform.platform().split("-")[0] == "Linux":
		os.system("clear")


def pause():
	# input("按任意键继续...")
	input("按回车继续...")


def custom_pause(data):
	input(data)


def timer_open():
	import time
	return time.time()


def timer_math(time):
	if time == "":
		import redoam
		time = redoam.readint(1, 2333)
		return "使用方法：\n直接调用即可\n例子：\nprint(timer_math(timer_math(" + time + ")))\n输出：\n" + timer_math(
			timer_math(time))
	if time > 60:
		minute = int(time / 60)
		if minute > 60:
			hour = int(minute / 60)
			if hour > 24:
				day = int(hour / 24)
				# 月就算不出来了，应为有的月是30天，有的月是31天
				back = str(day + "天" + hour + "时" + minute + "分" + time + "秒")
			else:
				back = str(hour + "时" + minute + "分" + time + "秒")
		else:
			back = str(minute + "分" + time + "秒")
	else:
		back = str(time + "秒")
	return str(back)


def error_code(data):
	print("程序出现问题，请联系作者，错误码：\n" + str(data) + "\n")


def error(data):
	print("程序出现问题，请联系作者，错误内容：\n" + str(data) + "\n")


def 文本加密(texto, key):
	import string
	from random import randint
	# def encrypt(texto):
	if key == "null":
		key = "áéíóúÁÉÍÚÓàèìòùÀÈÌÒÙäëïöüÄËÏÖÜñÑ´"
	abecedario = string.printable + key
	abecedario2 = []
	nummoves = randint(1, len(abecedario))
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


def 文本解密(texto, key):
	import string
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
def is_all_chinese(strs):
	# 检验是否全是中文字符
	for _char in strs:
		if not '\u4e00' <= _char <= '\u9fa5':
			return False
	return True


def is_contains_chinese(strs):
	# 检验是否含有中文字符
	for _char in strs:
		if '\u4e00' <= _char <= '\u9fa5':
			return True
	return False


def is_all_english(strs):
	# 检测是否全是英文字符
	import string
	for i in strs:
		if i not in string.ascii_lowercase + string.ascii_uppercase:
			return False
	return True


def is_contains_english(strs):
	# 检测是否含有英文字符
	if (u'\u0041' <= strs <= u'\u005a') or (u'\u0061' <= strs <= u'\u007a'):
		return True
	else:
		return False


def print_(*objects, sepr=" ", end="\n", t=None):
	# 已知BUG：在输出时sleep的话控制符也会被算进去
	# 基本颜色变化：	支持的颜色: 红 绿 黄 蓝 紫 青 白 黑 和 l红 l绿 l黄 l蓝 l紫 l青 l白 l黑[注意这个是小写的L]	‘\\’+颜色 -> 字体颜色(前景色)改变 ;	‘\\’+颜色 -> 背景色改变
	# 特殊控制符：	‘\\’ 去除一切渲染	‘\\clear’ 清屏	‘\\under’ 添加下划线	’\\nounder’关闭下划线	‘\\anti’反色(就是前景色和后景色互换)	 ‘\\noanti’关闭反色	‘\\hide’隐藏光标	’\\show’显示光标
	def replace(strname, *w):
		for x in w:
			strname = strname.replace(x[0], x[1])
		return strname

	import sys
	import time
	str_all = sepr.join(objects)
	str_all = replace(str_all, ("\\黑", "\033[30m"), ("\\clear", "\033[2J\033[00H"), ("\\under", "\033[4m"),
					  ("\\nounder", "\033[24m"), ("\\anti", "\033[7m"), ("\\noanti", "\033[27m"),
					  ("\\hide", "\033[25l"), ("\\show", "\033[25h"), ("\\红", "\033[31m"), ("\\绿", "\033[32m"),
					  ("\\黄", "\033[33m"), ("\\蓝", "\033[34m"), ("\\紫", "\033[35m"), ("\\青", "\033[36m"),
					  ("\\白", "\033[37m"), ("\\l红", "\033[91m"), ("\\l绿", "\033[92m"), ("\\l黄", "\033[93m"),
					  ("\\l蓝", "\033[94m"), ("\\l紫", "\033[95m"), ("\\l青", "\033[96m"), ("\\l白", "\033[97m"),
					  ("\\bl红", "\033[101m"), ("\\bl绿", "\033[102m"), ("\\bl黄", "\033[103m"),
					  ("\\bl蓝", "\033[104m"),
					  ("\\bl紫", "\033[105m"), ("\\bl青", "\033[106m"), ("\\bl白", "\033[107m"),
					  ("\\bl黑", "\033[100m"),
					  ("\\b红", "\033[41m"), ("\\b绿", "\033[42m"), ("\\b黄", "\033[43m"), ("\\b蓝", "\033[44m"),
					  ("\\b紫", "\033[45m"), ("\\b青", "\033[46m"), ("\\b白", "\033[47m"), ("\\b黑", "\033[40m"),
					  ("\\", "\033[0m"), ("//", "\\"), )
	if t == None:
		sys.stdout.write(str_all)
		sys.stdout.flush()
	else:
		for y in str_all:
			sys.stdout.write(y)
			sys.stdout.flush()
			time.sleep(t)
	sys.stdout.write(end)


def Copy_To_Clipboard(string):
	# 将需要的字符串或文字复制到剪切板.
	from Tkinter import Tk
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(string)
	r.update()


def test_system():
	import platform
	return platform.platform().split("-")[0]


def open_web(web):
	if web == "":
		return "使用方法：\n传入网站，例如：www.baidu.com\n或者传入iP，例如：110.242.68.66"
	web = "http://" + str(web)
	import webbrowser
	webbrowser.open(web)


def getuser():
	import os
	for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
		user = os.environ.get(name)
		if user:
			return user
	import pwd
	return pwd.getpwuid(os.getuid())[0]
