# 调取摄像头
import cv2
import numpy as np
import sys
import os
import time


def illegal_capture():
    print("开始拍摄入侵视频 : %s" % time.ctime())
    os.chdir('/home/pi/project/housekeeper/Camera/')
    time.sleep(8)
    # video_name即为时间戳
    video_name = str(time.time())[0:10]
    # print(video_name)

    # 下面的网址介绍了raspivid指令的参数，以及如何把.h264转换为.mp4格式的视频
    # https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
    os.system('raspivid -o %s.h264' % video_name)
    # 将这段  H.264 格式的视频流转换为每秒30帧的 .mp4 格式视频
    os.system('MP4Box -fps 30 -add %s.h264 %s.mp4' % (video_name, video_name))
    # 转换完之后，将.h264文件删除
    os.system('rm %s.h264' % video_name)
    print("视频录制结束 : %s" % time.ctime())

    return video_name


# if __name__ == "__main__":
#     illegal_capture()
