import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/bayes/hssw/others/ros2project/test/python/workspace/src/install/demo_python_pkg'
