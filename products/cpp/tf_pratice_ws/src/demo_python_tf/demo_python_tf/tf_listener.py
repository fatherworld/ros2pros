import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener,Buffer
from tf_transformations import euler_from_quaternion

class TFListener(Node):
    def __init__(self,nodename):
        super().__init__(nodename)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer,self)
        self.timer = self.create_timer(1,self.get_transform)
    
    def get_transform(self,):
        try:
            result = self.tf_buffer.lookup_transform('base_link','bottom_link',rclpy.time.Time(seconds=0),rclpy.duration.Duration(seconds=1))
            transform = result.transform
            rotation_euler = euler_from_quaternion([transform.rotation.x,transform.rotation.y,transform.rotation.z,transform.rotation.w])
            self.get_logger().info(f'获取坐标转换成功，位姿为：{transform.translation}，欧拉角为：{rotation_euler}')
        except Exception as e:
            self.get_logger().info(f'获取坐标转换失败,原因:{str(e)}')

def main():
    rclpy.init()
    node = TFListener("tf_listener")
    rclpy.spin(node)
    rclpy.shutdown()