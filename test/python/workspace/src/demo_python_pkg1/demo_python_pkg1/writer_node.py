import rclpy
from rclpy.node import Node
from demo_python_pkg.person_node import PersonNode
class WriteNode(PersonNode):
    def __init__(self,book:str,name:str,age:int) -> None:
        print(f'WriteNode 的 init方法被调用了')
        super().__init__(name,age)
        self.book = book
    
def main():
    rclpy.init()
    node = WriteNode("张三自传","bayeswrite",31)
    node.eat("鱼香肉丝")
    rclpy.spin(node)
    rclpy.shutdown()