import os
import shutil


def merge_files(source_dir, output_file):
	# 获取源目录中的所有文件
	files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
	# 按照文件名排序，确保合并的顺序是正确的
	files.sort()

	# 创建输出文件
	with open(output_file, 'wb') as _:
		pass
	# 打开输出文件
	for file_ in files:
		with open(output_file, 'ab') as outfile:  # 每次都以追加的方式写入文件，每个分文件重新追加一次
			# 构建完整的输入文件路径
			file_path = os.path.join(source_dir, file_)
			# 打开分割的文件（输入文件）并读取内容
			with open(file_path, 'rb') as infile:
				shutil.copyfileobj(infile, outfile)


# 替换为你的源目录和输出文件路径
# source_dir = 'path/to/your/split/files'
# output_file = 'path/to/your/merged/file.ext'
# source_dir = input("将需要合并的文件放到同一目录下并保证没有其它文件后输入目录路径：")
source_dir = input("输入目录路径：")
output_file = input("输出文件路径：")
merge_files(source_dir, output_file)
