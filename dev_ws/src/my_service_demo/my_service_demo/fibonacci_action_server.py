#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from my_interfaces.action import Fibonacci
import time

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )
        self.get_logger().info("Fibonacci Action Server 已启动")

    def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info(f"收到目标请求，order={goal_handle.request.order}")
        feedback_msg = Fibonacci.Feedback()
        result = Fibonacci.Result()

        # 初始化斐波那契数列
        feedback_msg.partial_sequence = [0, 1]
        for i in range(1, goal_handle.request.order):
            # 检查是否收到取消请求
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info("任务被客户端取消")
                return result

            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1]
            )
            # 发布过程反馈
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f"反馈：{feedback_msg.partial_sequence}")
            time.sleep(0.5)

        goal_handle.succeed()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info(f"任务完成，最终序列：{result.sequence}")
        return result

def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
