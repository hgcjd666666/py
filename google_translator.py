# -*- coding:utf-8 -*-
import json
import os
import random
import re
import time
import urllib
import urllib.request
import urllib.parse
import requests


class Google():
	def __init__(self):

		self.lang_dict = {
			'中文': 'zh-CN',
			'英文': 'en',
			'俄文': 'ru',
			'法文': 'fr',
			'日文': 'ja',
			'韩文': 'ko'
		}

		self.headers = {
			'Host': 'translate.googleapis.com',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0;)',
			# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
		}

		self.url = 'https://translate.google.com/translate_a/single'
		self.session = requests.Session()
		self.session.keep_alive = False

	def TL(self, input_string):
		constant_value = 406644
		large_constant_value = 3293161072
		delimiter = "."
		shift_pattern1 = "+-a^+6"
		shift_pattern2 = "+-3^+b+-f"
		character_values = []
		secondary_index = 0

		for character in input_string:
			character_code = ord(character)
			if character_code < 128:
				character_values.append(character_code)
			elif character_code < 2048:
				character_values.append((character_code >> 6) | 192)
				character_values.append(character_code & 63 | 128)
			else:
				if (55296 <= character_code <= 56319 and secondary_index + 1 < len(input_string) and 56320 <= ord(
						input_string[secondary_index + 1]) <= 57343):
					character_code = 65536 + ((character_code & 1023) << 10) + (
							ord(input_string[secondary_index + 1]) & 1023)
					character_values.append((character_code >> 18) | 240)
					character_values.append((character_code >> 12) & 63 | 128)
					secondary_index += 1
				else:
					character_values.append((character_code >> 12) | 224)
					character_values.append((character_code >> 6) & 63 | 128)
					character_values.append(character_code & 63 | 128)
			secondary_index += 1

		accumulated_value = constant_value
		for i in range(len(character_values)):
			accumulated_value += character_values[i]
			accumulated_value = self.RL(accumulated_value, shift_pattern1)

		accumulated_value = self.RL(accumulated_value, shift_pattern2)
		accumulated_value ^= large_constant_value
		if accumulated_value < 0:
			accumulated_value = (accumulated_value & 2147483647) + 2147483648
		accumulated_value %= 1000000
		return str(accumulated_value) + delimiter + str(accumulated_value ^ constant_value)

	def RL(self, value, pattern):
		base_character = 'a'
		operation_character = '+'
		for i in range(0, len(pattern) - 2, 3):
			operation_code = pattern[i + 2]
			if operation_code >= base_character:
				shift_value = ord(operation_code) - 87
			else:
				shift_value = int(operation_code)
			if pattern[i + 1] == operation_character:
				shift_value = value >> shift_value
			else:
				shift_value = value << shift_value
			if pattern[i] == operation_character:
				value = (value + shift_value) & 4294967295
			else:
				value ^= shift_value
		return value

	def ip_loader(self):
		# ip文件路径
		file_path = 'google_translate_ips.txt'

		if self.file_over_an_hour(file_path) is False:
			# 打开文件
			with open(file_path, 'r') as file:
				# 读取整个文件内容到一行
				ip_text = file.read()
				# 注意：这会去除字符串末尾的空元素（如果有的话）
				ip_list = ip_text.strip().split('\n')
		else:
			url = 'https://bbs.binmt.cc/google_translate_ips.txt'
			header = {
				'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0;)',
			}
			res = requests.get(url, headers=header)
			if res.status_code == 200:
				ip_list = res.text.strip().split('\n')
				if ip_list:
					# 在这里，我们使用换行符'\n'来连接列表中的IP地址
					ip_text = '\n'.join(ip_list)
					# 将结果写入到ip.txt文件中
					with open(file_path, 'w') as file:
						file.write(ip_text)

		return random.choice(ip_list) if ip_list else ''

	def file_over_an_hour(self, file_path):
		try:
			# 获取文件的最后修改时间戳
			file_mtime = os.path.getmtime(file_path)
			# 获取当前时间的时间戳
			current_time = time.time()
			# 计算时间差（秒）
			time_difference = current_time - file_mtime
			# 判断时间差是否超过3600秒（即1小时）
			if time_difference > 3600:
				return True
			else:
				return False
		except Exception as e:
			return None

	def buildUrl(self, text, tk, sl, tl):
		# baseUrl = 'https://translate.google.com/translate_a/single'
		ip = self.ip_loader()
		baseUrl = 'http://' + ip + '/translate_a/single'
		baseUrl += '?client=webapp&'  # 这里client改成webapp后翻译的效果好一些 t翻译的比较差 ..
		baseUrl += 'sl=' + str(sl) + '&'  # 原语言
		baseUrl += 'tl=' + str(tl) + '&'  # 目标语言
		baseUrl += 'hl=zh-CN&'
		baseUrl += 'dt=at&'
		baseUrl += 'dt=bd&'
		baseUrl += 'dt=ex&'
		baseUrl += 'dt=ld&'
		baseUrl += 'dt=md&'
		baseUrl += 'dt=qca&'
		baseUrl += 'dt=rw&'
		baseUrl += 'dt=rm&'
		baseUrl += 'dt=ss&'
		baseUrl += 'dt=t&'
		baseUrl += 'ie=UTF-8&'
		baseUrl += 'oe=UTF-8&'
		baseUrl += 'clearbtn=1&'
		baseUrl += 'otf=1&'
		baseUrl += 'pc=1&'
		baseUrl += 'srcrom=0&'
		baseUrl += 'ssel=0&'
		baseUrl += 'tsel=0&'
		baseUrl += 'kc=2&'
		baseUrl += 'tk=' + str(tk) + '&'  # 校验
		content = urllib.parse.quote(text)
		baseUrl += 'q=' + content  # 待翻译文本
		return baseUrl

	def getHtml(self, session, url, headers):
		try:
			return session.get(url, headers=headers)
		except Exception as e:
			return None

	def translate(self, from_lang, to_lang, text):
		tk = self.TL(text)
		url = self.buildUrl(text, tk, from_lang, to_lang)
		# print(url)
		res = self.getHtml(self.session, url, self.headers)

		if res.status_code != 200:
			match = re.search(r'<title>(.*?)</title>', res.text, re.DOTALL)
			# requests.get('https://backend.cyzone.cn/system/index/dingding?id=bestla&text=谷歌翻译失败：' + match.group(1) if match else str(res.status_code))
			print('谷歌翻译失败：' + match.group(1) if match else str(res.status_code))
			return ''
		else:
			return res.json()[0][0][0]


if __name__ == '__main__':
	gg = Google()
	text = '你好， 新的我'
	print(gg.translate('zh-CN', 'en', text))
