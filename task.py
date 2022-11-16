import cv2
from tkinter import Label, Tk, Button,ttk
from PIL import ImageTk,Image
import os
import numpy as np
import multiprocessing as mp


win = Tk()
win.geometry("600x600")

filters ="RGB","GRAY","HSV","FHSV","HLS"
col_box = ttk.Combobox(win,values = filters)
col_box.current(0)
col_box.place(x=80,y=500,width = 100)
def change_color_filter(img):
    if col_box.get() =="RGB":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if col_box.get() =="GRAY":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if col_box.get() =="HSV":
        img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    if col_box.get() =="FHSV":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    if col_box.get() =="HLS":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    return img

filters1 = "SHARP", "BLUR"
filt_box = ttk.Combobox(win,values=filters1)
filt_box.current(0)
filt_box.place(x=430,y=500,width=100)
def change_image_filter(img):
    if filt_box.get() =="SHARP":
        kernel_sharpening = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])
        img = cv2.filter2D(img, -1, kernel_sharpening)
    if filt_box.get() =="BLUR":
        #kernel_3x3 = np.ones((3, 3), np.float32) / 12
        img = cv2.blur(img,(10,10))
    return img


path = os.getcwd()
myList = os.listdir("D:\Python\DataAnalysisZadanie85744")
list2 = []
for _, imgs in enumerate(myList):
    img =  imgs.split(".")
    if img[1] =="jpg" or img[1] =="png":
        list2.append(imgs)
# print(len(list2))

# print(myList)
def to_display(img, label, x, y, w, h):
    image = Image.fromarray(img)
    image = image.resize((w, h), Image.ANTIALIAS)
    pic = ImageTk.PhotoImage(image)
    label.configure(image=pic)
    label.image = pic
    label.place(x=x, y=y)

def switch(i):
    label = Label(win, bg="black")
    img = cv2.imread(list2[i])
    img = change_color_filter(img)
    img = change_image_filter(img)
    to_display(img,label,150,20,300,400)

count = 0
#next img
def counup():
    global count
    count +=1
    if count > len(list2)-1:
        count = 0
    switch(count)

# previous img
def coundown():
    global count
    count -=1
    if count < 0:
        count = len(list2)-1
    switch(count)
#     win.after(700,coundown)
# coundown()

#right = Button(win,text="▶",bg="gray",fg="white",command=counup).place(x=330,y=500,width = 40)
apply = Button(win,text="Apply",bg="green",fg="black",command=coundown).place(x=250,y=500,width = 80)

win.mainloop()
