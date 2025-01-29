import os
import random
import sys
import threading

from pygame import mixer

import lib
import time


class Data:
	def __init__(self):
		self.current_song_index: int = 0  # 当前播放歌曲的索引
		self.sort_method: str = "name"  # 播放列表排序方式：name（按名称）、addtime（按添加时间）
		self.playlist: list = []  # 播放列表
		self.player = None  # 音乐播放器对象
		self.play_mode: str = "random"  # 播放模式：sequential（顺序播放）、random（随机播放）
		self.input_thread = None  # 输入命令的线程对象
		self.running: bool = True  # 播放器运行状态：True（运行中）、False（停止）
		self.tick: float = 0.01  # 每次检测间隔时间，单位为秒
		self.help_text: str = """命令列表与功能如下：
line <歌曲序号>：显示当前正在播放的歌曲
time <分秒>：跳转到指定时间
sort <name/addtime>：修改播放列表排序方式
mode <sequential/random>：设置播放模式
w：上一首
s：下一首
exit：退出播放器
pause：暂停
resume：播放
<空格>：暂停/播放
volume <1-100的数>：调节音量至<1-100的数>%
不输入参数则为查看设定值
使用 "<命令> /?" 可以获取具体命令的帮助信息（<空格>的暂停播放没这功能）"""
		self.command_help: dict = {
			"line": "line <歌曲序号>：显示当前正在播放的歌曲",
			"time": "time <分秒>：跳转到指定时间，格式如 2008 或 20:08",
			"sort": "sort <name/addtime>：name按名称排序，addtime按添加时间排序",
			"mode": "mode <sequential/random>：sequential顺序播放random随机播放",
			"w": "上一首",
			"s": "下一首",
			"exit": "退出播放器",
			"pause": "暂停",
			"resume": "播放",
			" ": "输入空格，然后按下回车，就可以暂停和播放了。。。",
			"volume": "后面带个1-100的数即可",
		}
		self.path: str = sys.argv[0] + ".data"  # 查找歌曲文件的路径
		self.is_paused: bool = False  # 是否暂停播放
		self.volume: float = 0.5  # 默认音量为50%
	
	def get_current_song_name(self, _current_song_index: int) -> str:  # 正在播放的歌曲名
		filepath = self.playlist[_current_song_index]
		# 因为检索文件时及时是Windows也会用/所以如果没有/就说明在同一文件夹下，有就按/分就行
		filename = filepath.split("/")[-1]
		return filename


def get_music_files(_data: Data):
	supported_formats = (".wav", ".flac", ".mp3")
	supported_files = []
	for f in os.listdir(_data.path):
		if f.endswith(supported_formats):
			supported_files.append(f"{_data.path}/{f}")
	
	if data.sort_method == "name":
		# 按照文件名排序
		_data.playlist = sorted(supported_files)
	elif data.sort_method == "addtime":
		# 按照文件的创建时间排序
		_data.playlist = sorted(supported_files, key=lambda x: os.path.getctime(x))
	
	print("播放列表:")
	for i in range(len(_data.playlist)):
		print(f"{i}. {_data.get_current_song_name(i)}")


def play_next_song(_data: Data):
	if _data.play_mode == "sequential":
		_data.current_song_index = (_data.current_song_index + 1) % len(_data.playlist)
	elif _data.play_mode == "random":
		_data.current_song_index = random.randint(0, len(_data.playlist) - 1)
	_data.player.load(_data.playlist[_data.current_song_index])
	_data.player.play()


def input_thread(_data: Data):
	while _data.running:
		try:
			command = input("输入命令: ")
			parts = command.split(" ")
			cmd = parts[0]
			if command == " ":  # cmd是经过空格分割的，会顶掉这个空格
				if _data.is_paused:
					_data.player.unpause()
					_data.is_paused = False
					print("已继续播放")
				else:
					_data.player.pause()
					_data.is_paused = True
					print("已暂停播放")
			else:
				match cmd:
					case "line":
						match len(parts):
							case 1:
								print(f"当前播放的歌曲：{_data.get_current_song_name(_data.current_song_index)}")
							case _:
								song_index = int(parts[1]) - 1
								if 0 <= song_index < len(_data.playlist):
									_data.current_song_index = song_index
									_data.player.load(_data.playlist[song_index])
									_data.player.play()
								else:
									print("无效的歌曲序号。")
					
					case "time":
						match len(parts):
							case 1:
								print(f"当前时间：{time.strftime('%H:%M:%S')}")
							case _:
								time_str = parts[1].replace(":", "")
								minutes, seconds = divmod(int(time_str), 100)
								_data.player.set_pos(minutes * 60 + seconds)
					
					case "sort":
						match len(parts):
							case 1:
								print(f"当前排序方式：{_data.sort_method}")
							case _:
								sort_method = parts[1]
								if sort_method in ["name", "addtime"]:
									_data.sort_method = sort_method
									get_music_files(_data)
								else:
									print("无效的排序方式。")
					
					case "mode":
						match len(parts):
							case 1:
								print(f"当前播放模式：{_data.play_mode}")
							case _:
								play_mode = parts[1]
								if play_mode in ["sequential", "random"]:
									_data.play_mode = play_mode
									print(f"播放模式已更改为：{play_mode}")
								else:
									print("无效的播放模式。可用模式：sequential, random")
					
					case "w":
						_data.current_song_index = (_data.current_song_index - 1) % len(_data.playlist)
						_data.player.load(_data.playlist[_data.current_song_index])
						_data.player.play()
					
					case "s":
						play_next_song(_data)
					
					case "exit":
						_data.running = False
						print("播放器即将退出...")
					
					case "pause":
						if not _data.is_paused:
							_data.player.pause()
							_data.is_paused = True
							print("播放已暂停")
						else:
							print("播放已经暂停，无需重复暂停")
					
					case "resume":
						if _data.is_paused:
							_data.player.unpause()
							_data.is_paused = False
							print("播放已恢复")
						else:
							print("播放未暂停，无需恢复")
					
					case "volume":
						volume = float(parts[1]) / 100
						if 0.0 <= volume <= 1.0:
							_data.volume = volume
							_data.player.set_volume(volume)
							print(f"音量已设置为{parts[1]}%")
						else:
							print("音量∉(0,100)（音量不在0-100之间）")
					
					case _ if cmd.endswith("/?"):
						command_name = cmd[:-2].strip()
						if command_name in _data.command_help:
							print(_data.command_help[command_name])
						else:
							print("命令不存在")
							print(_data.help_text)
					
					case _:
						print("命令不存在")
						print(_data.help_text)
		except Exception as e:  # 防止输入错误全寄
			print(lib.Error(e))


if __name__ == "__main__":
	data: Data = Data()
	data.player = mixer.music
	mixer.init()
	get_music_files(data)
	data.player.load(data.playlist[data.current_song_index])
	data.player.play()
	
	data.input_thread = threading.Thread(target=input_thread, args=(data,), name="InputHandler")
	data.input_thread.start()
	
	# 主线程循环，检查音乐是否播放完毕
	while data.running:
		if (not data.player.get_busy()) and (not data.is_paused):
			play_next_song(data)
		time.sleep(data.tick)  # 每tick检测一次
