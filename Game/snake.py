from PyQt5.QtCore import Qt, QPoint, QRect

class Snake():
    def __init__(self, step_time_ms):
        self.step_time_ms = step_time_ms
        self.movement_step = int(step_time_ms/2)

        self.body = [QRect(100,100, 20, 20),
                     QRect(80,100, 20, 20),
                     QRect(60,100, 20, 20)]
        self.direction = QPoint(self.movement_step, 0)

        self.segment_directions = {}
        for k, seg in enumerate(self.body):
            self.segment_directions[f"segment_{k}"] = {
                "direction": self.direction,
                "movement_counter": 20/self.movement_step,
            }

    def move(self):
        new_head = self.body[0].translated(self.direction)
        self.body.insert(0, new_head)
        self.body.pop()
        # What is needed - method of linking the current direction of a segment to the segment
        # so - change direction - head immediately changes direction and maintains direciton* for 20/movement_step
        # movements. This stops overlap. after 20/movement_step movments the second segment will begin moving in direction*,
        # and so on. this maintians teh snakeish method of movement characteristic of the game.

    def changeDirection(self, key):
        prev_direction = self.direction
        if key == Qt.Key_Up and self.direction != QPoint(0, self.movement_step):
            self.direction = QPoint(0, -self.movement_step)
        elif key == Qt.Key_Right and self.direction != QPoint(-self.movement_step, 0):
            self.direction = QPoint(self.movement_step, 0)
        elif key == Qt.Key_Down and self.direction != QPoint(0, -self.movement_step):
            self.direction = QPoint(0, self.movement_step)
        elif key == Qt.Key_Left and self.direction != QPoint(self.movement_step, 0):
            self.direction = QPoint(-self.movement_step, 0)
        if prev_direction!= self.direction:
            self.changed_direction = True
            print(self.segment_directions)

    def grow(self):
        last_segment = self.body[-1]
        new_segment = QRect(last_segment.x(), last_segment.y(), last_segment.width(), last_segment.height())
        self.body.append(new_segment)

    def isCollidingWithSelf(self):
        return self.body[0] in self.body[1:]

    def isCollidingWithFood(self, food):
        head = self.body[0]
        head_x = head.x() + head.width()/2
        head_y = head.y() + head.height()/2

        y_in = head_y >= food.rect.y() and head_y <= food.rect.y() + food.rect.height()
        x_in = head_x >= food.rect.x() and head_x <= food.rect.x() + food.rect.width()

        return x_in and y_in
    
    def isOutOfBounds(self, width, height):
        head = self.body[0]
        return head.x() < 0 or head.y() < 0 or head.x() + head.width() > width or head.y() + head.height() > height

    def reset(self):
        self.body = [QRect(100,100, 20, 20),
                     QRect(80,100, 20, 20),
                     QRect(60,100, 20, 20)]
        self.direction = QPoint(self.movement_step, 0)