import arm
a = arm.StArm()
a.set_speed(1200)
x= a.where()
print(x)
pos = [-310.0,303.3,169.2,57.4,-61.6,0.0]
a.move_to(pos)
x= a.where()
pos[0] = -100
a.move_to(pos)
x= a.where()
print(x)