#!/bin/bash
echo "source /opt/ros/humble/local_setup.bash" >> ~/.bashrc
echo "source /src/ros2_ws/install/setup.bash" >> ~/.bashrc
# ros2 run imu_publisher publisher
source /opt/ros/humble/local_setup.bash
source /src/ros2_ws/install/setup.bash
# ros2 run pixpubsub pixhawk_worker
colcon build 
ros2 run depthsub Depth_node

/bin/bash