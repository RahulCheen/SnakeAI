# SnakeAI
In this repo, I have used python to write a simple Snake game using PyQT and have defined a custom environment using Stable Baselines 3 to train PPO and DQN algorithms to play the game. To train, run either the trainer_dqn.py or trainer_ppo.py scripts. To edit model hyperparameters, change the values in the "params" dictionary. Once complete, agents will save as zip folders. To run the agent and watch it play Snake, run the run_PPO.py or run_DQN.py scripts depending on the model trained.
NOTE: as is, the models don't work very well. I'm still figuring out hyperparameters and training conditions.

# This repo isn't fully set up yet
I need to reorganize some files and clean up some code before it's ready for development

# If you just want to play the game
You can play the snake game as long as you have the PyQt5 python module. You'll only need the files in the /Game folder. Just run main.py
Use arrow keys to control the snake and the escape key to pause

# snake_env.py
This is the custom Stable Baselines 3 environment I have defined for training the models.
- The observation space is a currently a simplified matrix representing the current game state where 0s are empty pixels, 1s are snake pixels, and 2s are food pixels. This will likely change as I figure out what works.
- The reward structure is simple. Eating a food gives +100 reward. In a given timestep, moving closer (Euclidian distance) yields +1 and moving further yields -1 reward. This will also likely change frequently as I play with different reward structures/values.
- The action space is one of four movements. Either up, down, left, or right.

# trainer_dqn.py and trainer_ppo.py
These scripts train either a DQN (Deep Q-Network) or a PPO (Proximal Policy Optimization) model. Models are automatically saved as zip folders both to the main directory and to the Agents Archive subfolder where they are numbered. I have added .zip files to the .gitignore so I don't flood the repo with my models.

# run_PPO.py and run_DQN.py
These are used to watch the agents of the respective models run. They look for a .zip file in the main directory, so there's no need to move any files around after training a model. Just run the script and watch it go. I have been messing around with some loggign to evaluate performance so these will probably change a little bit as I work on this project.

# custom_cnn_policy.py
This defines a custom convolutional neural network so I can modify network architecture as I need. It is not currently used by either trainer but the import is already defined in each trainer if you want to play with it.
