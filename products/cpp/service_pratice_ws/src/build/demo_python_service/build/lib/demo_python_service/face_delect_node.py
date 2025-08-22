import face_recognition
import cv2
import rclpy
from chapt4_interfaces.srv import FaceDetector
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
import time
from cv_bridge import CvBridge #用于格式转换(opencv图像个数转换ros2的image)
class faceDetectNode(Node):
    def __init__(self,nodename):
        super().__init__(nodename)
        self.bridge=CvBridge()
        self.service=self.create_service(FaceDetector,'/face_detect',self.detect_face_callback)
        self.default_image_path=get_package_share_directory('demo_python_service') + "/resources/test.jpg"
        self.upsample_time = 1
        self.model = "hog"

    def detect_face_callback(self,request,reponse):
        if request.image.data:
            cv_img = self.bridge.imgmsg_to_cv2(request.image)   #将图像消息接口格式转换成opencv的格式
        else:
            cv_img = cv2.imread(self.default_image_path)
        starttime = time.time()
        self.get_logger().info(f'开始识别')
        face_locations = face_recognition.face_locations(cv_img,self.upsample_time,self.model)


        endtime = time.time()
        self.get_logger().info(f'识别完成! 耗时{endtime-starttime}')
        reponse.number = len(face_locations)
        reponse.use_time = endtime-starttime
        for up,right,down,left in face_locations:
            reponse.top.append(up)
            reponse.right.append(right)
            reponse.bottom.append(down)
            reponse.left.append(left)

        #完成人脸检测功能
        return reponse
'''
sensor_msgs/Image image #原始图像
---
int16 number #人脸个数
float32 use_time #识别耗时
int32[] top     #人脸在图像中的位置
int32[] right
int32[] bottom
int32[] left
'''

def main():
    rclpy.init()
    node=faceDetectNode("face_detect_node")
    rclpy.spin(node)
    rclpy.shutdown()