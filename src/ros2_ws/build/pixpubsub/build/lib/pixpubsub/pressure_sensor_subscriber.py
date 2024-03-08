import rclpy
from rclpy.node import Node
from sensor_msgs.msg import FluidPressure

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.get_logger().info("Starting depth node")
        self.subscription = self.create_subscription(
            FluidPressure,
            'sensor_data',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

        # Initialize configurable parameters
        self.initialize_parameters()

    def initialize_parameters(self):
        # Configurable parameters
        self.declare_parameter("surface_pressure", 101325) # Pa
        self.declare_parameter("fluid_density", 1025) # kg/m³
        self.declare_parameter("gravity", 9.81) # m/s²
        self.declare_parameter("max_depth", 2) # meters

    def calculate_depth(self, fluid_pressure):
        # Get the configurable parameters
        surface_pressure = self.get_parameter("surface_pressure").value
        fluid_density = self.get_parameter("fluid_density").value
        gravity = self.get_parameter("gravity").value
        max_depth = self.get_parameter("max_depth").value

        # Calculate the depth
        depth = (fluid_pressure - surface_pressure) / (fluid_density * gravity)
        # Ensure the depth is within the pool's maximum depth
        if depth > max_depth:
            depth = max_depth
        return depth

    def listener_callback(self, msg):
        # Check if the 'fluid_pressure' field exists in the message
        if hasattr(msg, 'fluid_pressure'):
            depth = self.calculate_depth(msg.fluid_pressure)
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