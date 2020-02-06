import _thread
import os
import time
from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk

from style_transformer import *

img = [0, 0, 0]
imgpath = ["", "", ""]
canvassize = 300
now = ''
open("./log.txt", 'w').close()

if os.path.exists("./result.jpg"):
	os.remove("./result.jpg")

root = Tk()
root.title('风格迁移')
root.geometry('1280x720')
root.resizable(width=False, height=False)


def log():
	global now
	while 1:
		time.sleep(0.1)
		if os.path.exists("./result.jpg"):
			showpicture(canvas3, 2, "./result.jpg")
		for line in open("./log.txt", 'r'):
			now = line
		if now != '':
			log_label.config(text=now)
		else:
			log_label.config(text='Ready.')


def openpicture(mycanvas, num):
	filename = askopenfilename()  # 获取文件全路径
	showpicture(mycanvas, num, filename)


def showpicture(mycanvas, num, filename):
	imgpath[num] = filename
	image = Image.open(filename)  # 打开图片放到image中
	w, h = image.size  # 获取image的长和宽
	mul = canvassize / max(w, h)  # 取最大的一边作为缩放的基准缩放倍数
	w1 = int(w * mul)
	h1 = int(h * mul)
	re_image = image.resize((w1, h1))
	img[num] = ImageTk.PhotoImage(re_image)  # 在canvas中展示图片
	mycanvas.create_image(canvassize / 2, canvassize / 2, anchor='center', image=img[num])  # 以中点为锚点


def transfer():
	if imgpath[0] == '' or imgpath[1] == '':
		return
	content_loss_test(answers['cl_out'], imgpath)
	gram_matrix_test(answers['gm_out'], imgpath)
	style_loss_test(answers['sl_out'], imgpath)
	tv_loss_test(answers['tv_out'], imgpath)
	params = {
		'content_image': imgpath[0],
		'style_image': imgpath[1],
		'image_size': 192,
		'style_size': 192,
		'content_layer': 3,
		'content_weight': 6e-2,
		'style_layers': [1, 4, 6, 7],
		'style_weights': [300000, 1000, 15, 3],
		'tv_weight': 2e-2
	}
	style_transfer(**params)
	showpicture(canvas3, 2, "./result.jpg")


fm1 = Frame(root)
fm1.pack(side=TOP, expand=False)

canvas1 = Canvas(fm1, width=canvassize, height=canvassize)  # 画布
canvas1.pack(side=LEFT, fill=NONE, padx=20, expand=False)

canvas2 = Canvas(fm1, width=canvassize, height=canvassize)  # 画布
canvas2.pack(side=LEFT, fill=NONE, padx=20, expand=False)

canvas3 = Canvas(root, width=canvassize, height=canvassize)  # 画布
canvas3.pack(side=TOP, fill=NONE, padx=20, expand=False)

log_label = Label(root, text='Ready.')
log_label.pack(side=TOP, fill=X)
_thread.start_new_thread(log, tuple())

fm2 = Frame(root)
fm2.pack(side=TOP, expand=False)

b1 = Button(fm2, text='选择内容图片', width=20, height=2, bg="skyblue", command=lambda: openpicture(canvas1, 0))
b1.pack(side=LEFT, expand=False, padx=30)

b2 = Button(fm2, text='开始风格迁移', width=20, height=2, bg="deepskyblue",
			command=lambda: _thread.start_new_thread(transfer, tuple()))  # 用新线程执行
b2.pack(side=LEFT, expand=False, padx=30)

b3 = Button(fm2, text='选择风格图片', width=20, height=2, bg="skyblue", command=lambda: openpicture(canvas2, 1))
b3.pack(side=LEFT, expand=False, padx=30)

root.mainloop()
