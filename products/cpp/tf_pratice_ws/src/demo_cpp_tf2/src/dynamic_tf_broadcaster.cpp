#include<memory>
#include "rclcpp/rclcpp.hpp"
#include"tf2_ros/transform_broadcaster.h"
#include"geometry_msgs/msg/transform_stamped.hpp"
#include"tf2/LinearMath/Quaternion.h"
#include "tf2/convert.hpp"
#include <chrono>
#include <math.h>
using namespace std::chrono_literals;

class DynamicTFBroadcaster:public rclcpp::Node
{
    public:
        DynamicTFBroadcaster():Node("dynamic_tf_broadcaster")
        {
            RCLCPP_INFO(this->get_logger(),"动态坐标转换发布节点创建");
            broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
            timer_ = create_wall_timer(10ms,std::bind(&DynamicTFBroadcaster::publish_tf,this));
        }
    private:
        //静态的变换只需要发布一次，因为ROS2会为订阅者保留数据，当出现新的订阅者的时候，可以直接获取到保留的数据
        std::shared_ptr<tf2_ros::TransformBroadcaster> broadcaster_;
        rclcpp::TimerBase::SharedPtr timer_;
        void publish_tf()
        {
            geometry_msgs::msg::TransformStamped transform;
            transform.header.stamp = this->get_clock()->now();
            transform.header.frame_id = "map";
            transform.child_frame_id = "base_link1";
            transform.transform.translation.x = 2.0;
            transform.transform.translation.y = 3.0;
            transform.transform.translation.z = 0.0;
            tf2::Quaternion q;
            q.setRPY(0,0,30/180.0*M_PI);
            //transform.transform.rotation = tf2::toMsg(q);
            transform.transform.rotation.x = q.getX();
            transform.transform.rotation.y = q.getY();
            transform.transform.rotation.z = q.getZ();
            transform.transform.rotation.w = q.getW();
            broadcaster_->sendTransform(transform);
        }
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<DynamicTFBroadcaster>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

