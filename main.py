import snowboydecoder
import sys
import signal
import communite
import Voice.voice_detect
import os

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


if len(sys.argv) == 1:
    '''  
    如果没有执行的之后指定模型，执行这个函数
    '''
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

# sys.argv 是执行命令时对应的数组  ['demo.py', 'resources/models/snowboy.umdl']
# sys.argv[1]就是模型的存放位置
model = sys.argv[1]


# capture SIGINT signal, e.g., Ctrl+C
# 监听了SIGINT信号, 当程序在运行的时候同时按下键盘 Ctrl+c 就会执行signal_handler函数
signal.signal(signal.SIGINT, signal_handler)


# HotwordDetector()函数：Snowboy解码器检测是否由`decoder_model`指定的关键字
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')


VoiceManager = Voice.voice_detect.VoiceManager(
    '19779921', 'ohlZ0fwYGPpmjb2nTTANxj4n', 'KlN1dqu8eXU6RKsfwzNsgorntekL7Loi', '288b4064690743649baa9ee58e050bfa')
Work_path = os.getcwd()


def detect():
    snowboydecoder.play_audio_file()
    communite.communica(VoiceManager, Work_path)
    # print(result)


# main loop
# detector.start(detected_callback=snowboydecoder.play_audio_file,
#                interrupt_check=interrupt_callback,
#                sleep_time=0.03)
detector.start(detected_callback=detect,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
