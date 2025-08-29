import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
from tf_transformations import quaternion_from_euler

class StaticTFBroadcaster(Node):
    def __init__(self,nodename):
        super().__init__(nodename)
        self.static_broadcaster = StaticTransformBroadcaster(self)
        #self.timer = self.create_timer(1,self.broadcast_timer_callback)
    
    def publish_static_tf(self,):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "base_link"
        transform.child_frame_id = "camera_link"
        transform.transform.translation.x = 0.5
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.6
        #欧拉角转换四元数
        q = quaternion_from_euler(math.radians(0),0,0)
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        #发布静态坐标转换，静态坐标变换只需要发布一次，ROS2会为订阅者保留数据，当出现新的订阅者时，可以直接获取到保留的数据
        self.static_broadcaster.sendTransform(transform)
        self.get_logger().info(f'发布静态坐标转换')

def main():
    rclpy.init()
    node = StaticTFBroadcaster("static_tf_broadcaster")
    node.publish_static_tf()
    rclpy.spin(node)
    rclpy.shutdown()

