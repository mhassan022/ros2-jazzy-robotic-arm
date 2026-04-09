from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import xacro
import os

def generate_launch_description():

    # Package paths
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_lab_gazebo = get_package_share_directory('Adel_Arm')

    # Paths
    meshes_path = os.path.join(pkg_lab_gazebo, 'meshes')
    xacro_file = os.path.join(pkg_lab_gazebo, 'urdf', 'Adel_Arm.urdf')

    # Convert Xacro → URDF
    robot_description = xacro.process_file(xacro_file).toxml()

    # Launch Gazebo (empty world)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # Robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output="screen"
    )

    # Joint state publisher
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )

    # ROS ↔ GZ Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
        # Clock (IGN -> ROS2)
        '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        # Joint states (IGN -> ROS2)
        '/world/empty/Adel_Arm/rrbot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
        ],
        remappings=[
        ('/world/empty/model/Adel_Arm/joint_state', 'joint_states'),
        ],
        output='screen'
        )
    # Spawn URDF robot into Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['--name', 'Adel_Arm', '--topic', '/robot_description'],
        #parameters=[{"use_sim_time": True}],
        output='screen'
    )

    # Controllers
    robot_controller = os.path.join(pkg_lab_gazebo, "config/joint_controller.yaml")
    
    print('path: ', robot_controller)
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controller],
        output="screen"
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--param-file", robot_controller],
    )

    arm_controller_manager_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_group_controller', "--param-file", robot_controller],
        output='screen'
    )

    hand_controller_manager_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['hand_group_controller', "--param-file", robot_controller],
    )

    # RETURN EVERYTHING
    return LaunchDescription([
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', meshes_path),
        bridge,
        gazebo,
        spawn_entity,
        robot_state_publisher_node,
        joint_state_publisher_node,
       # control_node,
       # arm_controller_manager_spawner,
       # hand_controller_manager_spawner,
       # joint_state_broadcaster_spawner,
    ])