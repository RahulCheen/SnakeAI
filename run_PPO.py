from stable_baselines3 import PPO
# from stable_baselines3 import DQN
from snake_env import SnakeEnv
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 5]

model = PPO.load("ppo_snake_agent")

env = SnakeEnv(render=True)

obs = env.reset()
done = False
n = 0
rewards = []
# plt.ion()
# fig, ax = plt.subplots()
# ax.set_xlabel("Step"), ax.set_ylabel("Reward")
print('Step:\tReward\tLength\tFood Location')
while not done:
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    rewards.append(reward)

    print(f'{n}:\t{round(reward, 3)}\t{info["snake_length"]}\t{info["food_loc"]}')
    
    # fig.clf()
    # ax.set_xlabel("Step"), ax.set_ylabel("Reward")
    # if len(rewards) < 100:
    #     line = ax.plot(rewards, 'r')
    # else:
    #     line = ax.plot(rewards[-100:], 'r')
    # fig.canvas.draw()
    # fig.canvas.flush_events()
    env.render()
    n += 1

    

