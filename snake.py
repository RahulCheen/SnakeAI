from PyQt5.QtCore import Qt, QPoint, QRect

class Snake():
    def __init__(self):
        self.body = [QRect(100,100, 20, 20),
                     QRect(80,100, 20, 20),
                     QRect(60,100, 20, 20)]
        self.direction = QPoint(20, 0)

    def move(self):
        new_head = self.body[0].translated(self.direction)
        self.body.insert(0, new_head)
        self.body.pop()

    def changeDirection(self, key):
        if key == Qt.Key_Up and self.direction != QPoint(0, 20):
            self.direction = QPoint(0, -20)
        elif key == Qt.Key_Right and self.direction != QPoint(-20, 0):
            self.direction = QPoint(20, 0)
        elif key == Qt.Key_Down and self.direction != QPoint(0, -20):
            self.direction = QPoint(0, 20)
        elif key == Qt.Key_Left and self.direction != QPoint(20, 0):
            self.direction = QPoint(-20, 0)

    def grow(self):
        last_segment = self.body[-1]
        new_segment = QRect(last_segment.x(), last_segment.y(), last_segment.width(), last_segment.height())
        self.body.append(new_segment)

    def isCollidingWithSelf(self):
        return self.body[0] in self.body[1:]

    def isCollidingWithFood(self, food):
        return self.body[0] == food.rect
    
    def isOutOfBounds(self, width, height):
        head = self.body[0]
        return head.x() < 0 or head.y() < 0 or head.x() + head.width() > width or head.y() + head.height() > height

    def reset(self):
        self.body = [QRect(100,100, 20, 20),
                     QRect(80,100, 20, 20),
                     QRect(60,100, 20, 20)]
        self.direction = QPoint(20, 0)