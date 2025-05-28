from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt, QTimer, QPointF
import random
import math

class BouncingBallsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.balls = []
        for _ in range(10):
            ball = {
                'pos': QPointF(random.randint(50, 350), random.randint(50, 350)),
                'vel': QPointF(random.choice([-3, 3]), random.choice([-3, 3])),
                'color': QColor(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                'radius': random.randint(10, 20)
            }
            self.balls.append(ball)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)
        self.timer.start(30)

    def update_positions(self):
        for ball in self.balls:
            ball['pos'] += ball['vel']
            if ball['pos'].x() <= 0 or ball['pos'].x() >= self.width():
                ball['vel'].setX(-ball['vel'].x())
            if ball['pos'].y() <= 0 or ball['pos'].y() >= self.height():
                ball['vel'].setY(-ball['vel'].y())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        for ball in self.balls:
            painter.setBrush(ball['color'])
            painter.drawEllipse(ball['pos'], ball['radius'], ball['radius'])


class SnakeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.snake = [QPointF(600, 400)]
        self.length = 45
        self.angle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_snake)
        self.timer.start(50)

    def update_snake(self):
        self.angle += 0.05 # Adjust angle
        head = self.snake[0]
        new_head = QPointF(
            head.x() + math.cos(self.angle) * 15,
            head.y() + math.sin(self.angle * 2) * 15
        )
        self.snake.insert(0, new_head)
        if len(self.snake) > self.length:
            self.snake.pop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        for i, point in enumerate(self.snake):
            color = QColor(255 - i*10, 100 + i*10, 255)
            painter.setBrush(color)
            radius = max(5, 15 - i)
            painter.drawEllipse(point, radius, radius)


class TwinklingStarsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = []
        for _ in range(50):
            star = {
                'pos': QPointF(random.randint(0, 400), random.randint(0, 400)),
                'brightness': random.randint(100, 255)
            }
            self.stars.append(star)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stars)
        self.timer.start(50)

    def update_stars(self):
        for star in self.stars:
            change = random.choice([-55, 55])
            star['brightness'] = max(100, min(255, star['brightness'] + change))
            star['pos'].setY(star['pos'].y() - 1)
            if star['pos'].y() < 0:
                star['pos'].setY(self.height())
                star['pos'].setX(random.randint(0, self.width()))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        for star in self.stars:
            color = QColor(star['brightness'], star['brightness'], star['brightness'])
            painter.setBrush(color)
            painter.drawEllipse(star['pos'], 2, 2)
    # Add more here acc to your designs, whatever you need
    # Note: These basic animations were made with help from AI.
    # My goal was to use a GIF as a floating mascot.