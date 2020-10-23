import triad_openvr
import arm
import time
import sys

a = arm.StArm()

initial_pos = [-310.0,303.3,169.2]
a.move_to(initial_pos)
a.rotate_hand(30.0)


