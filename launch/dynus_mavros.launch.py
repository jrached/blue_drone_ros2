from launch import LaunchDescription  
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, EnvironmentVariable 
import os 

def generate_launch_description():
    namespace = LaunchConfiguration("ns")
    veh = os.environ.get("VEH_NAME")
    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument('argname', default_value='val'),
        DeclareLaunchArgument('hostname', default_value='nuc6'),
        DeclareLaunchArgument('tgt_system', default_value='1.1'),
        DeclareLaunchArgument('ns', default_value=EnvironmentVariable("VEH_NAME")),
        DeclareLaunchArgument('fcu_url', default_value='/dev/ttyACM0:921600'),
        DeclareLaunchArgument('respawn_mavros', default_value='false'),
        Node(
            package='ros2_px4_stack',
            executable='track_dynus_traj',
            name='track_dynus_traj_py',
            output='screen',
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='odom_to_mavros',
            arguments=['0', '0', '0', '-1.57', '3.14', '0', 'odom', 'world_mavros']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='odom_to_mocap',
            arguments=['-4.5', '0.0', '0.3', '0.0', '0', '0', 'world_mocap', 'odom'], # podium initial pos (for dynus testing) TODO: Change to initial pose
            # arguments=['1.457', '-3.192', '1.314', '1.576', '0', '0', 'world_mocap', 'odom'] #table close to the control room TODO: Change to initial pose #Usual initial pose
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_odom',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'map']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_ns',
            arguments=['0', '0', '0', '0', '0', '0', f"/{veh}/base_link", '/base_link'] #TODO: Change BD01 to namespace or smth
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_d455',
            arguments=['0', '0', '0', '0', '0', '0', f"{veh}/base_link", f"{veh}/d455_link"]
        ),

        # Launch the repub_mocap node
        Node(
            package='ros2_px4_stack',
            executable='repub_livox',
            name='repub_livox_py',
            namespace=namespace,
            output='screen',
        ),
    ])
