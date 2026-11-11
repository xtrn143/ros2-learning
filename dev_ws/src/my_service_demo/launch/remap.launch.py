from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="my_service_demo",
            executable="add_two_ints_server",
            name="add_two_ints_server",
            output="screen",
            remappings=[
                # ("原始名字", "新名字")
                ("/add_two_ints", "/my_add_two_ints")
            ]
        )
    ])
