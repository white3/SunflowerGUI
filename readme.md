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
communicator_ucas4_5.py		ucas4.5通信类
config.py					配置文件管理类
control.py					控制层
favicon.ico					ucas图标
service.py					服务层
window.py					GUI类
window2.py					debug GUI类
```



## 交互层

```python
    def setupAction(self, Form, flower):
        self.__setLCDNumberUI(self.haLcdNumber)
        self.__setLCDNumberUI(self.decLcdNumber)
        self.__setLCDNumberUI(self.RALcdNumber)

        # self.OriComboBox
        self.oriComboBox.addItem("CW")
        self.oriComboBox.addItem("CCW")
        self.oriComboBox.addItem("UP")
        self.oriComboBox.addItem("DOWN")
        self.oriComboBox.currentIndexChanged.connect(self.getSpeedAndOriValue)

        # self.speedSpinBox
        self.speedSpinBox.setValue(1)
        self.speedSpinBox.setMaximum(3)
        self.speedSpinBox.setMinimum(1)

        # self.
        self.haLcdNumber.setDigitCount(6)

        # self.moveButton.clicked.connect(flower.moveButton)
        self.traceButton.clicked.connect(flower.traceStar)
        self.stopButton.clicked.connect(flower.stopTrace)
        self.resetButton.clicked.connect(flower.resetTelescope)
        self.positionButton.clicked.connect(flower.getStarPosition)
        self.debugButton.clicked.connect(flower.connectTelescope)
```





## 控制层

```python

class control:
    def __init__(self, config):
        self.__sunflower = service(config=config)
        self.isTracing = threading.Condition()  # a global lock to control the thread of tracing the Sun
        self.traceFlag = True  # a signal
        self.traceThread = threading.Thread(target=self.traceStar, daemon=True)
        self.traceThread.start()

    def traceStar(self):
        self.traceFlag = False
        self.isTracing.acquire()
        self.isTracing.notify()
        self.isTracing.release()

    def stopTrace(self):
        self.traceFlag = True
        self.__sunflower.stopTelescope()

    def resetTelescope(self):
        self.traceFlag = True
        self.__sunflower.resetTelescope()

    def telescopePosition(self):
        self.__sunflower.getTelescopeLocation()

    def connectTelescope(self, comNumber):
        self.__sunflower.setCOM(comNumber)
        self.__sunflower.connectTelescope()

    def disconnectTelescope(self):
        self.__sunflower.disconnectTelescope()

    def changeMoveConfig(self, speed, ori):
        self.__sunflower.commdSpwOr(speed, ori)

    def getTelescopeLocation(self):
        self.__sunflower.getStarPosition()

    def getInnerStarsList(self):
        self.__sunflower.getInnerStarsList()

    def getStarPosition(self):
        self.__sunflower.getStarPosition()
```





## 服务层

```python
class service:
    def __init__(self, config):
        '''
        初始化 星体坐标计算对象、配置加载对象, 望远镜通信对象置空(在望远镜连接时初始化)
        :param config:
        '''

    def connectTelescope(self):
        '''
        初始化串口通信对象, 再通过该对象发送上电指令连接
        :return:
        '''

    def disconnectTelescope(self):
        '''
        断开望远镜, 并发送断电指令
        :return:
        '''

    def traceStar(self):
        '''
        望远镜追踪星体
        :return:
        '''

    def stopTelescope(self):
        '''
        望远镜停止转动
        :return:
        '''

    def resetTelescope(self):
        '''
        重置望远镜视角
        :return:
        '''

    def setStar(self, star):
        '''
        通过内置星体设置坐标
        :param star: planets[star]
        :return:
        '''

    def setStar(self, rightAscension, declination):
        '''
        设置被观测星体的坐标
        :param rightAscension:
        :param declination:
        :return:
        '''

    def commdSpwOr(self, speed, orient):
        '''
        配置望远镜转速和驱动模式
        :param speed:
        :param orient:
        :return:
        '''

    def getInnerStarsList(self):
        '''
        :return: {
                    0: ['SOLAR_SYSTEM_BARYCENTER', 'SSB', 'SOLAR SYSTEM BARYCENTER'],
                    1: ['MERCURY_BARYCENTER', 'MERCURY BARYCENTER'],
                    2: ['VENUS_BARYCENTER', 'VENUS BARYCENTER'],
                    3: ['EARTH_BARYCENTER', 'EMB', 'EARTH MOON BARYCENTER', 'EARTH-MOON BARYCENTER', 'EARTH BARYCENTER'],
                    4: ['MARS_BARYCENTER', 'MARS BARYCENTER'],
                    5: ['JUPITER_BARYCENTER', 'JUPITER BARYCENTER'],
                    6: ['SATURN_BARYCENTER', 'SATURN BARYCENTER'],
                    7: ['URANUS_BARYCENTER', 'URANUS BARYCENTER'],
                    8: ['NEPTUNE_BARYCENTER', 'NEPTUNE BARYCENTER'],
                    9: ['PLUTO_BARYCENTER', 'PLUTO BARYCENTER'],
                    10: ['SUN'],
                    199: ['MERCURY'],
                    299: ['VENUS'],
                    399: ['EARTH'],
                    301: ['MOON'],
                    499: ['MARS']
                }
        '''

    def getStarPosition(self):
        '''
        获取观测星体的坐标
        :return: [Right ascension, Declination]
        '''

    def getTelescopeLocation(self):
        '''
        返回已配置的 望远镜坐标
        :return:
        '''

    def setTelescopeLocation(self, lon, lat, elevation):
        '''
        设置望远镜所在坐标
        :param lon: 经度
        :param lat: 纬度
        :param elevation: 海拔
        :return:
        '''

    def setCOM(self, comNumber):
        '''
        设置串口
        :param comNumber: 串口号
        :return:
        '''
```



## 操作层



### 通信类

```python
class communicator_ucas4_5():    
    def __init__(self, comNumber):
        '''
        配置串口.
        :param comNumber: 串口号
        :return:
        '''
        
    def __del__(self):
        '''
        发送急停后, 再发送断电指令, 并断开连接
        '''
        
	def isConnect(self):
        '''
        返回本机COM口连接状态
        '''

    def disconnect(self):
        '''
        发送断电指令, 并断开与电机的连接
        '''

    def connect(self):
        '''
        发送上电指令, 并保持与电机的连接
        '''

    def reset(self):
        '''
        望远镜视向置为 1,1
        :return:
        '''

    def getPosition(self, isDisp=True):
        '''
        :param isDisp: 是否通过print输出
        :return: Hourangle, declination
        '''

    def stop(self):
        '''
        发送急停指令
        '''

    def trace(self, ha, dec):
        '''
        追踪ha、dec地址
        '''
```



### 计算类

```python
class calculator:
    def __init__(self, lat, lon, elevation, innerStarConfig, observer='earth', star='sun'):
        '''
        innerStarConfig的格式为 [True/False, [Right ascension, Declination]]，True表示使用指定的[RA, DEC]进行追踪，
        False表示使用 sky 库支持的天体追踪

        :param lat: 纬度
        :param lon: 经度
        :param elevation: 海拔
        :param innerStarConfig: innerStarConfig = [True/False, [Right ascension, Declination]]
        :param observer: 观察者所在位置
        :param star: 观测的星
        :return:
        '''

    def setLongitude(self, lon):
        '''

        :param lon: 经度
        '''

    def setLatitude(self, lat):
        '''

        :param lat: 维度
        '''

    def setElevation(self, elevation):
        '''

        :param elevation: 海拔
        '''

    def getStarPosition(self):
        '''
        获取当前所追的星的位置
        '''

    def setStar(self, RA, DEC):
        '''
        设置星提所在的赤经和赤纬

        :param RA: 赤经
        :param DEC: 赤纬
        '''

    def setStar(self, star):
        '''
        通过支持列表设置星体

        :param star: 
        '''
        
    def getStarList(self):
        '''
        返回支持直接获得跟踪坐标的星体列表
        '''

    def compute(self):
        '''
        计算当前指定星体的坐标

        :return: HaDegree 高度, Declination 赤纬
        '''
```



### 配置类

```python
class config:
    def __init__(self, configFilePath=".config.ini"):
        '''
        对象消除时会自动调用写文件保存

        :param configFilePath: 配置文件路径
        '''

    def getValue(self, key):
        '''
        获取配置中属性名 key 对应的键值.

        :param key: 配置文件的属性名
        :return:
        '''

    def setValue(self, key, value):
        '''
        将配置中属性名 key 对应的键值修改为 value.

        :param key: 属性名称
        :param value: 属性值
        :return:
        '''

    def checkConfig(self, filePath):
        # TODO make config check.

    def readConfig(self):
        '''
        读取配置文件, 如果配置文件不存在或非法, 将自动导入模板并创建文件
        '''

    def saveConfig(self):
        '''
        保存到默认源文件.

        :return:
        '''
        
    def saveConfig(self, filePath='config.ini'):
        '''
        保存配置文件至指定文件路径
        :param filePath: 文件路径
        :return:
        '''
```

