#include "PersonNode.h"
int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<PersonNode>("bayes0",30);
    node->eatfood("尖椒肉丝");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 1;
}