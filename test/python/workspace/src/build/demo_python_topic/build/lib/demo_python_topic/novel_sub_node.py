import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import time
import espeakng
from threading import Thread
class NovelSubNode(Node):
    def __init__(self,nodename):
        super().__init__(nodename)
        self.novelque=Queue()
        #print('11111111111111111111')
        self.novelsub=self.create_subscription(String,'novel',self.sub_callback,10)
        #print('22222222222222222222')
        self.speech_thread = Thread(target=self.speech_thread)
        self.speech_thread.start()
    
    def sub_callback(self,msg):
        self.novelque.put(msg.data)

    def speech_thread(self,):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'
        while rclpy.ok():
            #print(f'队列的的长度是:{self.novelque.qsize}')
            if self.novelque.qsize()>0:
                txt = self.novelque.get()
                self.get_logger().info(f'正在朗读 {txt}')
                speaker.say(txt)
                speaker.wait()
            else:
                time.sleep(1)

def main():
    rclpy.init()
    node = NovelSubNode("novelsubnode")
    rclpy.spin(node)
    rclpy.shutdown()