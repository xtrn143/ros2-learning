import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs

class TfListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.timer_cb)

    def timer_cb(self):
        try:
            # 构造一个点：在 laser 坐标系
            p_laser = PointStamped()
            p_laser.header.frame_id = "laser"
            p_laser.header.stamp = self.get_clock().now().to_msg()
            p_laser.point.x = 1.0
            p_laser.point.y = 0.0
            p_laser.point.z = 0.0

            # 把点转换到 base_link
            p_base = self.tf_buffer.transform(p_laser, "base_link")
            self.get_logger().info(
                f"Point in base_link: x={p_base.point.x:.2f}, y={p_base.point.y:.2f}, z={p_base.point.z:.2f}"
            )
        except Exception as e:
            self.get_logger().warn(f"Transform not available: {e}")

def main():
    rclpy.init()
    node = TfListener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
