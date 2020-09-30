# -*- coding: utf-8 -*-
import Voice.voice_detect
import os
import Camera.recogtion as recogtion
import Sensor.dht11API as dht11API
import Rtmp_post.rtmp_post as rtmp_post


def communica(VoiceManager, Work_path):
    # # 初始化声音监测对象  如果每次执行这个函数都要定义一次这个的话可能速度会比较慢
    # VoiceManager = Voice.voice_detect.VoiceManager(
    #     '19779921', 'ohlZ0fwYGPpmjb2nTTANxj4n', 'KlN1dqu8eXU6RKsfwzNsgorntekL7Loi', '/home/pi/project/housekeeper/Voice/')
    # os.chdir('/home/pi/project/housekeeper/Voice/')
    os.chdir(Work_path + '/Voice')
    # 录音得到录音文件
    VoiceManager.Record("result.wav")
    # 调用百度语音接口，识别刚才录制的.wav文件中的信息
    result = VoiceManager.voice2string(
        'result.wav')
    print(result)

    if "温度" in result:
        print("---------------")
        info = dht11API.GetDht11()
        conncont = "当前温度为%d摄氏度" % info['temperature'] + \
            "当前湿度为百分之%d" % info['humidity']
        VoiceManager.string2voice(conncont, 'ip.mp3')
        return 0
    elif "IP" in result:
        ip = "我的IP地址是"+VoiceManager.get_host_ip()
        VoiceManager.string2voice(ip, 'ip.mp3')
        return 0
    elif "出门" in result:
        VoiceManager.string2voice("主人注意安全，我会自动开启人脸识别监控的", 'result.mp3')
        recogtion.load_image()
        return 0
    elif "睡觉" in result:
        VoiceManager.GetVoice("主人请放心，我会帮忙照看宝宝的", 'result.mp3')
        rtmp_post.push_to_aliyun()
        return 0
    elif "退出" in result:
        VoiceManager.string2voice("再见了主人", 'ip.mp3')
        exit()

    tulingworkds = VoiceManager.Tuling(result)
    print(tulingworkds)
    VoiceManager.string2voice(tulingworkds, 'result.mp3')

    # playsound('tuling.mp3')
    # os.remove('result.mp3')


# if __name__ == "__main__":
#     rtmp_post.push_to_aliyun()
"""  
1.录音，将录音中的内容监测返回字符串 √
2.对接图灵机器 √
3.讲图灵机器人的回话播放出来 √
4.人脸识别 √
5.pytorch图像分类检测 √
"""
