#include "PersonNode.h"
class WriteNode:public PersonNode
{
    public:
    WriteNode(string name,int age):PersonNode(name,age)
    {

    }

    virtual void eatfood(string foodname)
    {
        //std::cout<<"111111"<<name<<endl;
    }
    virtual ~WriteNode()
    {

    }
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<WriteNode>("bayes0",30);
    node->eatfood("尖椒肉丝");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 1;
}