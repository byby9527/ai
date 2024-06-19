# 參考老師的程式碼:https://github.com/ccc112b/py2cs/blob/master/03-%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7/05-%E7%A5%9E%E7%B6%93%E7%B6%B2%E8%B7%AF/02-%E6%B7%B1%E5%BA%A6%E5%AD%B8%E7%BF%92/01-MNIST/lenet.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        ### 定義卷積層，用於輸入特徵圖中提取特徵
        super(Net, self).__init__()
       ### 接收1個通道的輸入（灰度圖像），產生8個通道的輸出，應用3x3的卷積核
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, padding=1)
       ### 定義全連接層，將前一層的所有神經元（或特徵）連接到每一個神經元上，用於分類或回歸任務
        self.fc1 = nn.Linear(in_features=16*7*7, out_features=256)
        self.fc2 = nn.Linear(in_features=256, out_features=120)
        self.fc3 = nn.Linear(in_features=120, out_features=10)

    def forward(self, x):
       ### 第一個卷積層，並應用ReLU激活函數
        x = F.relu(self.conv1(x))
        ### 最大池化層，將特徵圖尺寸減半
        x = F.max_pool2d(x, kernel_size=2, stride=2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, kernel_size=2, stride=2)
       ### 展平特徵圖
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
       ### 最後一個全連接層，不使用激活函數
        x = self.fc3(x)
        return x
