import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    pkg_share = get_package_share_directory("my_service_demo")
    param_file = os.path.join(pkg_share, "config", "params.yaml")

    return LaunchDescription([
        # 参数节点
        Node(
            package="my_service_demo",
            executable="param_demo",
            name="param_demo_node",
            output="screen",
            parameters=[param_file]
        ),
        # AddTwoInts 服务端
        Node(
            package="my_service_demo",
            executable="add_two_ints_server",
            name="add_two_ints_server",
            output="screen"
        ),
        # Fibonacci Action Server
        Node(
            package="my_service_demo",
            executable="fibonacci_action_server",
            name="fibonacci_action_server",
            output="screen"
        )
    ])
