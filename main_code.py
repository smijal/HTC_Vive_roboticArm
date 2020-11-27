# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 23:29:17 2020

@authors: Lohith Muppala, Stefan Mijalkov, Ali Kazmi, Joshua Zychal
"""
##################################################### MODES EXPLANATION #####################################################################
## 1. Teaching -> constantly reads displacements from HTC Vive and sends it to the arm and writes them in a text file -> Arm moves         ##
## 2. Save -> stops the teaching mode -> saves the file                                                                                    ##     
## 3. Replicating -> reads from the saved file and sends positions to the robot to replicate                                               ## 
## 4. Stop -> Stops replication, ready for Teaching                                                                                        ##  
#############################################################################################################################################
####################################################### SYSTEM STATES #######################################################################
## 1. OFF STATE -> In this state HTC Vive does NOT react to any key presses, it is waits to be turned ON (Pressing the MENU button)        ##
## 2. ON STATE -> In this state HTC Vive reponds to key presses, functionalities of different keys are explained in the next section       ##
#############################################################################################################################################
########################################## HTC VIVE CONTROLLER KEYS FUNCTIONALITIES #########################################################
## 1. APPLICATION MENU KEY -> TURNS THE SYSTEM ON/OFF                                                                                      ##
## 2. GRIP KEY -> Changes between modes                                                                                                    ## 
## 3. TOUCHPAD DOWN_ARROW KEY -> change to fine grain                                                                                      ## 
## 4. HAIR TRIGGER -> switches between axes                                                                                                ## 
############################################################################################################################################# 

import tkinter as tk
from tkinter import * 
import os
from PIL import Image,ImageTk
import triad_openvr
import time
import sys
import arm
from pydub import AudioSegment
from pydub.playback import play

############# GLOBAL VARIABLES ############
#default system state, and mode (System OFF, Mode: Save)       
system_ON = False
modes = ['Teaching', 'Save', 'Replicating', 'Stop']
currMode = modes[3]
delay = 2
move_states = 0 #can go 0 1 2 -> 0 is move x , 1 is move y , 2 is move z
tunning = 400 #ideal tunning for now 400
lim = 10 #limit was 10
multiply_factor = 1000

#Vive controller and tracker objects
v = triad_openvr.triad_openvr()
v.print_discovered_objects()
controller = triad_openvr.vr_tracked_device(v.vr,1,"Controller") #Instantiates the object

# Waits for connection with Vive to be established
vive_position = v.devices["controller_1"].get_pose_euler()
print("Checking connection Controller-Base Station...")
while(not vive_position):
    vive_position = v.devices["controller_1"].get_pose_euler()
print("Connection ready !")

#memorizes the initial vive position
current_posX = vive_position[0]
current_posY = vive_position[1]
current_posZ = vive_position[2]
robot_position = [-310.0,303.0,170.0]

#This code has to be uncommented when the arm is connected
# it is commented for HTC Vive outputs testing 
#Initializes the ARM -> calibrate, send to home position, adjust speed
# a = arm.StArm()
# time.sleep(0.5)
# a.move_to(robot_position)
# time.sleep(0.5)
# a.rotate_hand(30.0)
# time.sleep(0.5)
# a.set_speed(8000)

#To create a new directory for saving the different coordinate files
current_directory = os.path.dirname(os.path.abspath(__file__))
filepath_document = os.path.join(current_directory , 'Documentation.pdf')
final_directory = os.path.join(current_directory, r'movement_paths')
audio_directory = os.path.join(current_directory, 'audio_files')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

# Create a file that stores the previous num_paths (Example: 5 files are stored already, (file0 to file4), take the value stored and continue from there)
num_paths = len(os.listdir(final_directory))

# Loads the audio files that will be used as voice guide
x_audio_path = os.path.join(audio_directory,"x_axis.wav")
y_audio_path = os.path.join(audio_directory,"y_axis.wav")
z_audio_path = os.path.join(audio_directory, "z_axis.wav")
x_audio = AudioSegment.from_file(x_audio_path)
y_audio = AudioSegment.from_file(y_audio_path)
z_audio = AudioSegment.from_file(z_audio_path)
audioFiles = [x_audio,y_audio,z_audio]

#to open a new text file in the new directory
filename = os.path.join(final_directory, "coords" + str(num_paths) + ".txt")   
f = open(filename, "w+") #collects the co-ords in a text file.

#interval frequency for coordinates to be scanned from Vive (Can be manipulated) 
if len(sys.argv) == 1:
    interval = 1/5 #1/5
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False
print("Vive reading interval is " + str(interval))
# a.get_speed()
# print("Speed used: " +str(speed))

#-------------------------------------------------------------
# This function focuses on collecting the co-ordinates and sending the co-ordinates to the robot for visual input.
# The co-ordinates are more over stored in a text file so that we can call the Replication function later.
# Parameters:   v: Vive tracker | obj: controller keys inputs (might be redundant) | f: file to write to | interval (might be redundant if delay is not used)
#               a -> St Robotics Arm object  
#     
# Returns: f -> text file that has been updated
#-------------------------------------------------------------
def teaching_mode(v):
	global current_posX,current_posY, current_posZ,tunning,lim,move_states,multiply_factor#,a
	vive_position = v.devices["controller_1"].get_pose_euler()
	if(vive_position==None):
		print("Vive can't read, make sure the controller and the base station can communicate...")
	else:
		displacementX = current_posX-vive_position[0]
		displacementX = round(displacementX,1)
		displacementY = current_posY-vive_position[1]
		displacementY = round(displacementY,1)
		displacementZ = current_posZ-vive_position[2]
		displacementZ = round(displacementZ,1)
		displacementZ*=-1
		current_posX = vive_position[0]
		current_posY = vive_position[1]
		current_posZ = vive_position[2]
		try:
			#a.smooth()
			if(move_states==0):
				if(abs(displacementX*tunning)<lim):
					print("Displacement in X too small")
				else:
					#print("MOVING X")
					dis = displacementX*multiply_factor
					print(dis)
					#a.rotate_waist(dis)
			elif(move_states==1):
				if(abs(displacementY*tunning)<lim):
					print("Displacement in Y too small")
				else:
					#print("MOVING Y")
					dis = displacementY*multiply_factor
					print(dis)
					#a.rotate_elbow(dis)
			elif(move_states==2):
				if(abs(displacementZ*tunning)<lim):
					print("Displacement in Z too small")
				else:
					#call rotation on the other joint
					#print("MOVING Z")
					dis = displacementZ*multiply_factor
					print(dis)
					#a.rotate_shoulder(dis)
		except:
			print("Error in teaching function...")



#------------------------------------------------
# The function's main purpose is to replicate the motions, previously learned
# Parameters: txt-> text file to read from, a -> St Robotics Arm object   
# Returns:  None
#------------------------------------------------
def replication_mode(txt):
	#global a,robot_position
	f = open("C:/Users/hazar/Documents/GitHub/smijal/HTC_Vive_roboticArm/movement_paths/coords21.txt", 'r') 
	Lines = f.readlines()
	if(not Lines):
		print("File is empty, Nothing to replicate...")
		return None
	#a.move_to(robot_position)
	time.sleep(0.5)
	for line in Lines:
		line = line.split(' ')
		x_s = line[0]
		y_s = line[1]
		z_s = line[2]
		x=float(x_s)
		y=float(y_s)
		z=float(z_s)
		position = [x,y,z]
		print(position)
		# try:
		# 	a.move_to(position)
		# 	time.sleep(0.4)
		# except:
		# 	print("Invalid position")
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
	global robot_position, system_ON, modes, currMode, num_paths, v, controller, final_directory, interval, filename, f, filepath_document, delay, move_states,multiply_factor,a
	#Main controll, polling and wait for Vive button triggers to perform different functionalities
	
	#while True:
	if(root.poll):
		root.after(2,main)
		start=time.time()
		vive_buttons = controller.get_controller_inputs() #Calling the method for htc inputs  
		if(vive_buttons['menu_button']): 
			time.sleep(0.3)
			system_ON=turn_ON_OFF(system_ON, currMode)
		if(system_ON):
			if(vive_buttons['grip_button']):
				time.sleep(0.2) #add this maybe
				currMode=switchMode(modes,currMode)
			if(currMode=="Teaching"):
				if(f.closed):
					filename = os.path.join(final_directory, "coords" + str(num_paths) + ".txt")   
					f = open(filename, "w+") #Open new text file in write mode
					print("Writting into file: coords"+str(num_paths) + ".txt")
					num_paths+=1
				if(vive_buttons['trackpad_pressed'] and vive_buttons['trackpad_y']<-0.8):
					print("Fine grain")
					#f.write("FINE GRAIN\n")
					multiply_factor=300
					#a.set_speed(3000)
				elif(vive_buttons['trackpad_pressed'] and vive_buttons['trackpad_y']>0.8):
					print("Coarse mode")
					#f.write("COARSE MODE\n")
					multiply_factor = 1000
					#a.set_speed(8000)
				if(vive_buttons['trigger']>0.8):
					move_states+=1
					move_states%=3
					#cur_location= a.where_position()
					cur_location = [100.1132, 200.2312321, 300.34343, 999.99, 999.99, 999.99]
					#print(cur_location)
					txt=""
					for each in cur_location:   #Once we get the position we need to 
						txt += "%.1f" % each
						txt+=" "
					f.write(txt+'\n')
					play(audioFiles[move_states])
				teaching_mode(v)

			if(currMode=="Save" or currMode=="Stop"):
				if(not f.closed):
					f.close()
			if(currMode=="Replicating"):
				#a.move_to(robot_position)
				replication_mode(filename)
				currMode=switchMode(modes,currMode)
		else:
			print("System is OFF, press the MENU button to turn it ON", end='\r')
		sleep_time = interval-(time.time()-start)
		if sleep_time>0:
			time.sleep(sleep_time)

################################### GUI FUNCTIONS AND CONTROLLS ###########################################
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
# if __name__ == '__main__':
# 	main()