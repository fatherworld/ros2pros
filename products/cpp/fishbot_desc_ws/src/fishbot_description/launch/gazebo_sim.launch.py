import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
def generate_launch_description():
    #获取默认路径
    root_name_in_model = "fishbot"
    urdf_turorial_path = get_package_share_directory('fishbot_description')
    default_model_path = urdf_turorial_path + "/urdf/fishbot/fishbot.urdf.xacro"
    default_world_path = urdf_turorial_path + "/world/custom_room.world"
    # 为launch 声明参数
    action_declare_arg_model_path=launch.actions.DeclareLaunchArgument(
        name='model',default_value=str(default_model_path),
        description='urdf 的绝对路径'
    )

     #获取文件类容生成新的参数
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(['xacro ',launch.substitutions.LaunchConfiguration('model')]),
        value_type=str
    )

    #启动robot_state_publisher状态发布节点
    action_node_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    #通过IncludeLaunchDescription 包含另外一个launch文件
    launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']),
        #传递参数
        launch_arguments=[('world',default_world_path),('verbose','true')]
    )

    #请求Gazebo加载机器人
    spawn_entity_node = launch_ros.actions.Node(
        package = 'gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic','/robot_description',
                   '-entity',root_name_in_model]
    )

    return launch.LaunchDescription(
        [
            action_declare_arg_model_path,
            action_node_robot_state_publisher,
            launch_gazebo,
            spawn_entity_node
        ]
    )