# 引入Speech SDK
from aip import AipSpeech
import os
import requests
import json
import os
import sys
import pyaudio
import wave
import time
import socket


class VoiceManager:
    """
        声音检测类  

        :param Baidu_APP_ID  
        :param Baidu_APP_KEY  
        :param Baidu_SECRET_KEY  
        :param Tuling_API_KEY
    """

    def __init__(self, APP_ID, APP_KEY, SECRET_KEY, Tuling_API_KEY):
        # 初始化AipSpeech对象
        self.aipSpeech = AipSpeech(APP_ID, APP_KEY, SECRET_KEY)
        self.tulingKey = Tuling_API_KEY

    def voice2string(self,  filename):
        """
        声音监测函数

        :param filepath
        :param filename
        :param filetype
        """
        # 获取文件的类型
        filetype = filename.split(".")[1]
        result = self.aipSpeech.asr(self.get_file_content(filename),
                                    filetype, 16000)
        if (result['err_no'] == 0):
            return result['result'][0]
        else:
            return "ERROR"
        # return result

    # 读取文件

    def get_file_content(self, FileName):
        with open(FileName, 'rb') as fp:
            return fp.read()

    def string2voice(self, speakinfo, filename):
        """
        传入字符串得到mp3文件
        :param speakinfo 要说的话
        :param filename 文件名
        """
        result = self.aipSpeech.synthesis(speakinfo, 'zh', 1, {
            'vol': 5,
        })
        # print(result)
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open(filename, 'wb') as f:
                f.write(result)
            # return speakinfo

        os.system('mplayer %s' % filename)

    def Tuling(self, words):
        url = "http://www.tuling123.com/openapi/api"
        body = {"key": self.tulingKey, "info": words.encode("utf-8")}
        res = requests.post(url, data=body, verify=True)
        if res:
            date = json.loads(res.text)
            # print(date["text"])
            return date["text"]
        else:
            return None

     # 录音
    def Record(self, filename):

        # 关闭掉各种报错
        # os.close(sys.stderr.fileno())

        # 定义超参数
        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 5
        # WAVE_OUTPUT_FILENAME = filename
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("recording...")
        # 定义一个列表
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):       # 循环，采样率 44100 / 1024 * 5
            data = stream.read(CHUNK)       # 读取chunk个字节 保存到data中
            frames.append(data)             # 向列表frames中添加数据data
        print("done")

        stream.stop_stream()
        stream.close()          # 关闭
        p.terminate()           # 终止pyaudio

        '''save the date to the wavfile'''
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))      # 采样字节
        wf.setframerate(RATE)                           # 采样频率 8000 or 16000
        # https://stackoverflow.com/questions/32071536/typeerror-sequence-item-0-expected-str-instance-bytes-found
        wf.writeframes(b''.join(frames))

        wf.close()
        time.sleep(2)

    def get_host_ip(self):
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

# def Record(filename):

# 	#关闭掉各种报错
# 	# os.close(sys.stderr.fileno())

# 	CHUNK = 512
# 	FORMAT = pyaudio.paInt16
# 	CHANNELS = 1
# 	RATE = 16000
# 	RECORD_SECONDS = 5
# 	WAVE_OUTPUT_FILENAME = filename

# 	p = pyaudio.PyAudio()

# 	stream = p.open(format=FORMAT,
# 					channels=CHANNELS,
# 					rate=RATE,
# 					input=True,
# 					frames_per_buffer=CHUNK)

# 	print("recording...")

# 	frames = []

# 	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
# 		data = stream.read(CHUNK)
# 		frames.append(data)

# 	print("done")

# 	stream.stop_stream()
# 	stream.close()
# 	p.terminate()

# 	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# 	wf.setnchannels(CHANNELS)
# 	wf.setsampwidth(p.get_sample_size(FORMAT))
# 	wf.setframerate(RATE)
# 	wf.writeframes(b''.join(frames))
# 	wf.close()

# 	time.sleep(2)


# if __name__ == "__main__":
#     # voicetest()
#     t = VoiceDetecter('19779921', 'ohlZ0fwYGPpmjb2nTTANxj4n',
#                       'KlN1dqu8eXU6RKsfwzNsgorntekL7Loi')
#     res = t.detect('/home/pi/project/py_project/audiohandle/code/myaudio/',
#                    '16k.wav', 'wav')
#     Record("result.wav")
#     print(res)
# # 遍历文件夹中的wav并进行识别
# for dir in [x for x in os.listdir(path) if x[-1] == 'v']:
#     print(dir)
#     try:
#         t = aipSpeech.asr(get_file_content(dir), 'wav', 16000, {'lan': 'zh', })
#         # print t
#         print(t['result'][0])
#     except:
#         print("error ,pass")
