class Target:
    def __init__(self, name, isInherent=True):
        self.name = name
        self.hourAngle = 0
        self.declination = 0
        self.rightAscension = 0
        self.isInherent = isInherent

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