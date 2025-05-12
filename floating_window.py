from built_in_animations import BouncingBallsWidget, SnakeWidget, TwinklingStarsWidget
from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer, QPoint, QPointF
from PyQt6.QtGui import QMovie, QPixmap
import trimesh
import numpy as np
import pyqtgraph.opengl as gl

class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.dragging = False
        self.offset = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

class FloatingWindow(QMainWindow):
    def __init__(self, animation_type="image", file_path=None, built_in_animation=None):
        super().__init__()
        self.animation_type = animation_type
        self.file_path = file_path
        self.built_in_animation = built_in_animation
        self.mesh_items = []
        self._drag_active = False
        self._drag_position = QPoint()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(1350, 900)

        if self.animation_type == "image":
            self.display_image()
        elif self.animation_type == "3d":
            self.display_3d_model()
        elif self.animation_type == "built_in":
            self.display_built_in_animation()
        else:
            self.close()

    def display_image(self):
        self.label = DraggableLabel(self)
        if self.file_path.endswith(".gif"):
            self.movie = QMovie(self.file_path)
            self.label.setMovie(self.movie)
            self.movie.start()
        else:
            pixmap = QPixmap(self.file_path)
            self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.resize(200, 200)
        self.label.move(1180, 560)  # Starting position

    def display_3d_model(self):
        self.view = gl.GLViewWidget(self)
        self.setCentralWidget(self.view)
        self.view.setCameraPosition(distance=10)
        self.view.setBackgroundColor('w')

        # Will update full func ASAP
        scene_or_mesh = trimesh.load(self.file_path)

        if isinstance(scene_or_mesh, trimesh.Scene):
            meshes = scene_or_mesh.geometry.values()
        else:
            meshes = [scene_or_mesh]

        for mesh in meshes:
            vertices = np.array(mesh.vertices)
            faces = np.array(mesh.faces)

            if hasattr(mesh.visual, 'vertex_colors') and mesh.visual.vertex_colors is not None:
                colors = mesh.visual.vertex_colors[:, :3] / 255.0
            else:
                colors = np.ones((vertices.shape[0], 3))

            mesh_item = gl.GLMeshItem(
                vertexes=vertices,
                faces=faces,
                faceColors=colors,
                drawEdges=False,
                smooth=True,
                shader='shaded'
            )
            self.view.addItem(mesh_item)
            self.mesh_items.append(mesh_item)

        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_model)
        self.timer.start(30)

    def rotate_model(self):
        self.angle += 1
        for item in self.mesh_items:
            item.rotate(1, 0, 1, 0)

    def display_built_in_animation(self):
        if self.built_in_animation == "balls":
            self.animation_widget = BouncingBallsWidget(self)
        elif self.built_in_animation == "snake":
            self.animation_widget = SnakeWidget(self)
        elif self.built_in_animation == "stars":
            self.animation_widget = TwinklingStarsWidget(self)
        else:
            self.close()
            return

        self.setCentralWidget(self.animation_widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_active = False
        event.accept()
