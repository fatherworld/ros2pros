import face_recognition
import cv2
import rclpy
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,ParameterType,ParameterValue
from chapt4_interfaces.srv import FaceDetector
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
import time
from cv_bridge import CvBridge #用于格式转换(opencv图像个数转换ros2的image)
class FaceDetectorClient(Node):
    def __init__(self,nodename):
        print("111111111111")
        #print(f"nodename:{nodename}")
        super().__init__(nodename)
        #print(nodename)
        self.client = self.create_client(FaceDetector,'/face_detect')
        print(self.client)
        self.bridge = CvBridge()
        self.test1_image_test=get_package_share_directory("demo_python_service") + "/resources/test1.jpeg"
        self.img1 = cv2.imread(self.test1_image_test)
        self.detectfinished=False
    def send_request(self,):
        #TODO：发送请求并进行处理
        #判断服务是否在线
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f'等待服务上线 ...')
        
        #构造 Request
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.img1)

        #发送异步请求
        future = self.client.call_async(request)
        print("异步请求发送识别")
        def request_callback(result_future):
            response = result_future.result()
            self.detectfinished = True
            self.get_logger().info('f 识别结束')
            #self.show_face_location(response)
        future.add_done_callback(request_callback)
        return
    
    def call_set_parameters(self,parameters):
        client = self.create_client(SetParameters,'/face_detect_node/set_parameters')
        while client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f'等待参数设置服务上线 ...')

        #创建请求对象
        request = SetParameters.Request()
        request.parameters = parameters

        #异步调用，等待并返回响应结果
        future = client.call_async(request)
        def request_callback(result_future):
            response = result_future.result()
            for result in response.results:
                if result.successful:
                    self.get_logger().info(f'参数 face_location_model 设置完成')
                else:
                    self.get_logger().info(f'参数 face_location_model 设置失败，原因为 {result.reason}')

            #self.get_logger().info('f 识别结束')
            #self.show_face_location(response)
        future.add_done_callback(request_callback)

    def update_detect_mode(self,model):
        param=Parameter()
        param.name="face_location_model"
        paramvalue=ParameterValue()
        paramvalue.type=ParameterType.PARAMETER_STRING
        paramvalue.string_value=model
        param.value=paramvalue
        self.call_set_parameters([param])


    def show_face_location(self,response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.img1,(left,top),(right,bottom),(255,0,0),4)
        cv2.imshow('Face_Detector',self.img1)
        cv2.waitKey(0)

def main():
    try:
        rclpy.init()
        node = FaceDetectorClient("FaceClientNode")
    except Exception as e:
        print(f"节点创建失败: {e}")
        return
    node.get_logger().info(f"开始修改识别网络模型参数")
    node.update_detect_mode('cnn')
    node.get_logger().info(f"再次发送识别请求")
    node.send_request()

    time.sleep(1)
    node.get_logger().info(f"开始修改识别网络模型参数")
    while not node.detectfinished:
        continue
    node.update_detect_mode('hog')
    node.detectfinished = False
    node.get_logger().info(f"再次发送识别请求")
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdonw()