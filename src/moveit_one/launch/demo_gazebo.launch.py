from launch import LaunchDescription
from launch_ros.actions import SetParameter
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    
    # Gazebo simulator from Adel_Arm package
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('Adel_Arm'),
                'launch',
                'sim.launch.py'
            )
        )
    )

    # MoveIt demo launch from moveit_one (or moveit_try if renamed)
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('moveit_one'),
                'launch',
                'demo.launch.py'
            )
        )
    )

    return LaunchDescription([
        SetParameter(name="use_sim_time", value=True),
        gazebo_launch,
        moveit_launch,
    ])