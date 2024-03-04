import copy
import time
import argparse
import cv2 as cv
import numpy as np
import rclpy
from pupil_apriltags import Detector
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String

class DepthPublisher(Node):
    
    def __init__(self):

        super().__init__('depth_publisher')

        def main(self):
            rclpy.init()
            self.publisher_ = self.create_publisher(Float32MultiArray, 'depth_topic', 10)
            timer_period = 0.5
            self.timer = self.create_timer(timer_period, self.depth_estimation)
            rclpy.spin(self)
            rclpy.shutdown()

        
        def depth_estimation(self):
            cap_device = 0
            cap_width = 10000 # Cap width
            cap_height = 1000 # Cap height
            families = "tag36h11"
            nthreads = 1
            quad_decimate = 2.0
            quad_sigma = 0.0
            refine_edges = 1
            decode_sharpening = 0.25
            debug = 0

            cap = cv.VideoCapture(cap_device)
            cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
            cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

            at_detector = Detector(
                families=families,
                nthreads=nthreads,
                quad_decimate=quad_decimate,
                quad_sigma=quad_sigma,
                refine_edges=refine_edges,
                decode_sharpening=decode_sharpening,
                debug=debug,
            )

            elapsed_time = 0

            while True:
                start_time = time.time()
                ret, image = cap.read()
                if not ret:
                    break
                
                #increase brightness
                hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
                h, s, v = cv.split(hsv)
                lim = 255 - value
                v[v > lim] = 255
                v[v <= lim] += value
                final_hsv = cv.merge((h, s, v))
                image = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)

                #Increase blue channel
                blue_channel = image[:, :, 0].astype(np.float32)
                blue_channel *= 1.5
                blue_channel = np.clip(blue_channel, 0, 255).astype(np.uint8)
                image[:, :, 0] = blue_channel

                image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

                tags = at_detector.detect(
                    image,
                    estimate_tag_pose=False,
                    camera_params=None,
                    tag_size=None,
                )

                #The location of the april tag
                center = (int(center[0]), int(center[1]))
                corner_01 = (int(corners[0][0]), int(corners[0][1]))
                corner_02 = (int(corners[1][0]), int(corners[1][1]))
                corner_03 = (int(corners[2][0]), int(corners[2][1]))
                corner_04 = (int(corners[3][0]), int(corners[3][1]))
                size = np.sqrt((tag.corners[0][0] - tag.corners[2][0])**2 + (tag.corners[0][1] - tag.corners[2][1])**2)
                
                no_detection_start_time = None
                tag_size = 0.1
                focal_length = 500

                if len(tags) > 0:
                    distance = self.calculate_distance_to_tag(tag[0], focal_length, tag_size)
                    self.publish_depth(distance)
                else:
                    if self.no_detection_start_time is None:
                        self.no_detection_start_time = time.perf_counter()
                    elif time.perf_counter() - self.no_detection_start_time >= 2:
                        self.publish_message("AUV is very near the pool floor.")
                
                def calculate_distance_to_tag(self, tag, focal_length, tag_size):
                    size = np.sqrt((tag.corners[0][0] - tag.corners[2][0])**2 + (tag.corners[0][1] - tag.corners[2][1])**2)
                    return focal_length * tag_size / size

                def publish_depth(self, distance):
                    distance_km = distance / 1000
                    msg = Float32MultiArray()
                    msg.data = [distance_km]
                    self.publisher_.publish(msg)

                def publish_message(self, message):
                    msg = String()
                    msg.data = message

                    self.publisher_.publish(msg)


if __name__ == '__main__':
    depth_publisher = DepthPublisher()
    depth_publisher.main()