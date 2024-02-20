#!/bin/bash
ros2 run image_publisher image_publisher_node /tmp/images/people_cycles.jpg --ros-args --remap /image_raw:=/image
