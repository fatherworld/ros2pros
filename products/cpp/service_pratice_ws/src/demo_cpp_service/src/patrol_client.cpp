#include <cstdlib>
#include <ctime>
#include "rclcpp/rclcpp.hpp"
#include "chapt4_interfaces/srv/patrol.hpp"
#include <chrono> //引入时间相关头文件
using namespace std::chrono_literals; // 使用时间单位的字面量
using namespace std;
using Patrol = chapt4_interfaces::srv::Patrol;
class PatrolClient:public rclcpp::Node{
public:
    PatrolClient(string nodename):rclcpp::Node(nodename)
    {
        patrol_client = this->create_client<Patrol>("patrol");
        timer_ = this->create_wall_timer(10s,std::bind(&PatrolClient::timer_callback,this));
        srand(time(NULL)); //初始化随机数种子，使用当前时间作为种子
    }

    void timer_callback()
    {
        //TODO 生成随机目标点，请求服务端
        //1.等待服务上线
        while(!patrol_client->wait_for_service(std::chrono::seconds(1)))
        {
            //等待时间检测rclcpp的状态
            if(!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(),"等待服务的过程中被打断 .....");
                return ;
            }
            RCLCPP_INFO(this->get_logger(),"等待服务上线中 .....");
        }

        //2.构造请求的对象
        auto request = std::make_shared<Patrol::Request>();
        request->target_x = rand()%15;
        request->target_y = rand()%15;
        RCLCPP_INFO(this->get_logger(),"请求巡逻：{%f,%f}.....",request->target_x,request->target_y);

        //发送异步请求，然后等待返回，返回时候调用回调函数
        patrol_client->async_send_request(
            request,
            [&](rclcpp::Client<Patrol>::SharedFuture result_future) -> void
            {
                auto response = result_future.get();
                if(response->result == Patrol::Response::SUCESS)
                {
                    RCLCPP_INFO(this->get_logger(),"目标点设置成功");
                }
                else if(response->result == Patrol::Response::FAIL)
                {
                    RCLCPP_INFO(this->get_logger(),"目标处理失败");
                }
            }
        );
    }

private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<Patrol>::SharedPtr patrol_client;
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node=std::make_shared<PatrolClient>("turtle_client");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
