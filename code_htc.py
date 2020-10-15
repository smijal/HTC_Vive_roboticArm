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
## 4. HAIR TRIGGER -> pick and drop with hand                                                                                              ## 
############################################################################################################################################# 

# @authors: Lohith Muppala and Stefan Mijalkov
# """
import triad_openvr
import time
import sys
import arm
import os

#GLOBAL VARIABLES FOR NOW, MOSTLY FOR TESTING PURPOSES
current_posX = 0.0
robot_position = [-310.0,303.3,169.2]

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
    global current_posX
    global robot_position
    vive_position = v.devices["controller_1"].get_pose_euler()
    if(vive_position==None):
        print("Vive can't read, make sure the controller and the base station can communicate...")
    else:
        displacementX = current_posX-vive_position[0]
        current_posX = vive_position[0]
        if(abs(displacementX*250) < 8):
            print("Displacement too small")
        else:
            robot_position[0] = round(robot_position[0]+displacementX*250, 1)
            #a.move_to(robot_position)
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
    return f

#st_robot is taken out
#------------------------------------------------
# The function's main purpose is to replicate the motions, previously learned
# Parameters: txt-> text file to read from, a -> St Robotics Arm object   
# Returns:  None
#------------------------------------------------
def replication_mode(txt):
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
    #Instantiate the robotic arm object, set it to the convinient position for start.
    global robot_position
    # a = arm.StArm()
    # a.move_to(robot_position)
    # a.rotate_hand(30.0)

    #default system state, and mode (System OFF, Mode: Save)       
    system_ON = False
    modes = ['Teaching', 'Save', 'Replicating', 'Stop']
    currMode = modes[1]

    #TODO: Create a file that stores the previous num_paths (Example: 5 files are stored already, (file0 to file4), take the value stored and continue from there)
    num_paths = 0 #useful for creating more than one file (ex: file0, file1 ...)

    #Vive controller and tracker objects
    v = triad_openvr.triad_openvr()
    v.print_discovered_objects()
    controller = triad_openvr.vr_tracked_device(v.vr,1,"Controller") #Instantiates the object

    #To create a new directory for saving the different coordinate files
    current_directory = os.path.dirname(os.path.abspath(__file__))
    final_directory = os.path.join(current_directory, r'movement_paths')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    #to open a new text file in the new directory
    filename = os.path.join(final_directory, "coords" + str(num_paths) + ".txt")   
    f = open(filename, "w+") #collects the co-ords in a text file.

    #TODO: prompt the user to get alligned with the base station - NOT DONE !!!
    #print_cords(v)

    #interval frequency for coordinates to be scanned from Vive (Can be manipulated) 
    if len(sys.argv) == 1:
        interval = 1/250
    elif len(sys.argv) == 2:
        interval = 1/float(sys.argv[1])
    else:
        print("Invalid number of arguments")
        interval = False
    
    #Main controll, polling and wait for Vive button triggers to perform different functionalities
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

if __name__ == "__main__":
   main()

    