# core 更新记录

4.5m控制软件的核心模块文件夹



## v0.1 2020-11-14 17:24:06

- 添加calculator.py
  - class Calculator(object)
    - `__init__(self, lat:str, lon:str, elevation:int, target:Target, observer='earth')` 
    - computeLocation(self)
    - setTarget(self, target)
  - 用于Target对象的坐标计算操作
- 添加communicator.py
  - 用于封装与telescope通信的具体操作
- 添加window.py
  - 用于封装GUI与业务操作的绑定
- 添加window_ui.py
  - 用于封装GUI设计
- 添加recorder.py
  - class Recorder(object)
    - `__init__(self)`
    - readData(self, scale=[-180, 180], kind=HA)
    - writeData(self, haOffset: HAOffset, decOffset: DECOffset, globalClock: Times, target: Target)
  - 用于封装误差记录器功能
- 添加viewer.py
  - class View(object)
    - `__init__(self, target: Target, config: Config)`
      - 初始化需要配置文件，还需要观测目标
    - getViewData(self)
  - 用于封装视图模块的功能
- 添加corrector.py
  - class Corrector(object)
    - `__init__(self, recorder: Recorder)`
      - 初始化需要一个Recorder，用于读取误差数据库数据
    - changeMod(self, fitmod)
      - 改变拟合模式
    - update(self)
      - 更新拟合数据
    - fitHa(self, ha)，ha_offset 
      - 获取ha指定的修正值
    - fitDec(self, dec)，dec_offset 
      - 获取dec指定的修正值
    - show(self)
      - 绘画拟合后的数据
  - 主要用处
    - 用于封装修正模块的功能
- 添加config.py
  - class Config
    - `__init__(self, configFilePath="config.ini")`
    - getValue(self, section, option)，key
      - 返回section下option的值
    - setValue(self, section, option, value)
      - 设置section下option的值
  - 用于封装配置模块的功能
- 添加constant.py
  - 用于声明全局使用的Constant对象