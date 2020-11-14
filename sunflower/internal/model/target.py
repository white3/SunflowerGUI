class Target:
    def __init__(self, tid=None, name="test", isInherent=True, hourAngle=0.0, declination = 0.0, rightAscension = 0.0):
        """

        :param tid: 目标id号
        :param name: 目标名称
        :param isInherent: 目标是否在内置星图
        :param hourAngle: 目标时角
        :param declination: 目标赤纬
        :param rightAscension: 目标赤经
        """
        self.tid = tid
        self.name = name
        self.hourAngle = hourAngle
        self.declination = declination
        self.rightAscension = rightAscension
        self.isInherent = isInherent

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return f"不存在{item}属性"


    def __str__(self):
        return "{ name:'%s', hourAngle:'%f', declination:'%f', rightAscension:'%f', isInherent:'%s' }" % \
               (self.name, self.hourAngle, self.declination, self.rightAscension, self.isInherent)

if __name__ == '__main__':
    target = Target(name='sun')
    target.hourAngle = 0.1
    target.declination = 1.1
    target.rightAscension = 2.1
    target.isInherent = False

    print(target)