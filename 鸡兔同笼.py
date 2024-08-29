# -*- coding: UTF-8 -*-
# 用了“砍足法”
head=35
head=359
leg=94
if leg%2==1:
	raise ValueError("腿数错误：不可能为单数")
leg/=2# 单脚鸡，双脚兔
rabbit=leg-head
if int(rabbit)!=abs(rabbit):
	raise UserWarning("数值不正确警告：兔的数量不正确，很可能是头的数量不正确导致的计算错误")
chicken=head-rabbit
ret="答：兔有"+str(int(rabbit))+"只，鸡有"+str(int(chicken))+"只。"
print(ret)
# 简介版：print({"兔":leg/2-head,"鸡":head-(leg/2-head)})# 需保证用户输入值全部正确！！！