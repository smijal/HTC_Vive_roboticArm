import triad_openvr
import arm
import time
import sys

########### THIS SPACE IS FOR THE ARM CODE AND FUNCTION CALLS ###############
#a = arm.StArm()
#############################################################################


########### THIS SPACE IS FOR THE HTC VIVE CODE AND FUNCTION CALLS ###############

## System is initially "OFF", in a sense that it is polling for htc vive key presses but any key press except the MENU key won't affect the output
## Once Menu key is pressed, system turns ON, meaning it is i na default (most likely replication mode)
## At this point if the trigger key is pressed, it will be switching between modes (start teaching mode, or stop teaching mode and save)
## When the system is ON and in Teaching Mode, coordinates are being displayed on screen,(TO ADD : Saving coordinates in a file, TO ADD: Send direct commands to the robotic arm based on displacement)
## IF the MENU key is pressed at any time, System turns off.
## Proper use for now is:  Press MENU button->system ON, Press trigger -> system teaching mode , Press trigger again -> stops teaching saves coordinates, Press MENU -> system off

## QUESTIONS:
## Do you think gripper is convinient to use for start,stop teaching and then we do another key for replication mode?
## OR is it better that we use gripper to be switching between replicate and teach?

v = triad_openvr.triad_openvr() 
v.print_discovered_objects()
d = triad_openvr.vr_tracked_device(v.vr,1,"Controller") #to get inputs from HTC Vive
currMode = "save" #fake state, meaning it doesn't start with teaching by default
on = False #system OFF by default

#starts stops-saves the teaching mode
#called only if system is ON
def teaching_start_stop():
    global currMode
    global on
    if(on):
        if(currMode=="teaching"):
            currMode="save"
        elif(currMode=="save"):
            currMode="teaching"
        return currMode

# since this function is called inside the main while loop, acts as polling for HTC Vive inputs
# controlls the system state ON-OFF when MENU key is pressed
# calls the teaching_start_stop if trigger is pressed and system is ON
def polling(d):
    global currMode, on
    vive_inputs = d.get_controller_inputs()
    if(vive_inputs['menu_button']):
        time.sleep(0.6)
        if(on==True):
            on=False
        else:
            on=True
    if(vive_inputs['trigger']>0.97 and on):
        time.sleep(0.8)
        return teaching_start_stop()

# same as original controller_test.py
def getPosition(v):
    start = time.time()
    txt = ""
    for each in v.devices["controller_1"].get_pose_euler():
        txt += "%.4f" % each
        txt += " "
    print("\r" + txt , end="")
    #"    Trigger: " + str(format(vive_inputs['trigger'],".3f")) + "  Grip: " + str(int(vive_inputs['grip_button']))
    sleep_time = interval-(time.time()-start)
    if sleep_time>0:
        time.sleep(sleep_time)

# This is like a main function 
if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

if interval:
    while(True):
        polling(d) #While true, keep searching for key triggers ( We can make this more efficitent and make it actually stall and wait, maybe with threads)
        if(on): #if system ON
            print(currMode) #print the current mode
            if(currMode=="teaching"):
                getPosition(v) #if teaching, display coordinates (TO ADD: Should be calling MOVETO and move the arm based on displacement)
        if(on==False): #print message that system is currently OFF
            print("OFF press the menu button to turn ON", end='\r')
