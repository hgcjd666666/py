def delete_empty_folders(path):
	# 存储被删除的空文件夹路径
	deleted_folders = []
	
	# 使用os.walk遍历目录
	for root, dirs, files in os.walk(path, topdown=False):
		# 遍历当前目录下的文件夹
		for dir in dirs:
			dir_path = os.path.join(root, dir)
			# 检查文件夹是否为空
			if not os.listdir(dir_path):
				# 如果为空，则删除该文件夹
				os.rmdir(dir_path)
				# 输出被删除的文件夹路径
				print(f"删除空文件夹：{dir_path}")


import hashlib
import os


def get_file_hash(file_path, hash_func):
	"""
	计算文件的hash值
	"""
	hash_obj = hash_func()
	with open(file_path, 'rb') as f:
		chunk = f.read(4096)
		while chunk:
			hash_obj.update(chunk)
			chunk = f.read(4096)
	return hash_obj.hexdigest()


def find_duplicate_files(directory):
	file_sizes = {}
	duplicate_files = []
	for root, dirs, files in os.walk(directory):
		for file_ in files:
			file_path = os.path.join(root, file_)
			file_size = os.path.getsize(file_path)
			
			# 检查文件大小是否重复
			if file_size in file_sizes:
				# 如果文件大小相同，检查md5
				file_md5 = get_file_hash(file_path, hashlib.md5)
				if file_md5 in file_sizes[file_size]:
					# 如果md5相同，检查sha512
					file_sha512 = get_file_hash(file_path, hashlib.sha512)
					for dup_file_path in file_sizes[file_size][file_md5]:
						if get_file_hash(dup_file_path, hashlib.sha512) == file_sha512:
							# 如果sha512也相同，则添加到重复文件列表
							duplicate_files.append((file_path, dup_file_path))
				else:
					# 如果md5不同，添加到字典
					file_sizes[file_size][file_md5] = [file_path]
			else:
				# 如果文件大小不同，添加到字典
				file_sizes[file_size] = {get_file_hash(file_path, hashlib.md5): [file_path]}
	return duplicate_files


if __name__ == "__main__":
	choce = input("""功能列表：
	[1]查找重复文件
	[2]清理空文件夹
请选择一个功能使用：""")
	input_path = input("输入需要处理的路径：")
	if choce == "1":
		# 打印所有重复的文件路径
		for dup in find_duplicate_files(input_path):
			print(f"重复文件：“{dup[0]}”和“{dup[1]}”")
	elif choce == "2":
		delete_empty_folders(input_path)
	else:
		print("选项错误！")
