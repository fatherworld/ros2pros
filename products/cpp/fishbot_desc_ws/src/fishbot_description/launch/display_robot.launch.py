import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
def generate_launch_description():
    #获取默认路径
    urdf_tutorial_path = get_package_share_directory('fishbot_description')
    default_model_path = urdf_tutorial_path + '/urdf/first_robot.urdf.xacro'
    default_rviz_config_path = urdf_tutorial_path + '/config/rviz/display_model.rviz'
    #为launch 声明参数
    action_declare_model_path = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=default_model_path,
        description='Absolute path to robot urdf file'
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
    #启动joint_state_publisher关节状态发布节点
    action_node_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )
    #启动rviz节点   
    action_node_rviz = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path],
    )

    #合成启动描述并返回
    launch_description = launch.LaunchDescription([
        action_declare_model_path,
        action_node_robot_state_publisher,
        action_node_joint_state_publisher,
        action_node_rviz,
    ])
    return launch_description
