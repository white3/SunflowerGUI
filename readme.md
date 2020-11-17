
## 工作2020-11-16 15:45:58

串口控制    https://pythonhosted.org/pyserial/shortintro.html#configuring-ports-later

QList星表   https://blog.csdn.net/jia666666/article/details/81624550

状态信息自动滚动       https://stackoverflow.com/questions/7778726/autoscroll-pyqt-qtextwidget

关于导包问题  项目结构

关于测试问题  单元测试项目结构

总结时间    https://time.is/zh/UTC

## 工作2020-11-15 15:45:58

完成 wasd控制功能

完成 wasd与Correct叠加指向修正

完成 跟踪功能

完成 增加事件进行update拟合的map

！！Target模块——先来一个设置star

## 工作2020-11-14 15:45:58

完成 record   读写，已测试

完成 view     仪表，已测试

完成 correct  代码，未测试  —— 目前是一次读取全部数据，然后拟合出一个map，然后通过map修正指向

还需：

！！！wasd控制功能

！！！wasd与Correct叠加指向修正

！！！跟踪功能

！！Target模块——先来一个设置star

增加事件进行update拟合的map

## ease-version2

### correct

当用户使用 correct 模式时,存在的情况有

- 静默修正运行

- 运行时发现偏移，通过手动矫正

- 当用户摁下correct，变为off-correct后又立马摁下，此时存在并发问题——可能导致两个线程同时修正

- correct返回的值, 应该是一个

- 先将correct置为静态修正，不是一边指向一边拟合

### record

## ease-version

```
main.py                     主程序
calculator.py               计算模块
Communicator.py     通讯模块
config.py                   配置模块
recorder.py                 记录模块
Window.py                   交互模块
```

## 文件结构

```
Data						轨道数据
config.ini					配置文件
config.json					旧版本配置文件
main.py						主程序
ori_debugGUI.ui				debug GUI 设计文件
ori_debugTerminal.ui		debug terminal GUI设计文件
ori_main.ui					GUI设计文件
readme.md					参考文档
sunflower					代码包
```

sunflower包

```
calculator.py				位置计算类
Communicator.py		ucas4.5通信类
config.py					配置文件管理类
Control.py					控制层
favicon.ico					ucas图标
service.py					服务层
Window.py					GUI类
window2.py					debug GUI类
```

