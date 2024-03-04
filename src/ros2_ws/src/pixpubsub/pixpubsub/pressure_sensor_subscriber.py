import rclpy
from rclpy.node import Node
from sensor_msgs.msg import FluidPressure

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            FluidPressure,
            'sensor_data',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):

        # Check if the 'fluid_pressure' field exists in the message
        if hasattr(msg, 'fluid_pressure'):

            # Assuming the pressure at the surface is 101325 Pa
            surface_pressure = 101325  # Pa

            # Fluid density for water
            fluid_density = 1025  # kg/m³

            # Acceleration due to gravity
            gravity = 9.81  # m/s²

            # Calculate the depth
            depth = (msg.fluid_pressure - surface_pressure) / (fluid_density * gravity)

            # Ensure the depth is within the pool's maximum depth
            max_depth = 2  # meters
            if depth > max_depth:
                depth = max_depth
    
            self.get_logger().info(f'Calculated Depth: {depth} meters')

        else:
            self.get_logger().warn('The message does not contain a fluid_pressure field')

def main(args=None):
    
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()