from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os
import xacro


def generate_launch_description():

    pkg_path = get_package_share_directory('rover_description')

    xacro_file = os.path.join(
        pkg_path,
        'urdf',
        'robot.urdf.xacro'
    )

    robot_description_config = xacro.process_file(xacro_file)

    robot_description = {
        'robot_description': robot_description_config.toxml()
    }

    controller_params = os.path.join(
        pkg_path,
        'config',
        'ros2_control.yaml'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controller_params],
        output='screen'
    )

    joint_state_broadcaster_spawner = ExecuteProcess(
        cmd=[
            'ros2',
            'run',
            'controller_manager',
            'spawner',
            'joint_state_broadcaster'
        ],
        output='screen'
    )

    diff_drive_spawner = ExecuteProcess(
        cmd=[
            'ros2',
            'run',
            'controller_manager',
            'spawner',
            'diff_cont'
        ],
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        control_node,
        joint_state_broadcaster_spawner,
        diff_drive_spawner,
        rviz_node
    ])