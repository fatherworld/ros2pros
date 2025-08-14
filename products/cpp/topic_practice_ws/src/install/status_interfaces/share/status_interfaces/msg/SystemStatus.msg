builtin_interfaces/Time stamp #记录时间
string hostname
float32 cpu_percent
float32 memory_percent
float32 memory_total
float32 memory_avaliable
float64 net_sent
float64 net_recv

#定义好消息接口文件之后，需要在CMakeLists文件中完成注册，添加 builtin_interfaces依赖