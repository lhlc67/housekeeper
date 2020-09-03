# -*- coding: utf-8 -*-
import oss2
import pymysql
import time
from twilio.rest import Client
import os


def save_info(video_name, time):
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="",
        # 数据库用户名称
        user="",
        # 数据库用户密码
        password="",
        # 数据库名称
        db="",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # SQL插入语句
    insert_sql = "insert into intrusion (created_at,videoname) values(%s,%s)"
    try:
        # 执行sql语句
        cursor.execute(insert_sql, (time, video_name))
        # 提交到数据库执行
        conn.commit()
    except Exception as e:
        # 如果发生错误则回滚并打印错误信息
        conn.rollback()
        print(e)

    # 关闭游标
    cursor.close()
    # 关闭数据库连接
    conn.close()


def send_message(otherStyleTime):
    """  
    通过twilio服务来实现手机短信的发送的接口,让主程序来调用
    """
    # Your Account SID from twilio.com/console
    account_sid = ""
    # Your Auth Token from twilio.com/console
    auth_token = ""
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        # 这里中国的号码前面需要加86
        to="+",
        from_="+",
        body=''' Message From Your Raspberry!
%s  Your family has unknown visitors''' % otherStyleTime)
    print(message.sid)


def Upload_Video(video_name):

    # 将非法视频信息插入MySQL
    otherStyleTime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(int(video_name)))
    save_info(video_name, otherStyleTime)
    send_message(otherStyleTime)

    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    # auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
    auth = oss2.Auth('',
                     '')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    # bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')
    bucket = oss2.Bucket(auth, '', '')

    # <yourObjectName>上传文件到OSS时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
    # <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    # bucket.put_object_from_file('<yourObjectName>', '<yourLocalFile>')

    ObjectName = 'RaspiVideo/%s.mp4' % video_name
    LocalFile = os.getcwd() + '/%s.mp4' % video_name
    bucket.put_object_from_file(ObjectName, LocalFile)


# if __name__ == '__main__':
#     otherStyleTime = time.strftime(
#         "%Y-%m-%d %H:%M:%S", time.localtime(int(1593073206)))

#     send_message(otherStyleTime)
