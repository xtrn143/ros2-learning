import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener, TransformException
from geometry_msgs.msg import TransformStamped
import tf2_geometry_msgs

class TfLookupDemo(Node):
    def __init__(self):
        super().__init__('tf_lookup_demo')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.timer_cb)

    def timer_cb(self):
        try:
            # lookup_transform(target_frame, source_frame, time)
            # 含义：拿到 source_frame → target_frame 的变换
            t: TransformStamped = self.tf_buffer.lookup_transform(
                "base_link",
                "laser",
                rclpy.time.Time()
            )
            self.get_logger().info(
                f"laser relative to base_link: "
                f"x={t.transform.translation.x:.2f}, "
                f"y={t.transform.translation.y:.2f}, "
                f"z={t.transform.translation.z:.2f}; "
                f"q({t.transform.rotation.w:.2f}, {t.transform.rotation.x:.2f}, "
                f"{t.transform.rotation.y:.2f}, {t.transform.rotation.z:.2f})"
            )
        except TransformException as e:
            self.get_logger().warn(f"lookup transform failed: {e}")

def main():
    rclpy.init()
    node = TfLookupDemo()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
