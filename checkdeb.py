# 执行dpkg-query命令，获取包及其大小
def get_packages():
	cmd = "dpkg-query -W --showformat='${Installed-Size}KB\t${Package}\n'"
	# cmd = "dpkg-query -W --showformat='${Installed-Size;7}\t${Package}\n' | sort -r -t' '"
	import subprocess
	result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
	return result.stdout

# 解析命令输出，提取包名和大小
def parse_packages(output):
	packages = []
	import re
	for line in output.split('\n'):
		match = re.match(r'(\d+)KB\t(.+)', line)
		if match:
			size, pkg_name = match.groups()
			packages.append({"pkgname": pkg_name, "size": int(size)})
	return packages

# 对包列表按大小进行降序排序
def sort_packages(packages):
	return sorted(packages, key=lambda x: x["size"], reverse=True)

def format_size(size):
	# 定义单位
	units = ["KB", "MB", "GB", "TB", "PB"]
	# 转换为1024倍的单位
	for unit in units:
		if size < 1024:
			return f"{size} {unit}"
		size /= 1024
	return f"{size} {units[-1]}"  # 超过最大单位了，返回最大单位

def print_packages(packages):
	# 计算最长的包名长度
	max_length = max(len(pkg['pkgname']) for pkg in packages)
	
	# 打印每个包，自动对齐并转换大小单位
	for pkg in packages:
		formatted_size = format_size(pkg['size']) #格式化单位
		# 使用空格填充到最长包名的长度
		# print(f"{pkg['pkgname'].ljust(max_length)} {pkg['size']}KB")
		print(f"{pkg['pkgname'].ljust(max_length)} {formatted_size}")

if __name__ == "__main__":
	output = get_packages() #获取每个包的大小
	packages = parse_packages(output) #提取包名和大小放入列表
	sorted_packages = sort_packages(packages) #对列表进行排序
	print_packages(sorted_packages) #格式化并输出
