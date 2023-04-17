import gym
from gym import spaces
from PyQt5.QtCore import Qt
import numpy as np
from snake import Snake
from food import Food
import pygame
import math

pygame.init()

class SnakeEnv(gym.Env):
    def __init__(self, render=False):
        super().__init__()
        
        if render:
            pygame.display.set_mode(display=0)

        self.game_width = 900
        self.game_height = 900
        self.snake = Snake()
        self.food = Food()
        self.previous_direction = self.snake.direction
        # self.previous_distance_from_food = math.dist([self.snake.body[0].x(), self.snake.body[0].y()],
        #                                              [self.food.rect.x(), self.food.rect.y()])

        self.screen = None
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0,
                                            high=255,
                                            shape=(self.game_height//20+1,
                                                   self.game_width//20+1,
                                                   1),
                                            dtype=np.uint8)
        
    def step(self, action):
        action = int(action)
        action_to_direction = {
            0: Qt.Key_Up,
            1: Qt.Key_Down,
            2: Qt.Key_Left,
            3: Qt.Key_Right
        }
        direction_key = action_to_direction[action]
        self.snake.changeDirection(direction_key)

        self.snake.move()

        new_distance_from_food = math.dist([self.snake.body[0].x(), self.snake.body[0].y()],
                                           [self.food.rect.x(), self.food.rect.y()])
        
        # if self.previous_distance_from_food > new_distance_from_food:
        #     reward = 0.1
        # else:
        #     reward = -0.01
        # self.previous_distance_from_food = new_distance_from_food

        reward = 1
        
        if self.previous_direction == self.snake.direction:
            reward = -1
        self.previous_direction = self.snake.direction

        if self.snake.isCollidingWithFood(self.food):
            self.snake.grow()
            self.food.respawn(self.game_width, self.game_height, self.snake)
            reward = 100

        observation = self._get_observation()
        info = {}
        info['snake_length'] = len(self.snake.body)
        info['food_loc'] = (self.food.rect.x(), self.food.rect.y())

        done = False
        if self.snake.isCollidingWithSelf() or self.snake.isOutOfBounds(self.game_width, self.game_height):
            done = True
            reward = -10

        return observation, reward, done, info

    def reset(self):
        self.snake.reset()
        self.food.reset()
        return self._get_observation()

    def render(self, mode='human'):
        observation = self._get_observation()

        if self.screen is None:
            self.screen = pygame.display.set_mode((self.game_width, self.game_height))
            pygame.display.set_caption('Snek Env')
        
        self.screen.fill((31, 31, 31))

        for y in range(observation.shape[0]):
            for x in range(observation.shape[1]):
                if observation[y, x] == 1:
                    color = (255, 0, 0)
                elif observation[y, x] == 2:
                    color = (0, 0, 255)
                else:
                    continue

                pygame.draw.rect(self.screen, color, (x*20, y*20, 20, 20))
        
        pygame.display.flip()
        pygame.time.delay(50)

    def _get_observation(self):
        observation = np.zeros((self.game_height//20+1, self.game_width//20+1, 1),
                                dtype=np.uint8)
        
        for segment in self.snake.body:
            x, y = segment.x(), segment.y()
            observation[y//20, x//20] = 1

        x, y = self.food.rect.x(), self.food.rect.y()
        observation[y//20, x//20] = 2

        return observation