import launch
import launch_ros

def generate_launch_description():
    #launch 可以将参数传递给节点，可以给turtle_control 传递max_speed参数
    action_declare_max_speed = launch.actions.DeclareLaunchArgument(
        name='launch_max_speed',
        default_value='2.0',
        description='max speed of turtle'
    )

    action_node_turtle_control = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='turtle_control',
        #使用 launch 中参数launch_max_speed值，替换节点中的max_speed参数
        parameters=[{'max_speed': launch.substitutions.LaunchConfiguration('launch_max_speed',default='2.0')}],
        output='screen',
    )
    action_node_turtle_client = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='patrol_client',
        output='log',
    )
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='both',
    )

    #合成启动描述并返回
    launch_description = launch.LaunchDescription([
        action_declare_max_speed,
        action_node_turtle_control,
        action_node_turtle_client,
        action_node_turtlesim_node,
    ])
    return launch_description