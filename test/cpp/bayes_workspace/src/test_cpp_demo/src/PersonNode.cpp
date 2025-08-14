#include "PersonNode.h"

PersonNode::PersonNode(string name,int age):Node(name)
{
    this->age = age;
    this->name = name;
}

void PersonNode::eatfood(string foodname)
{
    RCLCPP_INFO(this->get_logger(),"哦我是 %s,今年%d 岁，我现在吃 %s",name.c_str(),age,foodname.c_str());
}
PersonNode::~PersonNode()
{

}

// int main(int argc,char** argv)
// {
//     rclcpp::init(argc,argv);
//     auto node = std::make_shared<PersonNode>("bayes0",30);
//     node->eatfood("尖椒肉丝");
//     rclcpp::spin(node);
//     rclcpp::shutdown();
//     return 1;
// }