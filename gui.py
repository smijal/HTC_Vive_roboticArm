# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 23:29:17 2020

@authors: Lohith Muppala, Stefan Mijalkov, Ali Kazmi, Joshua Zychal
"""
import tkinter as tk
from tkinter import * 
import os
from PIL import Image,ImageTk
import triad_openvr
import time
import sys
import arm
import code_htc


############# GLOBAL VARIABLES, THIS MIGHT BE THE ONLY OPTION SINCE WE ARE USING GUI ############
#default system state, and mode (System OFF, Mode: Save)       
system_ON = False
modes = ['Teaching', 'Save', 'Replicating', 'Stop']
currMode = modes[1]
delay = 2

#Vive controller and tracker objects
v = triad_openvr.triad_openvr()
v.print_discovered_objects()
controller = triad_openvr.vr_tracked_device(v.vr,1,"Controller") #Instantiates the object

vive_position = v.devices["controller_1"].get_pose_euler()
print("Checking connection Controller-Base Station...")
while(not vive_position):
    vive_position = v.devices["controller_1"].get_pose_euler()
print("Connection ready !")
current_posX = vive_position[0]
current_posY = vive_position[1]
current_posZ = vive_position[2]
robot_position = [-310.0,303.0,170.0]
a = arm.StArm()
a.move_to(robot_position)
a.rotate_hand(30.0)

rest_time=0.2
tunning = 400
lim = tunning/20

#To create a new directory for saving the different coordinate files
current_directory = os.path.dirname(os.path.abspath(__file__))
filepath_document = os.path.join(current_directory , 'Documentation.pdf')
final_directory = os.path.join(current_directory, r'movement_paths')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

#TODO: Create a file that stores the previous num_paths (Example: 5 files are stored already, (file0 to file4), take the value stored and continue from there)
num_paths = len(os.listdir(final_directory))


#to open a new text file in the new directory
filename = os.path.join(final_directory, "coords" + str(num_paths) + ".txt")   
f = open(filename, "w+") #collects the co-ords in a text file.

#TODO: prompt the user to get alligned with the base station - NOT DONE !!!
#print_cords(v)

#interval frequency for coordinates to be scanned from Vive (Can be manipulated) 
if len(sys.argv) == 1:
    interval = 1/10
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False
print("interval is " + str(interval))
#-------------------------------------------------------------
# This function focuses on collecting the co-ordinates and sending the co-ordinates to the robot for visual input.
# The co-ordinates are more over stored in a text file so that we can call the Replication function later.
# Parameters:   v: Vive tracker | obj: controller keys inputs (might be redundant) | f: file to write to | interval (might be redundant if delay is not used)
#               a -> St Robotics Arm object  
#     
# Returns: f -> text file that has been updated
#-------------------------------------------------------------
def teaching_mode(v,obj,f, interval):
    #start = time.time()
    global current_posX,current_posY, current_posZ, robot_position, rest_time,tunning,lim
    vive_position = v.devices["controller_1"].get_pose_euler()
    if(vive_position==None):
        print("Vive can't read, make sure the controller and the base station can communicate...")
    else:
        displacementX = current_posX-vive_position[0]
        displacementY = current_posY-vive_position[1]
        displacementZ = current_posZ-vive_position[2]
        current_posX = vive_position[0]
        current_posY = vive_position[1]
        current_posZ = vive_position[2]
        if( (abs(displacementX*tunning) < lim) and (abs(displacementY*tunning)<lim) and (abs(displacementZ*tunning)<lim) ):
            print("Displacement too small")
        else:
            x = round(robot_position[0]+displacementX*(tunning+200), 1)
            y = round(robot_position[1]+displacementY*tunning,1)
            z = round(robot_position[2]+displacementZ*(tunning+100),1)

            if(x>-400.0 and x<300.0):
                robot_position[0] = x
            else:
                print("X-axis reaches its limit...")
            if(y>200.0 and y<400.0):
                robot_position[1] = y
            else:
                print("Y-axis reaches its limit...")
            if(z>0.0 and z<300.0):
                robot_position[2] = z
            else:
                print("Z-axis reaches its limit...")
            try:
                #a.smooth()
                a.move_to(robot_position)
                print(robot_position)
                txt=""
                for each in robot_position:
                    txt += "%.1f" % each
                    txt+=" "
                #txt+=str(robot_position[0]) + ", " + str(robot_position[1]) + ", " + str(robot_position[2]) + "\n"
                f.write(txt+'\n')
            except:
                print("Error in teaching function...")
        
    # sleep_time = interval-(time.time()-start) 
    # if sleep_time>0:
    #     time.sleep(sleep_time)

    # txt = ""
    # for each in v.devices["controller_1"].get_pose_euler():
    #     txt += "%.4f" % each
    #     txt += " "
    #     #x,y,z,yaw,pitch and roll 
    # f.write(txt+'\n') #writes into the file 
    # robot_input = obj.get_controller_inputs() #Calling the method for htc inputs

    time.sleep(rest_time)
    #     time.sleep(0.3)
    #     #st_robot.set_speed(1200)
        
    #     #: add a function for the gripper J6 to controll the gripper within fine grain
        
    #     # try:
    #     #     #Take the displacement into consideration (one variable to save the previous position, add the displacement to the prev position)
    #     #     pos_val = txt #collects the x,y,z
    #     #     st_robot.move_to(pos_val) #tells the robot to move to that x,y,z position
    #     #     time.sleep(0.4)
    #     #     st_robot.rotate_wrist(txt[5]) #rotates the wrist using the roll
    #     #     time.sleep(0.4)
    #     #     st_robot.rotate_hand(txt[4]) #rotates the hand using the pitch 
    #     #     time.sleep(0.4)
    #     # except:
    #     #     print('Error in the teaching function')
    #     #     #call stop function
    #     #     #exit
    return f

#st_robot is taken out
#------------------------------------------------
# The function's main purpose is to replicate the motions, previously learned
# Parameters: txt-> text file to read from, a -> St Robotics Arm object   
# Returns:  None
#------------------------------------------------
def replication_mode(txt):
    #TODO fist place it to the home position , then start replicating
    f = open(txt, 'r') 
    Lines = f.readlines()
    if(not Lines):
        print("File is empty, Nothing to replicate...")
        return None 
    count = 0
    for line in Lines:
        count += 1
        print(line) #Debug 
        # try:
        #     pos_val = line[0:3] #collects the x,y,z
        #     st_robot.move_to(pos_val) #tells the robot to move to that x,y,z position
        #     time.sleep(0.4)
        #     st_robot.rotate_wrist(line[5]) #rotates the wrist using the roll
        #     time.sleep(0.4)
        #     st_robot.rotate_hand(line[4]) #rotates the hand using the pitch 
        #     time.sleep(0.4)
        # except:
        #     print('Invalid co-ordinates at line: ' + str(count))
    f.close()

#---------------------------------------------------
# Purpose:  To switch between ON and OFF state
# Parameters: system_ON : Boolean (True if ON, False if OFF) | currMode : To print the current mode for reference
# Returns: toggled system_ON
#---------------------------------------------------   
def turn_ON_OFF(system_ON, currMode):
    if(not system_ON):
        system_ON=True
        print("\nSystem ON")
        print("Current mode: " + currMode)
    else:
        system_ON=False
    return system_ON   

#--------------------------------------------------
# Purpose:  To switch between modes
# Parameters:   modes -> list of possible modes, currMode -> current mode
# Returns: currMode changes to next mode
#--------------------------------------------------
def switchMode(modes, currMode):
    count=0
    for m in modes:
        if(currMode==m):
            currMode=modes[(count+1)%4]
            print(currMode)
            time.sleep(0.3)
            return currMode
        count+=1

#--------------------------------------------------
# Purpose: Main function, controlls the other function calls and operates the system
# Parameters: None
# Returns: None
#-------------------------------------------------- 
def main():
    #TODO: Instead of printing on the console, print on the GUI Window
    global robot_position, system_ON, modes, currMode, num_paths, v, controller, final_directory, interval, filename, f, filepath_document, delay
    if root.poll:
        root.after(delay,main)
    #Main controll, polling and wait for Vive button triggers to perform different functionalities
    if(interval):
        start=time.time()
        vive_buttons = controller.get_controller_inputs() #Calling the method for htc inputs  
        if(vive_buttons['menu_button']): 
            time.sleep(0.3)
            system_ON=turn_ON_OFF(system_ON, currMode)
        if(system_ON):
            if(vive_buttons['grip_button']):
                currMode=switchMode(modes,currMode)
            if(currMode=="Teaching"):
                if(vive_buttons['trackpad_pressed'] and vive_buttons['trackpad_y']<-0.8):
                    print("Fine grain")
                    #f.write("FINE GRAIN\n")
                    tunning=400
                    lim=tunning/200
                    delay=4
                elif(vive_buttons['trackpad_pressed'] and vive_buttons['trackpad_y']>0.8):
                    print("Coarse mode")
                    #f.write("COARSE MODE\n")
                    tunning=400
                    lim=tunning/100
                    delay=8
                if(f.closed):
                    filename = os.path.join(final_directory, "coords" + str(num_paths) + ".txt")   
                    f = open(filename, "w+") #Open new text file in write mode
                    num_paths+=1
                f=teaching_mode(v,controller,f, interval)
            if(currMode==modes[1] or currMode==modes[3]):
                if(not f.closed):
                    f.close()
            if(currMode=="Replicating"):
                replication_mode(filename)
                currMode=switchMode(modes,currMode)
        else:
            print("System is OFF, press the MENU button to turn it ON", end='\r')
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)

#################################### GUI FUNCTIONS AND CONTROLLS ###########################################
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
    print(arm.DEFAULT_DEV)

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

steam = Button(root,text = 'Run Program',bg = 'Green',command = main)
steam.place(x = 90, y = 320,width = 100, height = 50)

stop_btn = Button(root,text = 'STOP',bg = 'Red',command = stop)
stop_btn.place(x = 250, y = 320,width = 100, height = 50)

help_btn = Button(root,text = 'Help Guide',command = helper)
help_btn.place(x = 170, y = 390,width = 100, height = 50)

root.mainloop()

# if __name__ == "__main__":
#    main()