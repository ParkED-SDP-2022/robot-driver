import subprocess

roscore = subprocess.Popen(["lxterminal", "-e", "roscore"])
cmd_vel_test = subprocess.Popen(["lxterminal", "-e", "rosrun", "robot-driver", "cmd_vel_test.py"])
firmware_test = subprocess.Popen(["lxterminal", "-e", "rosrun", "robot-driver", "firmwareTest.py"])