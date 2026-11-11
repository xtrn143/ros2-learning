#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult

class ParamDemoNode(Node):
    def __init__(self):
        super().__init__('param_demo_node')
        # 声明参数
        self.declare_parameter("robot_name", "mini_robot")
        self.declare_parameter("control_frequency", 10.0)
        self.declare_parameter("enable_sensor", True)
        self.declare_parameter("waypoints", [1.0, 2.0, 3.0])

        # 注册参数修改回调
        self.add_on_set_parameters_callback(self.param_change_callback)

        self.timer = self.create_timer(2.0, self.timer_callback)

    def param_change_callback(self, params: list[Parameter]) -> SetParametersResult:
        """参数被修改时自动触发"""
        result = SetParametersResult()
        result.successful = True  # 默认允许修改

        for param in params:
            self.get_logger().info(f"检测到参数变更: {param.name} = {param.value}")
            # 这里可以加校验逻辑：不符合条件就拒绝修改
            if param.name == "control_frequency" and param.value < 0.1:
                self.get_logger().error("control_frequency 不能小于0.1，拒绝修改！")
                result.successful = False

        return result

    def timer_callback(self):
        robot_name = self.get_parameter("robot_name").get_parameter_value().string_value
        freq = self.get_parameter("control_frequency").get_parameter_value().double_value
        enable_sensor = self.get_parameter("enable_sensor").get_parameter_value().bool_value
        waypoints = self.get_parameter("waypoints").get_parameter_value().double_array_value

        self.get_logger().info(f"robot_name: {robot_name}")
        self.get_logger().info(f"control_frequency: {freq}")
        self.get_logger().info(f"enable_sensor: {enable_sensor}")
        self.get_logger().info(f"waypoints: {waypoints}")

def main(args=None):
    rclpy.init(args=args)
    node = ParamDemoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
