#include<QApplication>
#include<QLabel>
#include<QString>
int main(int argc,char* argv[])
{
    QApplication app(argc,argv);
    QLabel* label = new QLabel();
    QString msg = QString::fromStdString("Hello Qt!");
    label->setText(msg);
    label->show();
    app.exec(); //类似于rclcpp::spin(),在方法内不断循环处理事件，阻塞程序继续往下面运行
    return 0;
}