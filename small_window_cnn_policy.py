import torch as th
import torch.nn as nn
from stable_baselines3.dqn import CnnPolicy

class CustomCnnPolicy(CnnPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomCnnPolicy, self).__init__(*args, **kwargs)

        self.cnn = nn.Sequential(
            nn.Conv2d(self.observation_space.shape[0], 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        # Calculate the output size of the CNN layers to determine the input size of the linear layers
        with th.no_grad():
            sample_obs = th.as_tensor(self.observation_space.sample()[None]).float()
            cnn_output_size = self.cnn(sample_obs).shape[1:].numel()

        self.q_net = nn.Sequential(
            nn.Linear(cnn_output_size, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_space.n)
        )

    def forward(self, obs: th.Tensor, deterministic: bool = True) -> th.Tensor:
        q_values = self.cnn(obs).view(obs.size(0), -1)
        return self.q_net(q_values)

