# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 10:15:51 2020

@author: mlohi
"""
#

import tkinter as tk
from tkinter import * 
import os
from PIL import Image,ImageTk
import triad_openvr

import arm
import code_htc

current_directory = os.path.dirname(os.path.abspath(__file__))
filepath_document = os.path.join(current_directory , 'Documentation.pdf')


#stop function to stop the GUI
def stop():
    root.poll = False
    print("Exiting the program!")
    root.destroy() #closes the window
        
#launches the Helper guide 
def helper():
    print('Help guide launching...')
    os.startfile(filepath_document)

#COM port setter
#TODO: Check in person if this actually works
# TODO: Write code that actually checks if connection is established 
def comport():
    global entry1
    content = entry1.get()
    if(content):
        arm.DEFAULT_DEV = "COM" + str(content)
    print('Connected to COM Port: ' + str(content))


root = tk.Tk() # instantiating the window
entry1 = StringVar() #assigning a variable for the text entry

root.poll = True #toggle variable

root.title('Motion Controll Robot GUI') #naming the window
root.configure(background='black')
root.minsize(width=100, height=100)
root.geometry('450x500+0+0') #setting the size of the window 
title = Label(root,text = 'Motion Controlled Robot',bg= 'black', fg = 'White',font = ('Verdana',27))
title.pack(anchor = CENTER)


#bringing the image. 
print(current_directory)
im_path = os.path.join(current_directory, 'pic.png')
im = Image.open(im_path)
im = im.resize((180, 180),Image.ANTIALIAS)
ph = ImageTk.PhotoImage(im)
image = Label(root, image=ph, highlightthickness = 0, bd = 0)
image.pack(side = 'top')


coms = Label(root,bg ='black', fg = 'white', text = 'COM Port: ',font = ('Verdana',15))
coms.pack(anchor = CENTER)
Entry(root,width = 30,textvariable = entry1,justify = 'center').pack(anchor = CENTER)

coms_button = Button(root,text = 'OK',width = 9, height = 1,command = comport)
coms_button.pack(anchor = CENTER,padx = 2, pady = 3)

steam = Button(root,text = 'Run Program',bg = 'Green',command = code_htc.main)
steam.place(x = 90, y = 320,width = 100, height = 50)

stop_btn = Button(root,text = 'STOP',bg = 'Red',command = stop)
stop_btn.place(x = 250, y = 320,width = 100, height = 50)

help_btn = Button(root,text = 'Help Guide',command = helper)
help_btn.place(x = 170, y = 390,width = 100, height = 50)

root.mainloop()

# if __name__ == "__main__":
#    main()