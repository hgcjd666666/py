import hashlib
import os


def calculate_md5(path):
	"""计算文件的MD5哈希值，处理异常并返回None"""
	hash_md5 = hashlib.md5()
	try:
		with open(path, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return hash_md5.hexdigest()
	except OSError as e:
		print(f"计算MD5失败 {path}: {e}")
		return None


def find_duplicate_files(directory):
	"""查找重复文件并返回分组列表"""
	size_dict = {}
	directory = os.path.abspath(directory)
	
	# 按文件大小分组
	for root, _, files in os.walk(directory):
		for file in files:
			path = os.path.join(root, file)
			if os.path.isfile(path):
				try:
					size = os.path.getsize(path)
				except OSError as e:
					print(f"获取文件大小失败 {path}: {e}")
					continue
				if size == 0:
					continue  # 跳过空文件
				size_dict.setdefault(size, []).append(path)
	
	# 对相同大小文件进行MD5校验
	duplicates = []
	jump = calculated = int()
	for size, paths in size_dict.items():
		if len(paths) < 2:
			jump += len(paths)
			continue
		
		md5_dict = {}
		for path in paths:
			md5 = calculate_md5(path)
			if md5 is not None:
				md5_dict.setdefault(md5, []).append(path)
				calculated += 1
		
		for md5_group in md5_dict.values():
			if len(md5_group) > 1:
				sorted_group = sorted(md5_group)
				duplicates.append(sorted_group)
	
	print(f"MD5计算完成\n\t应计算{jump + calculated}个\n\t实际计算{calculated}个\n\t跳过了{jump:.3f}%的文件")
	return duplicates


def delete_duplicates(duplicates_list):
	"""删除重复文件模块"""
	deleted_count = 0
	for group in duplicates_list:
		# 保留第一个文件（路径最短的），删除其他
		to_delete = group[1:]
		for path in to_delete:
			try:
				os.remove(path)
				print(f"已删除：{path}")
				deleted_count += 1
			except Exception as e:
				print(f"删除失败 [{path}]: {e}")
	print(f"\n共删除 {deleted_count} 个重复文件")


def delete_empty_folders(directory):
	"""递归删除空文件夹（无需确认）"""
	deleted_count = 0
	directory = os.path.abspath(directory)
	
	# 自底向上遍历目录树，否包含空文件夹的文件夹不会被删除
	for root, dirs, files in os.walk(directory, topdown=False):
		for dir_name in dirs:
			dir_path = os.path.join(root, dir_name)
			try:
				if not os.listdir(dir_path):  # 检查是否为空
					os.rmdir(dir_path)
					print(f"已删除空文件夹：{dir_path}")
					deleted_count += 1
			except Exception as e:
				print(f"删除失败 [{dir_path}]: {e}")
	
	print(f"共清理 {deleted_count} 个空文件夹")


if __name__ == "__main__":
	choice = input("""功能列表：
	[1] 查找重复文件
	[2] 清理空文件夹
请选择一个功能使用：""")
	
	input_path = input("输入需要处理的路径：").strip()
	if not os.path.isdir(input_path):
		print("错误：目录不存在")
		exit()
	
	if choice == "1":
		duplicates = find_duplicate_files(input_path)
		if duplicates:
			print("\n发现以下重复文件组（每组保留第一个文件）：")
			for i, group in enumerate(duplicates, 1):
				print(f"\n组 {i}（共 {len(group)} 个重复）:")
				print(f"  保留：{group[0]}")
				for path in group[1:]:
					print(f"  删除：{path}")
			
			# 新增删除确认
			if input("\n是否删除重复文件？[y/n] ").lower() == 'y':
				delete_duplicates(duplicates)
			else:
				print("取消删除操作")
		else:
			print("未发现重复文件")
	
	elif choice == "2":
		print("\n开始清理空文件夹...")
		delete_empty_folders(input_path)
	
	else:
		print("无效选项！")
