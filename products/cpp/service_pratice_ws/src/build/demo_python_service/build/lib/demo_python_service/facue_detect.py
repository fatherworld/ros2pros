import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory






def main():
    #获取图片的真实路径
    default_img_path = get_package_share_directory('demo_python_service') + "/resources/test.jpg"

    img = cv2.imread(default_img_path)
    face_locations = face_recognition.face_locations(img,number_of_times_to_upsample=10,model='hog')

    for top,right,bottom,left in face_locations:
        cv2.rectangle(img,(left,top),(right,bottom),(255,0,0),4)
    cv2.imshow('Face_Detector',img)
    cv2.waitKey(0)
