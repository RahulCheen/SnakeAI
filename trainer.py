from stable_baselines3 import PPO
from stable_baselines3 import DQN
from custom_cnn_policy import CustomCnnPolicy
# from small_window_cnn_policy import CustomCnnPolicy
# from stable_baselines3.dqn import CnnPolicy
from stable_baselines3.ppo import CnnPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from snake_env import SnakeEnv
import glob

def main():
    # policy = CustomCnnPolicy
    policy = CnnPolicy
    env = SnakeEnv()
    env = DummyVecEnv([lambda: env])

    params = {
        "learning_rate": 1e-4,
        "n_steps": 16384,
        "batch_size": 128,
        "n_epochs": 10,
        "gamma": 0.99,
        "gae_lambda": 0.95,
        "clip_range": 0.5,
        "clip_range_vf": None,
        "ent_coef": 0.01,
        "vf_coef": 0.75,
        "max_grad_norm": 0.5,
        "use_sde": False,
        "sde_sample_freq": -1,
        "target_kl": 1,
        "verbose": 1,
        "tensorboard_log": None, 
        "seed": None,
    }
    # params = {
    #     "buffer_size": 1000000,
    #     "learning_rate": 5e-4,
    #     "batch_size": 128,
    #     "gamma": 0.99,
    #     "tau": 0.01,
    #     "target_update_interval": 1000,
    #     "train_freq": (4, "step"),
    #     "gradient_steps": 1,
    #     "exploration_fraction": 0.5,
    #     "exploration_initial_eps": 1.0,
    #     "exploration_final_eps": 0.05,
    #     "verbose": 1,
    # }

    model = PPO(
        policy, 
        env,
        **params
    )

    model.learn(total_timesteps=1_000_000)

    agent = len(glob.glob("./Agents Archive/ppo*.zip"))+1
    model.save(f"./Agents Archive/ppo_snake_agent0{agent}")
    model.save("ppo_snake_agent")

if __name__ == "__main__":
    main()
