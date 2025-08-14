#include "rclcpp/rclcpp.hpp"
#include <string>
using namespace std;
class PersonNode:public rclcpp::Node
{
public:
    PersonNode(string name,int age);
    virtual void eatfood(string foodname);
    string name;
    virtual ~PersonNode();
    int age;
};