import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
def generate_launch_description():
    #利用 IncludeLaunchDescription 加载 launch 文件
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('turtlesim'), "/launch","/turtlesim.launch.py"]
        )
    )

    #利用ExecuteProcess动作执行命令行
    action_execute_process = launch.actions.ExecuteProcess(
        cmd=['ros2', 'service', 'call', '/turtlesim1/spawn', 'turtlesim/srv/Spawn', '{x: 1, y: 2}']
    )

    #利用 LogInfo动作输出日志
    action_log_info = launch.actions.LogInfo(
        msg='使用launch 来调用服务生成海龟'
    )

    #利用定时器动作实现依次启动日志输出和进程执行，并使用GroupAction封装成组合
    action_group = launch.actions.GroupAction([
        launch.actions.TimerAction(
            period=3.0,
            actions=[action_log_info]
        ),
        launch.actions.TimerAction(
            period=5.0,
            actions=[action_execute_process]
        )
    ])

    #合成启动描述并返回
    launch_description = launch.LaunchDescription([
        action_include_launch,
        action_group
    ])

    return launch_description

    