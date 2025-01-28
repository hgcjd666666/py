import os
import shutil


def split_file(file_path, chunk_size=512 * 1024 * 1024):  # 按照每512mb一个文件分割
	# 获取文件名和后缀
	file_name, file_extension = os.path.splitext(os.path.basename(file_path))

	# 读取文件
	with open(file_path, 'rb') as file_:
		chunk_number = 1
		while True:
			# 读取指定大小的数据块
			chunk = file_.read(chunk_size)
			if not chunk:
				break  # 文件结束
			# 创建新文件名
			new_file_name = f"{chunk_number}.{file_name}{file_extension}"
			# 写入新文件
			with open(new_file_name, 'wb') as new_file:
				new_file.write(chunk)
			chunk_number += 1


# 替换为你的文件路径
# file_path = 'path/to/your/large/file.ext'
file_path = input("输入文件路径：")
split_file(file_path)
