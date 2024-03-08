#!/bin/bash

source /opt/ros/humble/setup.bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

if [ -f "/src/ros2_ws/install/setup.bash" ]; then
    echo "source /src/ros2_ws/install/setup.bash" >> ~/.bashrc
else
    source /opt/ros/humble/setup.bash
    cd /src/ros2_ws/
    colcon build
    echo "source /src/ros2_ws/install/setup.bash" >> ~/.bashrc
fi

source /src/ros2_ws/install/setup.bash

echo "alias bws='/scripts/build_ws.sh'" >> ~/.bashrc
echo "alias sws='/scripts/source_ws.sh'" >> ~/.bashrc
echo "Setup finished."
ros2 run pixpubsub pixhawk_worker
ros2 run pixpubsub Depth_node
/bin/bash
