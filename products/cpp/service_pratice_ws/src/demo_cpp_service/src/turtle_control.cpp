#include "chapt4_interfaces/srv/patrol.hpp"
#include"rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"
#include <string>
#include <unistd.h>
using namespace chapt4_interfaces::srv;
using namespace std;
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;
class TurtleContorller:public rclcpp::Node
{
public:
   TurtleContorller(string nodename):rclcpp::Node(nodename)
    {
        //声明和初始化参数
        this->declare_parameter("k",1.0);
        this->declare_parameter("max_speed",1.0); 
        this->get_parameter("k",k_);
        this->get_parameter("max_speed",max_speed);
        
        velocity_pub = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);
        velocity_sub = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose",10,std::bind(&TurtleContorller::on_pose_received,this,std::placeholders::_1));
        //创建服务
        patrol_ser = this->create_service<Patrol>(
            "patrol",[&](const std::shared_ptr<Patrol::Request> request,std::shared_ptr<Patrol::Response> response) -> void {
                //判断逻辑节点是否在模拟器边界内部
                if(0 > request->target_x || 0>request->target_y || request->target_x>12.0f  || request->target_y >12.0f )
                {
                    response->result = Patrol::Response::FAIL;
                }
                else
                {
                    target_x = request->target_x;
                    target_y = request->target_y;
                    response->result = Patrol::Response::SUCESS;
                }
            }
        );


        //添加参数设置回调
        parameters_callback_handle_ = this->add_on_set_parameters_callback(
            [&](const std::vector<rclcpp::Parameter> & params) -> SetParametersResult{

                //遍历参数
                for(auto param:params)
                {
                    RCLCPP_INFO(this->get_logger(),"更新参数 %s 值为 ：%f",param.get_name().c_str(),param.as_double());
                    if(param.get_name()=="k")
                    {
                        k_ = param.as_double();
                    }
                    else if(param.get_name()=="max_speed")
                    {
                        max_speed = param.as_double(); 
                    }
                }
                auto result = SetParametersResult();
                result.successful = true;
                return result;
            }
        );
    }
public:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_pub;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr velocity_sub;

    void on_pose_received(const turtlesim::msg::Pose::SharedPtr pose)
    {
        auto msg = geometry_msgs::msg::Twist();
        //记录当前位置
        double current_x = pose->x;
        double current_y = pose->y;

        double dis = std::sqrt((target_x-current_x)*(target_x-current_x) + (target_y-current_y)*(target_y-current_y));
        double angle = std::atan2(target_y-current_y,target_x-current_x) - pose->theta;

        RCLCPP_INFO(this->get_logger(),"参数k: %f, 参数max_speed ：%f",k_,max_speed);
        //std::cout<<"dis:"<<dis<<"-------"<<"angle:"<<angle<<std::endl;
        
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


private:
    rclcpp::Service<Patrol>::SharedPtr patrol_ser;

    OnSetParametersCallbackHandle::SharedPtr parameters_callback_handle_;
};

/*
float32 target_x
float32 target_y
---
int8 SUCESS = 1
int8 FAIL = 0
int8 result
*/

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node=std::make_shared<TurtleContorller>("turtle_control");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}