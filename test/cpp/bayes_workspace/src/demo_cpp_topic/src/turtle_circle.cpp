#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <chrono>
//使用时间单位的字面量，可以在代码中使用s和ms表示时间
using namespace std;
using namespace std::chrono_literals;
class TurtleCircle:public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; //发布者智能指针
public:
    explicit TurtleCircle(string nodename):Node(nodename)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);

        //调用继承而来的弗雷函数创建定时器
        timer_ = this->create_wall_timer(1000ms,std::bind(&TurtleCircle::callback,this));

    }
    void callback()
    {
       auto msg = geometry_msgs::msg::Twist();
       msg.linear.x = 1.0; //每秒1m
       msg.angular.y = 0.5; //每秒0.5度
       publisher_->publish(msg);
    }
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<TurtleCircle>("turtel_circle");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
