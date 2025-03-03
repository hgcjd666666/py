import json
import os
import re
import subprocess


def bv_to_av(BV):  # 把BA号转为AV号
	if BV.startswith("BV"):
		BV = BV[2:]  # 去除开头的BV号
	if len(BV) != 10:
		print("BV号长度不正确")
	code = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL2VG3guMTKNPAwcF"
	tmp1 = list()  # 初始化tmp1，用于存储转数字后的结果
	for i in BV:
		tmp1.append(code.index(i))  # 转数字
	code = "624859371"
	for i in range(len(code)):
		tmp1[i] *= 58 ** int(code[i])  # 乘上58的i次方，最后一个跳过
	tmp2 = int()  # 初始化tmp2，用于存储和
	for i in tmp1:
		tmp2 += i  # 求和
	tmp3 = tmp2 - 100618342136696320  # 求差
	tmp4 = tmp3 ^ 177451812  # 异或
	av = f"av{tmp4}"
	return av


def find_files(main_dir):
	for root, dirs, files in os.walk(main_dir):
		if "entry.json" in files:
			entry_path = os.path.join(root, "entry.json")
			yield entry_path


def download_to_aac(download_dir):
	output_dir = download_dir
	
	for entry_path in find_files(download_dir):
		try:
			# 读取entry.json
			with open(entry_path, 'r', encoding='utf-8') as f:
				entry_data = json.load(f)
				title = entry_data.get("title", "untitled")
			
			# 处理文件名中的非法字符
			safe_title = re.sub(r'[\\/*?:"<>|]', '_', title)
			output_filename = f"{safe_title}.aac"
			output_path = os.path.join(output_dir, output_filename)
			
			# 获取audio.m4s路径
			parent_dir = os.path.dirname(entry_path)
			subdirs = [d for d in os.listdir(parent_dir)
			           if os.path.isdir(os.path.join(parent_dir, d))]
			
			if len(subdirs) != 1:
				print(f"⚠️ 目录结构异常：{parent_dir} 包含 {len(subdirs)} 个子目录")
				continue
			
			audio_dir = os.path.join(parent_dir, subdirs[0])
			audio_path = os.path.join(audio_dir, "audio.m4s")
			
			if not os.path.exists(audio_path):
				print(f"⛔ 未找到音频文件：{audio_path}")
				continue
			
			# 使用ffmpeg转换
			cmd = [
				'ffmpeg',
				'-v', 'error',  # 减少输出信息
				'-i', audio_path,
				'-c:a', 'copy',  # 无损复制音频流
				'-y',  # 覆盖已存在文件
				output_path
			]
			
			subprocess.run(cmd, check=True)
			print(f"✅ 成功转换：{output_filename}")
		
		except json.JSONDecodeError:
			print(f"❌ JSON解析失败：{entry_path}")
		except subprocess.CalledProcessError as e:
			print(f"❌ FFmpeg转换失败：{e}")
		except Exception as e:
			print(f"❌ 发生未知错误：{str(e)}")


download_to_aac(r"F:\download")
# BA("BV17x411w7KC")  # av170001
