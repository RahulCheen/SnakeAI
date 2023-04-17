from PyQt5.QtCore import QRect
import random

class Food():
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.rect = QRect(140, 100, 20, 20)

    def respawn(self, game_width, game_height, snake):
        while True:
            x = random.randint(0, (game_width//20)-1)*20
            y = random.randint(0, (game_height//20)-1)*20
            self.rect.moveTo(x, y)
            
            if self.rect not in snake.body:
                break