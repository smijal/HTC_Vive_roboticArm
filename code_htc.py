# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 21:31:04 2020

@author: Lohith Muppala
"""
import triad_openvr
import time
import sys
import command
v = triad_openvr.triad_openvr()
v.print_discovered_objects()

#imports the st.py as command and then instansiates the arm.
arm = command.StArm()

def get_cords():
    f = open("coords.txt", "a") #collects the co-ords in a text file. 
    if len(sys.argv) == 1:
        interval = 1/250
    elif len(sys.argv) == 2:
        interval = 1/float(sys.argv[1])
    else:
        print("Invalid number of arguments")
        interval = False
        
    if interval:
        while(True):
            start = time.time()
            txt = ""
            for each in v.devices["controller_1"].get_pose_euler():
                txt += "%.4f" % each
                txt += " "
                #x,y,z,yaw,pitch and roll 
                f.write(txt) #writes into the file 
                #TODO: add the move to from the st.py file
                pos_val = txt[0:3] #collects the x,y,z
                arm.move_to(pos_val) #tells the robot to move to that x,y,z position
                arm.rotate_wrist(5) #rotates the wrist using the roll
                arm.rotate_hand(4) #rotates the hand using the pitch 
            print("\r" + txt, end="")
            sleep_time = interval-(time.time()-start)
            if sleep_time>0:
                time.sleep(sleep_time)
        f.close()        
    return f

#TODO: 1) We have to collect the inputs of the HTC vive
#TODO: 2) We have to create the replication function
#TODO 3) We have to create the fine_grain movement.  
    
    