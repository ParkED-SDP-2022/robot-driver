source ~/.bashrc

lxterminal --command="source ~/.bashrc -c 'rosrun robot-driver manual_driver.py; /bin/bash'"
lxterminal --command="source ~/.bashrc -c 'rosrun robot-driver cmd_vel_test.py; /bin/bash'"

