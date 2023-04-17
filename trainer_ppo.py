from stable_baselines3 import PPO
# from custom_cnn_policy import CustomCnnPolicy
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

    model = PPO(
        policy, 
        env,
        **params
    )

    model.learn(total_timesteps=1_000_000)

    agent = '{:03d}'.format(len(glob.glob("./Agents Archive/ppo*.zip"))+1)
    model.save(f"./Agents Archive/ppo_snake_agent{agent}")
    model.save("ppo_snake_agent")

if __name__ == "__main__":
    main()
