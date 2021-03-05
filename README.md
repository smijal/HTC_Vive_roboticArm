# HTC Vive controlled robotic Arm (ST Robotics R17)

### Content
- [Video explanation](#video-with-a-full-explanation)
- [Getting started](#getting-started)
- [Configuration file](#configuration-file)
- [Run](#run)
- [Hardware schematics](#hardware-schematics)
- [Contributors](#contributors)
- [References](#references)

### **Video with a full explanation:**
- [HTC Vive controlled robotic arm (ST Robotics R17)](https://www.youtube.com/watch?v=tr84YwzHvdM)

### **Getting Started**

1. Clone the repository
2. Install dependencies
3. Install Steam
4. Change the config file



**Imports:**
```
pip install python-tk
pip install Pillow
pip install openvr
pip install pydub
pip install serial

NOTE: Few libraries might not be listed.
```


**Install SteamVR**

Follow the [guide](https://www.acer.com/ac/en/US/content/windows-mixed-reality-setup-steamvr) for installation.



### **Configuration file**

In order to run SteamVR without a headset, config file has to be changed.
Follow the path, find and edit the default.vrsettings file in ProgramFiles ->
`...steamapps/common/SteamVR/resources/settings/default.vrsettings`

Set requireHmd to FALSE.

![image](https://user-images.githubusercontent.com/65141613/110067189-cb74c480-7d38-11eb-8cfe-9b1578b6ddcf.png)



### **Run**

1. Run the program_launcher.py
1. Follow the GUI


### **Hardware schematics**

![image](https://user-images.githubusercontent.com/65141613/110068133-a6815100-7d3a-11eb-8017-9875347dde6a.png)



### **Contributors**
- [Stefan Mijalkov](https://smijal.github.io/)
- [Joshua Zychal](https://www.linkedin.com/in/josh-zychal-1a4278191/)
- [Lohith Muppala](https://www.linkedin.com/in/lohithmuppala/)
- Ali Kazmi



### **References**
- [TriadSemi/triad_openvr](https://github.com/TriadSemi/triad_openvr)
- [OlinRoboticsAndBioinspiration/st](https://github.com/OlinRoboticsAndBioinspiration/st/blob/master/st.py)
- [ST Robotics](https://strobotics.com/info2.htm)


