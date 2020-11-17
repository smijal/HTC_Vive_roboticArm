
import os
from PIL import Image,ImageTk
import triad_openvr
import time
import sys
import arm
import code_htc
from pydub import AudioSegment
from pydub.playback import play

robot_position = [-310.0,303.0,170.0]

#Initializes the ARM -> calibrate, send to home position, adjust speed
a = arm.StArm()
time.sleep(0.5)
# a.move_to(robot_position)
# time.sleep(0.5)
# a.rotate_hand(30.0)
# time.sleep(0.5)
a.set_speed(8000)

def replication_mode(txt):
	global a,robot_position
	f = open(txt, 'r') 
	Lines = f.readlines()
	if(not Lines):
		print("File is empty, Nothing to replicate...")
		return None
	a.move_to(robot_position)
	time.sleep(0.5)
	a.rotate_hand(5.0)
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
		try:
			a.move_to(position)
			time.sleep(0.4)
		except:
			print("Invalid position")
	f.close()


current_directory = os.path.dirname(os.path.abspath(__file__))
final_directory = os.path.join(current_directory, 'movement_paths')
file_dir = os.path.join(final_directory,'coords21.txt')
replication_mode(file_dir)