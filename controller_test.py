import triad_openvr
import time
import sys

v = triad_openvr.triad_openvr()
v.print_discovered_objects()
d = triad_openvr.vr_tracked_device(v.vr,1,"Controller") #I added this

if len(sys.argv) == 1:
    interval = 1/5
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

#print(interval)

if interval:
    while(True):
        start = time.time()
        txt = ""
        # for each in v.devices["controller_1"].get_pose_euler():
        #     txt += "%.4f" % each
        #     txt += " "
        # print("\r" + txt, end="")   #positions are commented out
        roll = v.devices["controller_1"].get_pose_euler()[5]
        print(roll)
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
        #test = d.get_controller_inputs() #and this
        #print(test)