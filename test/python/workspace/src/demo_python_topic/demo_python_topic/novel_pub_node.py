import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String #ros2定义消息接口类型
from queue import Queue
from threading import Thread
class NovelPubNode(Node):
    def __init__(self,nodename:str):
        super().__init__(nodename)
        #创建发布者
        self.novel_queue=Queue()
        self.novel_pub = self.create_publisher(String,'novel',10) #参数依次是接口名称，话题名称，qos
        self.timer_ = self.create_timer(5,self.time_callback)

    def time_callback(self,):
        if self.novel_queue.qsize() > 0 :
            #发布
            msg = String()
            msg.data = self.novel_queue.get()
            self.novel_pub.publish(msg)
            self.get_logger().info(f'发布了一行小说： {msg.data}')
    def download(self,url:str):
        response=requests.get(url)
        response.encoding='utf-8'
        self.get_logger().info(f'下载 {url} 完成')
        for line in response.text.splitlines():
            self.novel_queue.put(line)

def main():
    rclpy.init()
    node = NovelPubNode("novelpublisher")
    node.download("http://localhost:8000/novel1.txt")
    rclpy.spin(node)
    rclpy.shutdown()        
