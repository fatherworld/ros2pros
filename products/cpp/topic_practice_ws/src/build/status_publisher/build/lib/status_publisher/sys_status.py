import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus #导入消息接口
import psutil
import platform

class SysStatusPub(Node):
    def __init__(self,nodename):
        super().__init__(nodename)
        self.status_pub = self.create_publisher(SystemStatus,"sys_status",10)
        self.timer = self.create_timer(1,self.timecallback)
    
    def timecallback(self,):
        #获取系统硬件信息
        cpu_percent=psutil.cpu_percent()
        memory_info=psutil.virtual_memory()
        net_io_counter=psutil.net_io_counters()

        msg=SystemStatus()
        msg.stamp=self.get_clock().now().to_msg()
        msg.hostname=platform.node()
        msg.cpu_percent=cpu_percent
        msg.memory_percent=memory_info.percent
        msg.memory_total=memory_info.total/1024/1024
        msg.memory_avaliable=memory_info.available/1024/1024
        msg.net_sent=net_io_counter.bytes_sent/1024/1024
        msg.net_recv=net_io_counter.bytes_sent/1024/1024

        self.get_logger().info(f'发布:{str(msg)}')
        self.status_pub(msg)

def main():
    rclpy.init()
    node = SysStatusPub('sys_status_pub')
    rclpy.spin(node)
    rclpy.shutdown()