from PyQt5.QtCore import Qt, QPoint, QRect
import time
class Snake():
    def __init__(self, step_time_ms):
        self.step_time_ms = step_time_ms
        self.movement_step = int(step_time_ms/2)
        self.segment_offset_factor = (20 - self.movement_step)/self.movement_step
        self.segment_steps = int(20/self.movement_step) 
    
        self.body = [QRect(100,100, 20, 20),
                     QRect(80,100, 20, 20),
                     QRect(60,100, 20, 20)]
        self.direction = QPoint(self.movement_step, 0)
        self.start = time.time()
        self.previous_directions = []
        for _ in range(len(self.body)*self.segment_steps):
            self.previous_directions.append(self.segment_steps*self.direction)

    def move(self):
        for seg in range(len(self.body)):
            seg = len(self.body) - seg - 1
            if seg == 0:
                self.body[seg].moveTo(self.body[seg].x() + self.direction.x(), self.body[seg].y() + self.direction.y())
                self.previous_directions.insert(0, self.direction)
                self.previous_directions.pop()
            else:
                prev_seg = seg-1
                previous_direction = self.previous_directions[prev_seg*self.segment_steps]
                offset_x = int(self.segment_offset_factor * previous_direction.x())
                offset_y = int(self.segment_offset_factor * previous_direction.y())
                self.body[seg].moveTo(self.body[prev_seg].x() - offset_x, self.body[prev_seg].y() - offset_y)

    def changeDirection(self, key):
        if key == Qt.Key_Up and self.direction != QPoint(0, self.movement_step):
            self.direction = QPoint(0, -self.movement_step)
        elif key == Qt.Key_Right and self.direction != QPoint(-self.movement_step, 0):
            self.direction = QPoint(self.movement_step, 0)
        elif key == Qt.Key_Down and self.direction != QPoint(0, -self.movement_step):
            self.direction = QPoint(0, self.movement_step)
        elif key == Qt.Key_Left and self.direction != QPoint(self.movement_step, 0):
            self.direction = QPoint(-self.movement_step, 0)

    def grow(self):
        last_segment = self.body[-1]
        new_segment = QRect(last_segment.x(), last_segment.y(), last_segment.width(), last_segment.height())
        self.previous_directions.extend(self.previous_directions[-self.segment_steps:])
        self.body.append(new_segment)

    def isCollidingWithSelf(self):
        return self.body[0] in self.body[1:]

    def isCollidingWithFood(self, food):
        head = self.body[0]
        head_x = head.x() + head.width()/2
        head_y = head.y() + head.height()/2

        y_in = head_y >= food.rect.y() - 8 and head_y <= food.rect.y() + food.rect.height() + 8
        x_in = head_x >= food.rect.x() - 8 and head_x <= food.rect.x() + food.rect.width() + 8

        return x_in and y_in
    
    def isOutOfBounds(self, width, height):
        head = self.body[0]
        return head.x() < 0 or head.y() < 0 or head.x() + head.width() > width or head.y() + head.height() > height

    def reset(self):
        self.body = [QRect(100,100, 20, 20),
                     QRect(80,100, 20, 20),
                     QRect(60,100, 20, 20)]
        self.direction = QPoint(self.movement_step, 0)