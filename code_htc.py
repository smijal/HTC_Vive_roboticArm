# -*- coding: utf-8 -*-
# """
# Created on Fri Oct  2 21:31:04 2020

# @author: Lohith Muppala
# """
import triad_openvr
import time
import sys
import arm
import os

current_posX = 0.0
robot_position = [-310.0,303.3,169.2]

#st_robot is taken out
def teaching_mode(v,obj,f, interval,a):
    # """
    # This function focuses on collecting the co-ordinates and sending the co-ordinates to the robot for visual input.
    # The co-ordinates are more over stored in a text file so that we can call the Replication function later.

    # Parameters
    # ----------
    # st_robot : object
    #     This object instantiates the robot commands in Roboforth.
    # v : OpenVR triad object
    #     This object instantiates.

    # Returns
    # -------
    # f : text file
    #     Textfile that collects all the co-ordinates collected within the function. 
    # """
    #initial_pos = [-310.0,303.3,169.2,57.4,-61.6]
    #when we enable the teaching mode, we command the robot to move to the default position. 
    #st_robot.move_to(initial_pos) 
    #time.sleep(0.4)
    #st_robot.rotate_wrist(initial_pos[4]) #rotates the wrist using the roll
    #time.sleep(0.4)
    #st_robot.rotate_hand(initial_pos[3]) #rotates the hand using the pitch 
    #time.sleep(0.4)
    #start = time.time()
    global current_posX
    global robot_position
    vive_position = v.devices["controller_1"].get_pose_euler()
    if(vive_position==None):
        print("NONE")
    else:
        displacementX = current_posX-vive_position[0]
        current_posX = vive_position[0]
        #print(displacementX)
        if(abs(displacementX*250) < 20):
            print("Displacement too small")
        else:
            robot_position[0] = robot_position[0]+displacementX*250
            robot_position[0] = round(robot_position[0],1)
            a.move_to(robot_position)
            print(robot_position)
        time.sleep(0.2)
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
    # if(robot_input['trackpad_pressed'] and robot_input['trackpad_y']<-0.8):
    #     print("Fine grain")
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
    # print("\r" + txt, end="")
       
    return f

#st_robot is taken out
def replication_mode(txt):
    # """
    # The function's main purpose is to replicate the motions 

    # Parameters
    # ----------
    # txt : text file
    #     Text file with all the collected co-ordinates.
    # st_robot : St Robotic object
    #     The object let us send commands to the robot using ROBOFORTH.

    # Returns
    # -------
    # None.
    # However, replicates the saved co-ordinates during replication mode.
    # """
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
        
def turn_ON_OFF(system_ON, currMode):
    if(not system_ON):
        system_ON=True
        print("\nSystem ON")
        print("Current mode: " + currMode)
    else:
        system_ON=False
    return system_ON   

def switchMode(modes, currMode):
    count=0
    for m in modes:
        if(currMode==m):
            currMode=modes[(count+1)%4]
            print(currMode)
            time.sleep(0.3)
            return currMode
        count+=1

def main():
    global robot_position
    a = arm.StArm()
    a.move_to(robot_position)
    a.rotate_hand(30.0)

    #Variables 
    system_ON = False
    modes = ['Teaching', 'Save', 'Replicating', 'Stop']
    currMode = modes[1]
    num_paths = 0 #useful for creating more than one file (ex: file0, file1 ...)
    v = triad_openvr.triad_openvr()
    v.print_discovered_objects()

    #imports the st.py as command and then instansiates the arm.
    #st_robot = arm.StArm()
    
    controller = triad_openvr.vr_tracked_device(v.vr,1,"Controller") #Instantiates the object
    
    #To create a new directory for saving the different coordinate files
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'movement_paths')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    #to open new a text file in the new directory
    filename = os.path.join(final_directory, "coords" + str(num_paths) + ".txt")   
    f = open(filename, "w+") #collects the co-ords in a text file.

    #prompt the user to get alligned with the base station -DONE??
    print_cords(v) 
    #have a function to display the co-ordinates so that the user can align to the co-ords. 
    #TODO: How do I know if the switch is on or off like the toggle?
    #TODO: Create specific scneraios for the robot using different buttons: 1) Gripping 2) fine grain.
    if len(sys.argv) == 1:
        interval = 1/250
    elif len(sys.argv) == 2:
        interval = 1/float(sys.argv[1])
    else:
        print("Invalid number of arguments")
        interval = False
    if(interval):
        while(True):
            vive_buttons = controller.get_controller_inputs() #Calling the method for htc inputs  
            if(vive_buttons['menu_button']): 
                time.sleep(0.4)
                system_ON=turn_ON_OFF(system_ON, currMode)
            if(system_ON):
                if(vive_buttons['grip_button']):
                    currMode=switchMode(modes,currMode)
                if(currMode=="Teaching"):
                    if(f.closed):
                        filename = os.path.join(final_directory, "coords" + str(num_paths) + ".txt")   
                        f = open(filename, "w+") #collects the co-ords in a text file.
                        num_paths+=1
                    f=teaching_mode(v,controller,f, interval,a)
                if(currMode==modes[1] or currMode==modes[3]):
                    if(not f.closed):
                        f.close() 
                if(currMode=="Replicating"):
                    replication_mode(filename)
                    currMode=switchMode(modes,currMode)

            else:
                print("System is OFF, press the MENU button to turn it ON", end='\r')

if __name__ == "__main__":
   main()

    