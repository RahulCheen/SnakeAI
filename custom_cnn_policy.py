from stable_baselines3.ppo import CnnPolicy
from stable_baselines3.common.torch_layers import NatureCNN
import torch.nn as nn

class CustomCnnPolicy(CnnPolicy):
    def __init(self, *args, **kwargs):
        super(CustomCnnPolicy, self).__init__(*args, **kwargs)
    
    def _build_cnn_extractor(self) -> None:
        self.cnn_extractor = CustomNatureCNN(self.features_dim, self.channels)

class CustomNatureCNN(NatureCNN):
    def __init__(self, features_dim: int, channels: int):
        super(NatureCNN, self).__init__()

        self.conv1 = nn.Conv2d(1, 64, kernel_size=2, stride=4, padding=0)
        self.conv2 = nn.Conv2d(64, 256, kernel_size=2, stride=2, padding=0)
        self.conv3 = nn.Conv2d(256, 256, kernel_size=1, stride=1, padding=0)