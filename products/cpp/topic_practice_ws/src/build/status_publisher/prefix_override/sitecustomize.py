import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/bayes/hssw/others/ros2project/products/cpp/topic_practice_ws/src/install/status_publisher'
