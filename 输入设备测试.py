import datetime

from pynput import keyboard, mouse


def on_press(key):
	try:
		print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')}：按下：{key.char}")
	except AttributeError:
		print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')}：按下：{key}")


def on_release(key):
	try:
		print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')}：抬起：{key.char}")
	except AttributeError:
		print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')}：抬起：{key}")


def on_click(x, y, button, pressed):
	if pressed:
		print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')}：鼠标 {button} 在 ({x}, {y}) 被按下")
	else:
		print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')}：鼠标 {button} 在 ({x}, {y}) 被释放")


# 创建键盘监听器
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# 创建鼠标监听器
mouse_listener = mouse.Listener(on_click=on_click)

# 启动监听器
keyboard_listener.start()
mouse_listener.start()

# 等待监听器结束
keyboard_listener.join()
mouse_listener.join()
