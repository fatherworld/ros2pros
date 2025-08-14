#include<QApplication>
#include<QLabel>
#include<QString>
#include"rclcpp/rclcpp.hpp"
#include "status_interfaces/msg/system_status.hpp"
using namespace std;
using SystemStatus = status_interfaces::msg::SystemStatus;
class StatusDisplay:public rclcpp::Node
{
public:
    explicit StatusDisplay(string nodename):rclcpp::Node(nodename)
    {
        sub = this->create_subscription<SystemStatus>("sys_status",10,[&](const SystemStatus::SharedPtr msg) -> void
    {
        label_->setText(get_qstr_form_msg(msg));
    });
        label_ = new QLabel(get_qstr_form_msg(std::make_shared<SystemStatus>()));
        label_->show();
    }

    QString get_qstr_form_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str<< "=============== 系统状态可视化显示工具 =============== \n";
        show_str<< "数据时间：\t" <<msg->stamp.sec <<"\ts\n";
         show_str<< "数据时间：\t" <<msg->stamp.sec <<"\ts\n";
         show_str<< "用户名：\t" <<msg->hostname <<"\ts\n";
          show_str<< "cpu使用率：\t" <<msg->cpu_percent <<"\ts\n";
           show_str<< "内存使用率：\t" <<msg->memory_percent<<"\ts\n";
           show_str<< "内存总大小：\t" <<msg->memory_total <<"\ts\n";
            show_str<< "剩余有效内存：\t" <<msg->memory_avaliable<<"\ts\n";
          show_str<< "网络发送量:\t" <<msg->net_sent <<"\ts\n";
           show_str << "网络接受量：\t" <<msg->net_recv<<"\ts\n";
            show_str<< "===================================================";
        return QString::fromStdString(show_str.str());
    }
    

private:
    rclcpp::Subscription<SystemStatus>::SharedPtr sub;
    QLabel* label_;
};

int main(int argc,char*argv[])
{
    rclcpp::init(argc,argv);
    QApplication app(argc,argv);
    auto node = std::make_shared<StatusDisplay>("StatusDisplay");
    std::thread spin_thread([&]() -> void
{
    rclcpp::spin(node);
});
    spin_thread.detach();
    app.exec();
    rclcpp::shutdown();
    return 0;
}

