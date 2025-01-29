import threading

import requests
import urllib3

import lib
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用警告
import random


class Data:
	def __init__(self):
		self.url = [
			# OneDrive国际版
			requests.get(
				"http://8.131.94.236:5244/d/%E9%BB%84%E9%87%91/%E7%94%B5%E5%BD%B1/1/%E8%AE%A9%E5%AD%90%E5%BC%B9%E9%A3%9E.mp4",
				stream=True, allow_redirects=True, timeout=10, verify=False).url,
			# 咪咕快游[高速]
			# "https://freeserver.migufun.com/resource/beta/apk/20240412135425/MiguPlay-V3.79.1.1_miguzsj.apk",
			# 咪咕音乐
			"https://wsdkdl.migu.cn:8443/b486900f41fc411187240dcb45fdbc8d/1716482115184/netsdk_b.js",
			# 咪咕视频
			"https://img.cmvideo.cn/publish/noms/2023/12/06/1O4SHFIFR36BD.gif",
			# 咪咕快游2
			# "https://h5cdn.migufun.com/middleh5/_nuxt/643447d.js",
			# 和彩云
			"https://img.mcloud.139.com/material_prod/material_media/20221128/1669626861087.png",
			# 联通电视
			##"https://listen.10155.com/listener/womusic-bucket/90115000/mv_vod/volte_mp4/20200805/1290953968000712705.mp4",
			# 电信测速
			# "https://vipspeedtest8.wuhan.net.cn:8080/download?size=1073741824",
			# Cachefly
			##"https://web1.cachefly.net/speedtest/downloading",
			# Cloudflare
			"https://speed.cloudflare.com/__down?bytes=104857600",
			# jsDelivr
			# "https://cdn.jsdelivr.net/gh/ljxi/CDN-IP-test@main/dump",
			# Cloudflare Workers
			# "https://gh.con.sh/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z",
			# Steam Akamai
			##"https://cdn.akamai.steamstatic.com/steam/apps/1063730/extras/NW_Sword_Sorcery_2.gif",
			# Steam Cloudflare
			##"https://cdn.cloudflare.steamstatic.com/steam/apps/1063730/extras/NW_Sword_Sorcery_2.gif",
			# Microsoft Akamai
			##"https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RW16Ptm",
		]  # 文件下载的URL
		lib.pr("url获取完成")
		self.total_downloaded = lib.load("total_downloaded")
		if not self.total_downloaded:  # 未保存数据
			self.total_downloaded = 0  # 已下载总量设为0
		else:
			self.total_downloaded = int(self.total_downloaded)
			print(f"\r发现历史记录，之前消耗{format_size(self.total_downloaded)}")  # 覆盖上一条消息
		self.last_downloaded = 0  # 上一次统计时的已下载量
		self.last_time = time.time()  # 上一次统计的时间
		self.running = True  # 控制线程运行状态的标志
		self.threads = []  # 存放所有线程对象的列表
		self.session = requests.Session()  # 使用Session对象复用连接
		# self.headers = {"User-Agent": UserAgent().random}  # 随机生成的请求头
		self.headers = {}


def download_file(_data):
	_data.threads.append(threading.current_thread())  # 将当前线程对象加入Data类的threads列表
	while _data.running:
		try:
			response = _data.session.get(random.choice(_data.url),
			                             headers=_data.headers,  # 设定请求头
			                             stream=True,  # 流式传输
			                             timeout=10,  # 设置超时时间
			                             verify=False  # 不验证证书
			                             )
			for chunk in response.iter_content(chunk_size=8192):
				if not _data.running:
					break
				_data.total_downloaded += len(chunk)
				# 内丢弃获取到的内容
				with open(lib.get_null_device(), "ab") as f:
					f.write(chunk)
		except Exception as e:
			lib.log(lib.Error(e))  # 出错重试


def format_size(size):
	units = ["B", "KB", "MB", "GB", "TB"]
	index = 0
	while size >= 1024 and index < len(units) - 1:
		size /= 1024
		index += 1
	return f"{size:.5f}{units[index]}"


def format_speed(_speed):
	units = ["B/s", "KB/s", "MB/s", "GB/s", "TB/s"]
	index = 0
	while _speed >= 1024 and index < len(units) - 1:
		_speed /= 1024
		index += 1
	return f"{_speed:.5f}{units[index]}"


if __name__ == "__main__":
	num_threads = 64  # 线程数
	data = Data()
	threads = []
	for _ in range(num_threads):
		thread = threading.Thread(target=download_file, args=(data,))
		thread.start()
		threads.append(thread)
	try:
		while data.running:
			current_time = time.time()
			elapsed_time = current_time - data.last_time
			if elapsed_time >= 1:  # 至少等待1s
				downloaded = data.total_downloaded - data.last_downloaded
				speed = downloaded / elapsed_time
				data.last_downloaded = data.total_downloaded
				data.last_time = current_time
				lib.pr(f"已消耗{format_size(data.total_downloaded)}实时速度{format_speed(speed)}  ")
	except KeyboardInterrupt:
		data.running = False
		print("\n正在保存数据")
		lib.save("total_downloaded", data.total_downloaded)
		print("数据保存完成")
		print("正在等待下载线程退出")
		for thread in data.threads:
			thread.join()
		print("所有下载线程已退出")
