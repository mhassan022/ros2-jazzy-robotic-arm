cmake_minimum_required(VERSION 3.8)
project(Adel_Arm)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# -------------------------------------------------------
# Dependencies
# -------------------------------------------------------
find_package(ament_cmake REQUIRED)
find_package(controller_manager REQUIRED)
find_package(ros2_control REQUIRED)
find_package(ros2_controllers REQUIRED)
find_package(gripper_controllers REQUIRED)
find_package(trajectory_msgs REQUIRED)

find_package(ros_gz REQUIRED)
find_package(ros_gz_sim REQUIRED)
find_package(ros_gz_bridge REQUIRED)
find_package(ros_gz_image REQUIRED)
find_package(gz_ros2_control REQUIRED)

find_package(rclcpp REQUIRED)
find_package(xacro REQUIRED)

# -------------------------------------------------------
# Install URDF, meshes, config, and launch files
# -------------------------------------------------------
install(
  DIRECTORY launch urdf config meshes
  DESTINATION share/${PROJECT_NAME}/
)

# -------------------------------------------------------
# Testing (optional)
# -------------------------------------------------------
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_cpplint_FOUND TRUE)
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# -------------------------------------------------------
# Package export
# -------------------------------------------------------
ament_package()