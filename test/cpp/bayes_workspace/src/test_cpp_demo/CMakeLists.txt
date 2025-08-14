cmake_minimum_required(VERSION 3.8)
project(test_cpp_demo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(bayes_test src/bayestest.cpp)

find_package(rclcpp REQUIRED)

add_executable(mainPerson src/mainPerson.cpp src/PersonNode.cpp)
target_include_directories(mainPerson PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include/test_cpp_demo/)
ament_target_dependencies(mainPerson rclcpp)

message(${CMAKE_CURRENT_SOURCE_DIR})
add_executable(WriteNode src/WriteNode.cpp src/PersonNode.cpp)
target_include_directories(WriteNode PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include/test_cpp_demo/)
ament_target_dependencies(WriteNode rclcpp)

install(TARGETS
  bayes_test
  WriteNode
  mainPerson
  DESTINATION lib/${PROJECT_NAME}
)
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
