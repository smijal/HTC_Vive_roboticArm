import tkinter as tk
import os
from tkinter import * 
from PIL import Image,ImageTk
import subprocess as sp
import sys
sys.path.insert(1,os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_scripts'))
import arm

class GUI():

    def __init__(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.filepath_document = os.path.join(self.current_directory , 'gui_files/documentation.pdf' )
        main_code = os.path.join(self.current_directory, 'main_scripts')
        main_code = os.path.join(main_code, 'main_code.py')
        self.command = ['python',str(main_code)]
        self.process_running = False
        self.root = tk.Tk() # instantiating the window
        self.entry1 = StringVar() #assigning a variable for the text entry
        self.title = Label(self.root,text = 'Motion Controlled Robot',bg= 'black', fg = 'White',font = ('Verdana',27))
        im_path = os.path.join(self.current_directory, 'gui_files')
        im_path = os.path.join(im_path,'pic.png')
        im = Image.open(im_path)
        im = im.resize((180, 180),Image.ANTIALIAS)
        self.ph = ImageTk.PhotoImage(im)
        self.image = Label(self.root, image=self.ph, highlightthickness = 0, bd = 0)
        self.coms = Label(self.root,bg ='black', fg = 'white', text = 'COM Port: ',font = ('Verdana',15))
        self.coms_button = Button(self.root,text = 'OK',width = 9, height = 1,command = self.comport)
        self.steam = Button(self.root,text = 'Run Program',bg = 'Green',command = self.launchMain)
        self.stop_btn = Button(self.root,text = 'STOP',bg = 'Red',command = self.stop)
        self.help_btn = Button(self.root,text = 'Help Guide',command = self.helper)

    def setup(self):
        self.root.poll = True #toggle variable
        self.root.title('Motion Controll Robot GUI') #naming the window
        self.root.configure(background='black')
        self.root.minsize(width=100, height=100)
        self.root.geometry('450x500+0+0') #setting the size of the window
        self.root.resizable(False,False)
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.title.pack(anchor = CENTER)
        #bringing the image.
        self.image.pack(side = 'top')
        self.coms.pack(anchor = CENTER)
        Entry(self.root,width = 30,textvariable = self.entry1,justify = 'center').pack(anchor = CENTER) 
        self.coms_button.pack(anchor = CENTER,padx = 2, pady = 3)
        self.steam.place(x = 90, y = 320,width = 100, height = 50)
        self.stop_btn.place(x = 250, y = 320,width = 100, height = 50)
        self.help_btn.place(x = 170, y = 390,width = 100, height = 50)
    
    def disable_event(self):
        print("Please use the STOP button to exit!")
        pass

    def stop(self):
        if(self.process_running):   
            sp.Popen.terminate(self.process)
        print("Exiting the program!")
        self.root.poll = False
        self.root.destroy() #closes the window
        
    #launches the Helper guide 
    def helper(self):
        print('Help guide launching...')
        os.startfile(self.filepath_document)

    #COM port setter 
    def comport(self):
        if(self.process_running):
            print("Process is running, cannot change Serial connection.")
            return None
        self.entry1
        content = self.entry1.get()
        if(content):
            arm.setPort(content)
        print('Attempted serial connection to ' + arm.getPort())

    def launchMain(self):
        if(not self.process_running):
            self.process = sp.Popen(self.command)
            self.process_running = True

    def launchGUI(self):
        self.setup()
        self.root.mainloop()

def main():
    gui = GUI()
    gui.launchGUI()

if __name__ == '__main__':
	main()