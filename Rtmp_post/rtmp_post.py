# 需先自行安装FFmpeg，并添加环境变量
import cv2
import subprocess
import Rtmp_post.sleep_detect_module as sleep_detect_module
import torch
from PIL import Image
from torch.autograd import Variable


# RTMP服务器地址
rtmp = "rtmp://123.57.31.195/live"
# 读取视频并获取属性
cap = cv2.VideoCapture(0)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
sizeStr = str(size[0]) + 'x' + str(size[1])

model = sleep_detect_module.Digit().to('cpu')
model.load_state_dict(torch.load('../sleep_Convolution.pt'))

command = ['ffmpeg',
           '-re',
           '-y', '-an',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', sizeStr,
           '-r', '25',
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmp]
pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE)


def sleep_detect(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = Image.fromarray(frame_gray)
    image = sleep_detect_module.data_transforms['train'](image).to('cpu')
    image = Variable(torch.unsqueeze(
        image, dim=0).float(), requires_grad=False)

    output = model(image)
    pred = torch.argmax(output, dim=1)
    # print(pred.item())
    # AddText = frame.copy()
    if pred.item() == 1:
        status = "UNCOVER"
    elif pred.item() == 0:
        status = "COVER"
    cv2.putText(frame, status, (200, 100),
                cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
    return frame


def push_to_aliyun():
    while cap.isOpened():
        success, frame = cap.read()
        frame2 = sleep_detect(frame)
        # cv2.imshow("")
        if success:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            pipe.stdin.write(frame.tostring())
    cap.release()
    pipe.terminate()
