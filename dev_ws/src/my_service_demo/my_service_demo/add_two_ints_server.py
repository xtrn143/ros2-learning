#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_interfaces.srv import AddTwoInts

class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.callback)
        self.get_logger().info("服务端已启动，等待请求...")

    def callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f"收到请求: a={request.a}, b={request.b} -> sum={response.sum}")
        return response

def main(args=None):
    rclpy.init(args=args)
    server = AddTwoIntsServer()
    rclpy.spin(server)
    server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
