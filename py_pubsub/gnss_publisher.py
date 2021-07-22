import rclpy
from rclpy.node import Node
from tutorial_interfaces.msg import Num    # CHANGE


serialPort = serial.Serial(port="/", baudrate=115200)
serialString = ""

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Num, 'topic', 10)     # CHANGE
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        msg = Num()                                           # CHANGE
        msg.num = self.i                                      # CHANGE
        self.publisher_.publish(msg)
        self.get_logger().info('Publishingggg: "%d"' % msg.num)  # CHANGE
        self.i += 1.0


def main(args=None):
    ## Read Serial -->>>>
 
    '''
    1  read serial --> 
    1.1 find -> lat long alt 
    1.2 
    2  publish ros node

    '''

    ##
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()