#include<memory>
#include "rclcpp/rclcpp.hpp"
#include"tf2_ros/transform_broadcaster.h"
#include"geometry_msgs/msg/transform_stamped.hpp"  //提供消息接口
#include"tf2/LinearMath/Quaternion.h"              
#include <chrono>
#include <math.h>
#include "tf2/utils.h"                              //提供tf2::getEluerYRP函数
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"    //提供消息类型转换函数

using namespace std::chrono_literals;

class TFListener:public rclcpp::Node
{
    public:     
        TFListener():Node("tf_listener")
        {
            RCLCPP_INFO(this->get_logger(),"bayes坐标转换订阅节点创建");
            tf_buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
            tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
            timer_ = create_wall_timer(1s,std::bind(&TFListener::get_transform,this));
        }
    private:
        std::shared_ptr<tf2_ros::Buffer> tf_buffer_;    
        std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
        rclcpp::TimerBase::SharedPtr timer_;
        void get_transform()
        {
            try
            {
                //lookupTransform是一个阻塞函数，会一直等待直到获取到坐标转换数据，最后两个参数表示从现在就开始查询，超时时间是1s
                geometry_msgs::msg::TransformStamped transform = tf_buffer_->lookupTransform("base_link1","target_point",this->get_clock()->now(),
            rclcpp::Duration::from_seconds(1.0));
                //tf2::Quaternion q(transform.transform.rotation.x,transform.transform.rotation.y,transform.transform.rotation.z,transform.transform.rotation.w);
                //将获得的TransformStamped接口的四元数转换成线速度和欧拉角roll,pitch,yaw
                const auto &translation = transform.transform.translation;
                const auto& rotation = transform.transform.rotation;
                double roll,pitch,yaw;
                tf2::getEulerYPR(rotation,yaw,pitch,roll);
                RCLCPP_INFO(this->get_logger(),"获取坐标转换成功，位姿为：(%f,%f,%f),欧拉角为：(%f,%f,%f)",translation.x,translation.y,translation.z,roll,pitch,yaw);
            }
            catch(tf2::TransformException &ex)
            {
                RCLCPP_ERROR(this->get_logger(),"获取坐标转换失败，原因：%s",ex.what());
            }
        }
};
int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<TFListener>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
