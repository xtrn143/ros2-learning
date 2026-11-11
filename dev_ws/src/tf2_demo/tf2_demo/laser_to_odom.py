import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener, TransformException
import tf2_geometry_msgs
from geometry_msgs.msg import Point, PointStamped

class LaserToOdom(Node):
    def __init__(self):
        super().__init__('laser_to_odom')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.5, self.timer_cb)

    def timer_cb(self):
        try:
            # 直接查询：laser -> odom，取最新可用，最多等0.5s
            t = self.tf_buffer.lookup_transform(
                target_frame="odom",
                source_frame="laser",
                time=rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.5)
            )

            # 构造在 laser 坐标系下的点
            p_laser = PointStamped()
            p_laser.header.frame_id = "laser"
            p_laser.point.x = 1.0
            p_laser.point.y = 0.0   
            p_laser.point.z = 0.0

            # 使用拿到的变换手动转换
            p_odom = tf2_geometry_msgs.do_transform_point(p_laser, t)

            self.get_logger().info(
                f"Point in odom: x={p_odom.point.x:.2f}, y={p_odom.point.y:.2f}"
            )
        except TransformException as e:
            self.get_logger().warn(f"fail: {e}")

def main():
    rclpy.init()
    node = LaserToOdom()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
