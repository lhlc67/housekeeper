import face_recognition
# import cv2
from cv2 import cv2
import pymysql
import numpy as np
import time
import Camera.illegal_capture as illegal_capture
import Camera.aliyunoss as aliyunoss
# import illegal_capture
# import aliyunoss
from PIL import Image, ImageDraw, ImageFont
import os
import sys



# 人脸特征编码集合
known_face_encodings = []

# 人脸特征姓名集合
known_face_names = []


# 从数据库获取保存的人脸特征信息
def get_info():
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="39.106.160.132",
        # 数据库用户名称
        user="cyq",
        # 数据库用户密码
        password="123",
        # 数据库名称
        db="raspi",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # SQL查询语句
    sql = "select * from face"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 返回的结果集为元组
        for row in results:
            name = row[1]
            encoding = row[2]
            # print("name=%s,encoding=%s" % (name, encoding))
            # 将字符串转为numpy ndarray类型，即矩阵
            # 转换成一个list
            dlist = encoding.strip(' ').split(',')
            # 将list中str转换为float
            dfloat = list(map(float, dlist))
            arr = np.array(dfloat)

            # 将从数据库获取出来的信息追加到集合中
            known_face_encodings.append(arr)
            known_face_names.append(name)

    except Exception as e:
        print(e)

        # 关闭数据库连接
        conn.close()


# 加载视频图像
def load_image():
    print(sys.path)
    #  打开摄像头 0代表笔记本的内置摄像头，1代表外置摄像头
    video_capture = cv2.VideoCapture(0)
    #video_capture= cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # 得到特征信息
    get_info()

    process_this_frame = True

    while True:

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 读取摄像头画面
        ret, frame = video_capture.read()

        # 利用opencv的缩放函数改变摄像头图像的大小，图像越小，所做的计算就少
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
        rgb_small_frame = small_frame[:, :, ::-1]

        # 处理每一帧的图像
        if process_this_frame:
            # 使用默认的HOG模型查找图像中的所有人脸
            face_locations = face_recognition.face_locations(rgb_small_frame)
            # 如果硬件允许，可以使用GPU进行加速，此时应改为CNN模型
            # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

            # 返回128维人脸编码，即人脸特征
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []

            # 将得到的人脸特征与数据库中的人脸特征集合进行比较，相同返回True，不同返回False
            for face_encoding in face_encodings:

                # matches：一个返回值为True或者False值的列表，该表指示了known_face_encodings列表的每个成员的匹配结果
                # tolerance：越小对比越严格，官方说法是0.6为典型的最佳值，也是默认值
                # 这里我设置0.45为最佳，可能跟我硬件有关
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.45)
                # 默认为unknown
                name = "Unknow"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    print('已存在')
                else:
                    # 释放摄像头资源,防止非法录像调用摄像头冲突
                    video_capture.release()
                    print('不存在')

                    # 开始进行录像,illegal_capture()返回值为时间戳，即为录像视频的文件名
                    video_name = illegal_capture.illegal_capture()
                    # 将视频名传入Upload_Video()函数，上传到阿里云OSS   
                    # 同时还要将入侵信息保存到MySQL中，暂时就这样写，后期再改
                    aliyunoss.Upload_Video(video_name)
                    # 将时间戳转化成时间格式
                    otherStyleTime = time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(int(video_name)))
                    print("时间->%s 非法入侵视频已上传阿里云OSS" % otherStyleTime)

                    video_capture = cv2.VideoCapture(0)

                face_names.append(name)
                # print("face_names.append(name)")

        process_this_frame = not process_this_frame

        # 将捕捉到的人脸显示出来
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # 恢复显示的图像大小
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # CV库有自己的编码规范，要想在图像上输出中文，需将图片格式转化为PIL库的格式，用PIL的方法写入中文，然后在转化为CV的格式
            # cv2和PIL中颜色的hex码的储存顺序不同
            cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pilimg = Image.fromarray(cv2img)
            
            # PIL图片上打印汉字NotoSansCJK-Light.ttc
            draw = ImageDraw.Draw(pilimg)
            # NotoSansCJK-Light.ttc为本机上已有的字体，可通过locate *.ttc进行查询

            # font = ImageFont.truetype("notosans.otf", 30, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
            # draw.text((left + 10, top - 40), name, (255, 255, 255), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
            
            # font = ImageFont.truetype(
            #     "NotoSansCJK-Light.otf", 30, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
            font = ImageFont.load_default().font
            draw.text((left + 10, top - 40), name, (255, 255, 255),
                      font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

            # PIL图片转cv2 图片
            frame = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)

            # 对人脸画出矩形框
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # 如果只想输出英文，可以省略以上步骤，编写以下代码即可
            # 显示的字体类型
            # font = cv2.FONT_HERSHEY_TRIPLEX
            # 打印识别信息
            #cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
        # 显示图像
        cv2.imshow('monitor', frame)

        # 按Q退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头资源
    video_capture.release()
    # 关闭显示图像的窗口
    cv2.destroyAllWindows()


if __name__ == '__main__':
    load_image()
