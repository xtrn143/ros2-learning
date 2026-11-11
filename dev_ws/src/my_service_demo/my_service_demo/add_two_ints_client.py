#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_interfaces.srv import AddTwoInts
import sys

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        # 创建客户端，和服务端名字、类型必须一一对应
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        # 等待服务上线，最多等1秒
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务 add_two_ints 上线...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        # 异步发送请求，拿到future
        self.future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    client = AddTwoIntsClient()

    # 从命令行读取两个数字
    if len(sys.argv) != 3:
        client.get_logger().error("用法：ros2 run my_service_demo add_two_ints_client 4 5")
        return
    a = int(sys.argv[1])
    b = int(sys.argv[2])

    response = client.send_request(a, b)
    client.get_logger().info(f"收到结果: {a} + {b} = {response.sum}")

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
