from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from Game.snake import Snake
from Game.food import Food

def red_to_blue(steps):
    gradient_colors = []
    red_vals = range(255,-1,int(-1*256/steps))
    blue_vals = range(0,256,int(256/steps))

    for i in range(steps):
        gradient_colors.append((red_vals[i], 0, blue_vals[i]))

    return gradient_colors

class MainWindow(QMainWindow):
    def __init__(self, game_width, game_height, step_time_ms):
        super().__init__()

        self.setWindowTitle("Snake!")
        self.setFixedSize(game_width, game_height)

        self.game_widget = GameWidget(self, game_width, game_height, step_time_ms)
        self.setCentralWidget(self.game_widget)

    def keyPressEvent(self, event):
        self.game_widget.handleKeyPress(event)

class GameWidget(QWidget):
    def __init__(self, parent, game_width, game_height, step_time_ms):
        super().__init__(parent)
        self.step_time_ms = step_time_ms

        self.setFixedSize(game_width, game_height)
        self.setFocusPolicy(Qt.StrongFocus)

        self.snake = Snake(self.step_time_ms)
        self.food = Food()

        self.key_pressed = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGameState)
        self.startGame()

    def startGame(self):
        self.snake.reset()
        self.timer.start(self.step_time_ms)

    def handleKeyPress(self, event):
        self.key_pressed = event.key()

    def updateGameState(self):
        if self.key_pressed is not None:
            if self.key_pressed == Qt.Key_Escape:
                self.showPauseDialogue()
            else:
                self.snake.changeDirection(self.key_pressed)
            self.key_pressed = None

        if self.snake.isCollidingWithFood(self.food):
            self.snake.grow()
            self.food.respawn(self.width(), self.height(), self.snake)
        
        if self.snake.isCollidingWithSelf() or self.snake.isOutOfBounds(self.width(), self.height()):
            self.gameOver()
        
        self.snake.move()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        background_color = QColor(31, 31, 31)
        painter.fillRect(QRect(0, 0, self.width(), self.height()), background_color)

        self.drawSnake(painter)
        self.drawFood(painter)

    def drawSnake(self, painter):
        snek_len = len(self.snake.body)
        snek_colors = red_to_blue(snek_len)

        for i in range(len(self.snake.body)):
            segment = self.snake.body[i]
            painter.setBrush(QColor(*snek_colors[i]))
            border_color = QColor(*snek_colors[i])
            border_width = 0.5
            painter.setPen(QPen(border_color, border_width))
            painter.drawRect(segment)

    def drawFood(self, painter):
        painter.setBrush(QColor(0, 0, 255))
        border_color = QColor(63, 63, 255)
        border_width = 0.5
        painter.setPen(QPen(border_color, border_width))
        painter.drawRect(self.food.rect)
    
    def gameOver(self):
        self.timer.stop()
        self.showGameOverDialogue()

    def showPauseDialogue(self):
        self.timer.stop()
        pause_dialog = QMessageBox(self)
        pause_dialog.setWindowTitle("Pause")
        pause_dialog.setText(f"Game Paused\nScore: {len(self.snake.body)}")
        resume_button = QPushButton("We go", pause_dialog)
        close_button = QPushButton("Dinner's ready, gtg", pause_dialog)
        pause_dialog.addButton(resume_button, QMessageBox.AcceptRole)
        pause_dialog.addButton(close_button, QMessageBox.RejectRole)
        result = pause_dialog.exec()

        if result == QMessageBox.AcceptRole:
            self.timer.start()
        if result == QMessageBox.RejectRole:
            self.parent().close()

    def showGameOverDialogue(self):
        self.timer.stop()
        pause_dialog = QMessageBox(self)
        pause_dialog.setWindowTitle("Game Over")
        if len(self.snake.body) == 2304:
            pause_dialog.setText(f"You win! Go again?")
            close_button = QPushButton("Touch Grass", pause_dialog)
        else:
            pause_dialog.setText(f"Game Over. Try again?\nScore: {len(self.snake.body)}")
            close_button = QPushButton("GG no Re", pause_dialog)
        resume_button = QPushButton("Go Next", pause_dialog)
        pause_dialog.addButton(resume_button, QMessageBox.AcceptRole)
        pause_dialog.addButton(close_button, QMessageBox.RejectRole)
        result = pause_dialog.exec()

        if result == QMessageBox.AcceptRole:
            self.resetGame()
            self.startGame()
        if result == QMessageBox.RejectRole:
            self.parent().close()

    def resetGame(self):
        self.snake = Snake(self.step_time_ms)
        self.food = Food()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-wp", "--width", type=int, default=1280, help="Width of the game window")
    parser.add_argument("-hp", "--height", type=int, default=720, help="Height of the game window")
    parser.add_argument("-fr", "--frame_rate", type=int, default=25, help="Frame rate of the game")

    input_args = parser.parse_args()

    app = QApplication([])
    main_window = MainWindow(
        game_width=input_args.width, 
        game_height=input_args.height, 
        step_time_ms=int(1000/input_args.frame_rate),
        )
    main_window.show()
    app.exec_()
