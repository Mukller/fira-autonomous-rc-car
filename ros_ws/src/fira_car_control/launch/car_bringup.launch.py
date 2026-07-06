"""Bring up the full onboard autonomous stack.

Does not include a camera driver node — that's supplied by whichever
camera package fits the hardware eventually chosen (v4l2_camera for a USB
camera, camera_ros for CSI on Raspberry Pi, etc. — see roadmap).
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='fira_car_control',
            executable='lane_detection_node',
            name='lane_detection_node',
            output='screen',
        ),
        Node(
            package='fira_car_control',
            executable='steering_control_node',
            name='steering_control_node',
            output='screen',
        ),
        Node(
            package='fira_car_control',
            executable='speed_control_node',
            name='speed_control_node',
            output='screen',
        ),
        Node(
            package='fira_car_control',
            executable='serial_bridge_node',
            name='serial_bridge_node',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'baud_rate': 115200,
            }],
        ),
    ])
