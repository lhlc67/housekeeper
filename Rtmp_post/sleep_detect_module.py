import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, models, transforms

# 神经网络


class Digit(torch.nn.Module):
    def __init__(self, *args, **kwargs):
        super(Digit, self).__init__(*args, **kwargs)
        self.conv1 = nn.Conv2d(1, 10, 5)
        self.conv2 = nn.Conv2d(10, 20, 5)
        self.pooling = torch.nn.MaxPool2d(2)

        self.fc1 = nn.Linear(320, 2)

    def forward(self, x):
        batch_size = x.size(0)
        x = F.relu(self.pooling(self.conv1(x)))
        x = F.relu(self.pooling(self.conv2(x)))

        x = x.view(batch_size, -1)
        x = self.fc1(x)
        output = F.log_softmax(x, dim=1)
        return output


data_transforms = {
    'train':
    transforms.Compose([
        # transforms.Resize(28),
        # 随机裁剪到300*300
        transforms.RandomResizedCrop(28),
        # transforms.RandomHorizontalFlip(),
        # transforms.CenterCrop(256),
        transforms.Grayscale(),
        transforms.ToTensor(),
        # 正则化处理，多数情况下来源于官方
        # transforms.Normalize([0.485, 0.456, 0.406],
        #  [0.229, 0.224, 0.225]),
    ]),
    'val':
    transforms.Compose([
        transforms.RandomResizedCrop(28),
        # transforms.CenterCrop(256),
        transforms.ToTensor(),

    ])
}
