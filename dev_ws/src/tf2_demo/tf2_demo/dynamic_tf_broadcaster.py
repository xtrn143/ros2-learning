import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

class DynamicTfBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.timer_cb)
        self.x = 0.0
        self.speed = 0.2  # m/s

    def timer_cb(self):
        now = self.get_clock().now().to_msg()
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"

        # x 持续增加，小车向前走
        self.x += self.speed * 0.1
        t.transform.translation.x = self.x
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        # 朝向不变，无旋转
        t.transform.rotation.w = 1.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0

        self.broadcaster.sendTransform(t)
        self.get_logger().info(f"robot odom x: {self.x:.2f}")

def main():
    rclpy.init()
    node = DynamicTfBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
