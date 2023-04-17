from stable_baselines3 import DQN
# from custom_cnn_policy import CustomCnnPolicy
from stable_baselines3.dqn import CnnPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from snake_env import SnakeEnv
import glob

def main():
    # policy = CustomCnnPolicy
    policy = CnnPolicy
    env = SnakeEnv()
    env = DummyVecEnv([lambda: env])

    params = {
        "buffer_size": 1000000,
        "learning_rate": 5e-4,
        "batch_size": 128,
        "gamma": 0.99,
        "tau": 0.01,
        "target_update_interval": 1000,
        "train_freq": (4, "step"),
        "gradient_steps": 1,
        "exploration_fraction": 0.5,
        "exploration_initial_eps": 1.0,
        "exploration_final_eps": 0.05,
        "verbose": 1,
    }

    model = DQN(
        policy, 
        env,
        **params
    )

    model.learn(total_timesteps=1_000_000)

    agent = '{:03d}'.format(len(glob.glob("./Agents Archive/dqn*.zip"))+1)
    model.save(f"./Agents Archive/dqn_snake_agent{agent}")
    model.save("dqn_snake_agent")

if __name__ == "__main__":
    main()
