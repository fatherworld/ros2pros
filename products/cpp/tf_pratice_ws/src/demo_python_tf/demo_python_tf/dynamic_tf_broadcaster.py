import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from tf_transformations import quaternion_from_euler

class DynamicTFBroadcaster(Node):
    def __init__(self,nodename):
        super().__init__(nodename)
        self.broadcaster = TransformBroadcaster(self)
        #动态tf需要持续发布，这里发布频率设置为100hz,0.01s发布一次
        self.timer = self.create_timer(0.01,self.publish_dynamic_tf)
        #self.timer = self.create_timer(1,self.broadcast_timer_callback)
    
    def publish_dynamic_tf(self,):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "camera_link"
        transform.child_frame_id = "bottom_link"
        transform.transform.translation.x = 0.2
        transform.transform.translation.y = 0.0
        transform.transform.translation.z = 0.1
        #欧拉角转换四元数
        q = quaternion_from_euler(math.radians(0),0,0)
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        #发布坐标转
        self.broadcaster.sendTransform(transform)
        self.get_logger().info(f'发布动态坐标转换')

def main():
    rclpy.init()
    node = DynamicTFBroadcaster("tf_broadcaster")
    rclpy.spin(node)
    rclpy.shutdown()