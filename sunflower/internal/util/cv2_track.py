# coding=utf-8
# 导入python包
import numpy as np
import argparse
import cv2


# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", help = "path to the image file")
# ap.add_argument("-r", "--radius", type = int, help = "radius of Gaussian blur; must be odd")
# args = vars(ap.parse_args())

# 高斯噪声
# 语法：GaussianBlur（src，ksize，sigmaX [，dst [，sigmaY [，borderType]]]）-> dst
# ——src输入图像；图像可以具有任意数量的通道，这些通道可以独立处理，但深度应为CV_8U，CV_16U，CV_16S，CV_32F或CV_64F。
# ——dst输出图像的大小和类型与src相同。
# ——ksize高斯内核大小。 ksize.width和ksize.height可以不同，但它们都必须为正数和奇数，也可以为零，然后根据sigma计算得出。
# ——sigmaX X方向上的高斯核标准偏差。
# ——sigmaY Y方向上的高斯核标准差；如果sigmaY为零，则将其设置为等于sigmaX；
#           如果两个sigmas为零，则分别从ksize.width和ksize.height计算得出；
#           为了完全控制结果，而不管将来可能对所有这些语义进行的修改，建议指定所有ksize，sigmaX和sigmaY。

def compute_offset(args=None):
    # 构建并解析参数
    # 读取图片并将其转化为灰度图片
    if args is None:
        args = {'image': 'res/cv3.jpg', 'radius': 11}

    image = cv2.imread(args["image"])
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 利用cv2.minMaxLoc寻找到图像中最亮和最暗的点
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # 在图像中绘制结果
    cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)

    # 应用高斯模糊进行预处理
    gray = cv2.GaussianBlur(gray, ksize=(args["radius"], args["radius"]), sigmaX=0)

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    image1 = orig.copy()
    cv2.circle(image1, maxLoc, args["radius"], (255, 0, 0), 2)
    # cv2.circle(image1, minLoc, args["radius"], (255, 0, 0), 2)
    center = [len(image[0]) / 2, len(image) / 2]
    offset = [center[0] - maxLoc[0], center[1] - maxLoc[1], ]

    print("minVal: %s, maxVal: %s, minLoc: %s, maxLoc: %s" % (minVal, maxVal, minLoc, maxLoc))
    print("center: %s" % center)
    print("需右移 x_offset: %s, 需上移 y_offset: %s" % (offset[0], offset[1]))

    # 显示结果
    result = np.hstack([orig, image, image1])
    cv2.imwrite("region5.png", result)
    cv2.imshow("Robust", result)
    cv2.waitKey(0)


def active_offset():
    cap = cv2.VideoCapture(1)
    cap.set(3, 1280)  # 设置帧宽
    cap.set(4, 720)  # 设置帧高
    font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
    kernel = np.ones((5, 5), np.uint8)  # 卷积核

    if cap.isOpened() is True:  # 检查摄像头是否正常启动
        while (True):
            ret, frame = cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰色通道
            # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 转换为HSV空间

            lower_green = np.array([35, 50, 100])  # 设定绿色的阈值下限
            upper_green = np.array([77, 255, 255])  # 设定绿色的阈值上限
            #  消除噪声
            mask = cv2.inRange(hsv, lower_green, upper_green)  # 设定掩膜取值范围
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 形态学开运算
            bila = cv2.bilateralFilter(mask, 10, 200, 200)  # 双边滤波消除噪声
            edges = cv2.Canny(opening, 50, 100)  # 边缘识别

            # 识别圆形
            circles = cv2.HoughCircles(
                edges, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=10, minRadius=10, maxRadius=500)
            if circles is not None:  # 如果识别出圆
                for circle in circles[0]:
                    #  获取圆的坐标与半径
                    x = int(circle[0])
                    y = int(circle[1])
                    r = int(circle[2])
                    cv2.circle(frame, (x, y), r, (0, 0, 255), 3)  # 标记圆
                    cv2.circle(frame, (x, y), 3, (255, 255, 0), -1)  # 标记圆心
                    text = 'x:  ' + str(x) + ' y:  ' + str(y)
                    cv2.putText(frame, text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)  # 显示圆心位置
            else:
                # 如果识别不出，显示圆心不存在
                cv2.putText(frame, 'x: None y: None', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)
            cv2.imshow('frame', frame)
            cv2.imshow('mask', mask)
            cv2.imshow('edges', edges)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print('cap is not opened!')


if __name__ == '__main__':
    active_offset()
