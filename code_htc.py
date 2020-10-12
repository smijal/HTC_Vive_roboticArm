# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 21:31:04 2020

@author: Lohith Muppala
"""
import triad_openvr
import time
import sys
import arm



def teaching_mode(st_robot,v,obj):
    """
    This function focuses on collecting the co-ordinates and sending the co-ordinates to the robot for visual input.
    The co-ordinates are more over stored in a text file so that we can call the Replication function later.

    Parameters
    ----------
    st_robot : object
        This object instantiates the robot commands in Roboforth.
    v : OpenVR triad object
        This object instantiates.

    Returns
    -------
    f : text file
        Textfile that collects all the co-ordinates collected within the function. 
    """
    initial_pos = [-310.0,303.3,169.2,57.4,-61.6]
    #when we enable the teaching mode, we command the robot to move to the default position. 
    st_robot.move_to(initial_pos) 
    time.sleep(0.4)
    st_robot.rotate_wrist(initial_pos[4]) #rotates the wrist using the roll
    time.sleep(0.4)
    st_robot.rotate_hand(initial_pos[3]) #rotates the hand using the pitch 
    time.sleep(0.4)
    
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
                robot_input = obj.get_controller_inputs() #Calling the method for htc inputs
                if(robot_input['trigger_button']):
                    #this could be our fine grain mode. 
                   st_robot.set_speed(1200)
        
                #TODO: add a function for the gripper J6 to controll the gripper within fine grain
                
                try:
                    #Take the displacement into consideration (one variable to save the previous position, add the displacement to the prev position)
                    pos_val = txt #collects the x,y,z
                    st_robot.move_to(pos_val) #tells the robot to move to that x,y,z position
                    time.sleep(0.4)
                    st_robot.rotate_wrist(txt[5]) #rotates the wrist using the roll
                    time.sleep(0.4)
                    st_robot.rotate_hand(txt[4]) #rotates the hand using the pitch 
                    time.sleep(0.4)
                except:
                    print('Error in the teaching function')
                    #call stop function
                    #exit
            print("\r" + txt, end="")
            sleep_time = interval-(time.time()-start)
            if sleep_time>0:
                time.sleep(sleep_time)
        f.close()        
    return f


def replication_mode(txt,st_robot):
    """
    The function's main purpose is to replicate the motions 

    Parameters
    ----------
    txt : text file
        Text file with all the collected co-ordinates.
    st_robot : St Robotic object
        The object let us send commands to the robot using ROBOFORTH.

    Returns
    -------
    None.
    However, replicates the saved co-ordinates during replication mode.
    """
    file = open(txt, 'r') 
    Lines = file.readlines() 
    count = 0
    for line in Lines:
        count += 1
        print(line) #Debug 
        try:
            
            pos_val = line[0:3] #collects the x,y,z
            st_robot.move_to(pos_val) #tells the robot to move to that x,y,z position
            time.sleep(0.4)
            st_robot.rotate_wrist(line[5]) #rotates the wrist using the roll
            time.sleep(0.4)
            st_robot.rotate_hand(line[4]) #rotates the hand using the pitch 
            time.sleep(0.4)
        except:
            print('Invalid co-ordinates at line: ' + str(count))
        
    


def main():
    v = triad_openvr.triad_openvr()
    v.print_discovered_objects()
    #imports the st.py as command and then instansiates the arm.
    st_robot = arm.StArm()
    robot_obj = triad_openvr.vr_tracked_device(v.vr,1,"Controller") #Instantiates the object
    robot_input = robot_obj.get_controller_inputs() #Calling the method for htc inputs
    #prompt the user to get alligned with the base station
    
    #TODO: How do I know if the switch is on or off like the toggle?
    #TODO: Create specific scneraios for the robot using different buttons: 1) Gripping 2) fine grain. 
    if(robot_input['menu_button']): 
        time.sleep(0.6)
        text_file = teaching_mode(st_robot,v,robot_obj)
    else:
        replication_mode(text_file,st_robot)
if __name__ == "__main__":
    main()

    
    