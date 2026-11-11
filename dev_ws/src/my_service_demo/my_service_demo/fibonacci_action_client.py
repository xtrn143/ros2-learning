#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_interfaces.action import Fibonacci
import sys

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # 等待服务端
        self._action_client.wait_for_server()

        # 发送goal，绑定回调：收到反馈、goal被接受、拿到最终结果
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('目标被拒绝')
            return

        self.get_logger().info('目标已接受，等待结果...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        # 收到过程反馈时执行
        feedback = feedback_msg.feedback
        self.get_logger().info(f"收到反馈：{feedback.partial_sequence}")

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"最终结果序列：{result.sequence}")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()

    if len(sys.argv) != 2:
        action_client.get_logger().error("用法：ros2 run my_service_demo fibonacci_action_client 8")
        return
    target_order = int(sys.argv[1])

    action_client.send_goal(target_order)
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
