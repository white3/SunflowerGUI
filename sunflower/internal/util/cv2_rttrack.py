# coding=utf-8
# 导入python包
import numpy as np
import cv2
import time

def active_offset():
    cap = cv2.VideoCapture(1)
    cap.set(3, 1280)  # 设置帧宽
    cap.set(4, 720)  # 设置帧高
    # font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
    # kernel = np.ones((5, 5), np.uint8)  # 卷积核
    args = {'image': 'res/cv3.jpg', 'radius': 11}

    if cap.isOpened() is True:  # 检查摄像头是否正常启动
        while (True):
            ret, image = cap.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰色通道

            #  消除噪声
            gray = cv2.GaussianBlur(gray, ksize=(args["radius"], args["radius"]), sigmaX=0)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
            cv2.circle(image, maxLoc, args["radius"], (255, 0, 0), 2)
            center = [len(image[0]) / 2, len(image) / 2]
            offset = [center[0] - maxLoc[0], center[1] - maxLoc[1], ]

            print("minVal: %s, maxVal: %s, minLoc: %s, maxLoc: %s" % (minVal, maxVal, minLoc, maxLoc))
            print("center: %s" % center)
            print("需右移 x_offset: %s, 需上移 y_offset: %s" % (offset[0], offset[1]))

            # result = np.hstack([orig, image, image])
            cv2.imshow('Robust', image)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
            time.sleep(0.1)
        cap.release()
        cv2.destroyAllWindows()
    else:
        print('cap is not opened!')


if __name__ == '__main__':
    active_offset()
