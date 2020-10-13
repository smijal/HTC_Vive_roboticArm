import triad_openvr
import arm
import time
import sys

a = arm.StArm()

initial_pos = [-310.0,303.3,169.2]
second_pos = [-300.0, 303.3, 169.2]
third_pos = [-310.0, 303.3, 169.2]
a.move_to(initial_pos)
a.rotate_hand(30.0)

positions = [initial_pos,second_pos,third_pos]
i = 1
while(True):
    a.move_to(positions[i])
    i+=1
    i=i%3

