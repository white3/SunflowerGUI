# model 更新记录

4.5m控制软件的基本数据结构文件夹



## v0.1 2020-11-14 16:48:12

- 添加times.py文件
  - class Times(object)
    - toUTC
    - toLocalTime
    - toLST
  - 主要用处
    - 时钟数据对象
    - 主程序中的全局时钟对象
    - 给误差标记时间，未来可给星图中的新加目标标记时间
- 添加target.py
  - class Target(object)
    - name
    - hourAngle
    - declination
    - rightAscension
    - isInherent
  - 主要用处
    - 观测数据对象
    - 主程序中的望远镜当前指向的坐标、目标的坐标
    - 用于误差记录时，同时记录观测对象，可用于未来误差数据分析
- 添加offset.py
  - class Offset(object)，class Offset(object)
    - `__add__`
    - `__init__`
    - `__getattr__`
  - 主要用处
    - 误差数据对象
    - 考虑到未来更大粒度的误差修正，这里将时角、赤纬分开