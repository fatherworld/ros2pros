import rclpy
from rclpy.node import Node
class PersonNode(Node):
    def __init__(self,name:str,age:int):
        super().__init__(name)
        self.name = name
        self.age = age
    
    def eat(self,foodname:str):
        print(f'我是 {self.name},今年{self.age} 岁，喜欢吃{foodname}')

def main():
    rclpy.init()
    node = PersonNode('bayes',30)
    node.eat("尖椒肉丝")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    
    main()