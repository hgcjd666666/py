a = int(input("a："))
b = int(input("b："))
c = int(input("c："))
# 获取abc的值

delt = b ** 2 - 4 * a * c
# 求根的判别式

if delt >= 0:
	print(f"delt为{delt}")
else:
	print("delt＜0，方程无实数根")
	exit()

print(f"({-b}±{delt}**0.5)/{2 * a}")
x1 = (-b + float(f"{-b + delt:.5f**0.5}")) / (2 * a)
x2 = (-b - float(f"{-b - delt:.5f**0.5}")) / (2 * a)
print(f"x1：{x1}")
print(f"x2：{x2}")

# input("按任意键退出...")
