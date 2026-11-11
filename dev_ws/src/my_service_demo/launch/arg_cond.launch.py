from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():
    # 声明启动参数：declare_launch_argument
    enable_action_server_arg = DeclareLaunchArgument(
        "enable_action_server",
        default_value="true",
        description="Whether to start fibonacci action server"
    )

    robot_name_arg = DeclareLaunchArgument(
        "robot_name",
        default_value="default_robot",
        description="Name of robot, pass from command line"
    )

    # 获取参数的值（LaunchConfiguration，是一个替换器，不是普通字符串）
    enable_action_server = LaunchConfiguration("enable_action_server")
    robot_name = LaunchConfiguration("robot_name")

    return LaunchDescription([
        enable_action_server_arg,
        robot_name_arg,

        # 参数节点，直接把 launch 传进来的 robot_name 作为节点参数
        Node(
            package="my_service_demo",
            executable="param_demo",
            name="param_demo_node",
            output="screen",
            parameters=[
                {"robot_name": robot_name},
                {"control_frequency": 10.0}
            ]
        ),

        # 服务端：一直启动
        Node(
            package="my_service_demo",
            executable="add_two_ints_server",
            name="add_two_ints_server",
            output="screen"
        ),

        # Action Server：加 IfCondition，只有 enable_action_server=true 才启动
        Node(
            package="my_service_demo",
            executable="fibonacci_action_server",
            name="fibonacci_action_server",
            output="screen",
            condition=IfCondition(enable_action_server)
        )
    ])
