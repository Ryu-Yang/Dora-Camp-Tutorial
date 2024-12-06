# 本代码来自于网络。对于原文代码更改如下：加入Dora节点、加入误差求解、while循环替换为遍历dora节点的事件
# 原文链接https://blog.51cto.com/u_13544/11102518。

import os
import numpy as np
import pyarrow as pa
import cv2
from dora import Node


os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


#定义一个形态学处理的函数
def good_thresh_img(img):
    gs_frame = cv2.GaussianBlur(img, (5, 5), 0)                     #高斯滤波
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)                 # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)
    return erode_hsv

#定义一个识别目标颜色并处理的函数
def select_color_img(target_color,img):
        for i in target_color:
            mask=cv2.inRange(erode_hsv,color_dist[i]['Lower'],color_dist[i]['Upper'])
            if(i==target_color[0]):
                inRange_hsv=cv2.bitwise_and(erode_hsv,erode_hsv,mask = mask)
            else:
                inRange_hsv1=cv2.bitwise_and(erode_hsv,erode_hsv,mask = mask)
                inRange_hsv=cv2.add(inRange_hsv,inRange_hsv1)
        return  inRange_hsv

#定义一个提取轮廓的函数
def extract_contour(img):
    inRange_gray = cv2.cvtColor(final_inRange_hsv,cv2.COLOR_BGR2GRAY)
    contours,hierarchy = cv2.findContours(inRange_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    return contours
    
#定义一个寻找目标并绘制外接矩形的函数
def find_target(contours,draw_img):
    for c in contours:
        if cv2.contourArea(c) < 2000:             #过滤掉较面积小的物体
            continue
        else:
            target_list.append(c)               #将面积较大的物体视为目标并存入目标列表
    for i in target_list:                       #绘制目标外接矩形
        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)
        cv2.drawContours(draw_img, [np.int0(box)], -1, (0, 255, 255), 2)
    return draw_img

#定义一个绘制中心点坐标的函数
def draw_center(target_list,draw_img):
    height, width, ch = draw_img.shape
    cv2.circle(draw_img, (width // 2, height // 2), 7, 128, -1)
    for c in target_list:
        M = cv2.moments(c)                   #计算中心点的x、y坐标
        center_x = int(M['m10']/M['m00'])
        center_y = int(M['m01']/M['m00'])
        print('center_x:',center_x)
        print('center_y:',center_y)
       
        cv2.circle(draw_img,(center_x,center_y),7,128,-1)#绘制中心点
        str1 = '(' + str(center_x)+ ',' +str(center_y) +')' #把坐标转化为字符串
        cv2.putText(draw_img,str1,(center_x-50,center_y+40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)#绘制坐标点位
    
    return draw_img

#计算误差
def get_error(target_list, draw_img):
    height, width, ch = draw_img.shape
    error_x, error_y = 0, 0
    for c in target_list:
        M = cv2.moments(c)
        center_x = int(M['m10']/M['m00'])
        center_y = int(M['m01']/M['m00'])

        error_x = width//2-center_x
        error_y = height//2-center_y
        str1 = "Error:"+'(' + str(error_x)+ ',' +str(error_y) +')' #把坐标转化为字符串
        cv2.putText(draw_img,str1,(0,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)#绘制坐标点位
        break

    return error_x, error_y


###主函数部分
#创建颜色字典
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'yellow': {'Lower': np.array([15, 160, 50]), 'Upper': np.array([35, 255, 255])},
              'green': {'Lower': np.array([50, 50, 50]), 'Upper': np.array([130, 255, 255])},
              }

#目标颜色
target_color = ['yellow']

#创建摄像头
capture = cv2.VideoCapture(0)

#初始化保存图片的编号
count=0

node = Node()

for event in node:
    if event["type"] == "INPUT":
        #创建目标列表。注意一定要将其放入循环中，可以尝试一下将这一行注释掉，把目标列表建在外面，看看区别
        target_list=[]
        
        ret, img = capture.read()
        draw_img = img
        erode_hsv = good_thresh_img(img)
        final_inRange_hsv = select_color_img(target_color,erode_hsv)
        contours = extract_contour(final_inRange_hsv)
        draw_img = find_target(contours,draw_img)
        final_img = draw_center(target_list,draw_img)
        error_x, error_y = get_error(target_list, draw_img)
        cv2.imshow('final_img', final_img)

        if event["id"] == "key-interval":
            key = cv2.waitKey(1)
            if key == 27:               #按Esc键退出
                break
            if key == -1 or key > 255:  #未按下则跳过
                continue
            elif key <= 255:
                node.send_output("key", pa.array([chr(key)]))

        if event["id"] == "error-interval":
            node.send_output("error", pa.array([error_x, error_y]))

cv2.destroyAllWindows()      #关闭展示窗口
capture.release()            #释放摄像头，若不释放，程序结束后摄像头一直处于开启状态
