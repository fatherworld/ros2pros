#include"rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <string>
#include <unistd.h>
using namespace std;
class TurtleControl:public rclcpp::Node
{
public:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_pub;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr velocity_sub;
    TurtleControl(string nodename):Node(nodename)
    {
        velocity_pub = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);
        velocity_sub = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose",10,std::bind(&TurtleControl::on_pose_received,this,std::placeholders::_1));

    }
    void on_pose_received(const turtlesim::msg::Pose::SharedPtr pose)
    {
        auto msg = geometry_msgs::msg::Twist();
        //记录当前位置
        double current_x = pose->x;
        double current_y = pose->y;

        double dis = std::sqrt((target_x-current_x)*(target_x-current_x) + (target_y-current_y)*(target_y-current_y));
        double angle = std::atan2(target_y-current_y,target_x-current_x) - pose->theta;

        std::cout<<"dis:"<<dis<<"-------"<<"angle:"<<angle<<std::endl;
        
        if(dis > 0.1)
        {
            //先计算角度，如果与目标的角度大于0.2，那么先调整与目标的方向角
            if(fabs(angle) > 0.2)
            {
                msg.angular.z = fabs(angle);
            }
            else
            {
                msg.linear.x = k_*dis;
            }
        }
        //如果距离小于0.1,那么停止前进，停在那里
        std::cout<<"msg.linear.x:"<<msg.linear.x<<endl;
        sleep(0.001);
        //限制最大值并发布消息
        if(msg.linear.x > max_speed)
        {
            msg.linear.x = max_speed;
        }
        
        velocity_pub->publish(msg);
    }
private:
    double target_x{1.0};
    double target_y{1.0};
    double k_{1.0};
    double max_speed{3.0}; //最大线速度
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node=std::make_shared<TurtleControl>("turtle_control");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}