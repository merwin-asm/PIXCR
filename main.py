from PyQt6.QtWidgets import QWidget , QApplication , QPushButton , QLabel
from PyQt6.QtGui import QIcon , QPainterPath , QRegion ,QPixmap
from screeninfo import get_monitors
from PyQt6.QtCore import Qt , QRectF , QThread , pyqtSignal
import sys
import cv2
import time
import pyautogui
import numpy as np
from PIL import ImageGrab


class BackgroundWork(QThread):
    a = pyqtSignal(list)
    b = pyqtSignal(list)
    c = pyqtSignal(list)
    d = pyqtSignal(str)
    e = pyqtSignal(int,int,int)
    def run(self):
        while self.run:
            time.sleep(0.01)
            pos = pyautogui.position()
            x = pos.x
            y = pos.y
            pos = f"x:{x}|y:{y}"
            self.d.emit(pos)
            self.img = ImageGrab.grab()
            self.img_np = np.array(self.img)
            self.scr = cv2.cvtColor(self.img_np, cv2.COLOR_RGB2BGR)
            cur = self.scr[y][x]
            cur = list(cur)
            r = cur[1]
            g = cur[2]
            b = cur[0]
            self.e.emit(r,g,b)
            r = [r, 0, 0]
            g = [0, g, 0]
            b = [0, 0, b]
            self.a.emit(r)
            self.b.emit(g)
            self.c.emit(b)
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PIXCR")
        self.setWindowIcon(QIcon("imgs/fill.png"))
        height = list(get_monitors())[0].height
        width = list(get_monitors())[0].width
        self.w = 350
        self.h = 200
        x = int(width)-int(self.w*2-self.w/2-150)
        y = 50
        self.setGeometry(x,y,1,1)
        self.setFixedWidth(self.w)
        self.setFixedHeight(self.h)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background:#344040;")
        self.create_title_bar()
        self.add_elem()
        self.show()
        self.run = True
        self.t = BackgroundWork()
        self.t.start()
        self.t.a.connect(self.change_c1)
        self.t.b.connect(self.change_c2)
        self.t.c.connect(self.change_c3)
        self.t.d.connect(self.change_txt_1)
        self.t.e.connect(self.change_txt_2)
    def change_c1(self,r):
        self.b1.setStyleSheet(f"background:rgb({r[0]},{r[1]},{r[2]})")
    def change_c2(self,r):
        self.b2.setStyleSheet(f"background:rgb({r[0]},{r[1]},{r[2]})")
    def change_c3(self,r):
        self.b3.setStyleSheet(f"background:rgb({r[0]},{r[1]},{r[2]})")
    def change_txt_1(self,pos):
        self.mouse_point.setText(pos)
    def change_txt_2(self,r,g,b):
        self.value.setText(f"rgb({r},{g},{b})")
    def create_title_bar(self):
        self.close_button = QPushButton("",self)
        self.close_button.setIcon(QIcon("imgs/cross-circle.png"))
        self.close_button.setFixedWidth(25)
        self.close_button.move(self.w-35,10)
        self.close_button.setStyleSheet("background-color:black;")
        self.minimize_button = QPushButton("",self)
        self.minimize_button.setIcon(QIcon("imgs/compress-alt.png"))
        self.minimize_button.setFixedWidth(25)
        self.minimize_button.move(self.w-65,10)
        self.minimize_button.setStyleSheet("background-color:black;")
        self.close_button.clicked.connect(self.close_btn)
        self.minimize_button.clicked.connect(self.minimize_btn)
        self.round_corners()
    def add_elem(self):
        self.label_IMG = QLabel(self)
        self.label_IMG.setPixmap(QPixmap("imgs/fill_2.png").scaledToWidth(30).scaledToHeight(30))
        self.label_IMG.move(30,150)
        self.value = QLabel("Value",self)
        self.value.setGeometry(80,160,150,15)
        self.value.setStyleSheet("color:#7ded3b")
        self.b1 = QLabel(self)
        self.b2 = QLabel(self)
        self.b3 = QLabel(self)
        self.b1.setGeometry(80,60,50,50)
        self.b2.setGeometry(150,60,50,50)
        self.b3.setGeometry(220,60,50,50)
        self.b1.setStyleSheet("background:red")
        self.b2.setStyleSheet("background:red")
        self.b3.setStyleSheet("background:red")
        self.mouse_point = QLabel("Mouse : ",self)
        self.mouse_point.setGeometry(250,180,100,15)
        self.mouse_point.setStyleSheet("color:#838582")
    def close_btn(self,a):
        self.run = False
        self.close()
    def minimize_btn(self,a):
        self.setWindowState(Qt.WindowState.WindowMinimized)
    def round_corners(self):
        radius = 8.0
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
app = QApplication(sys.argv)

win = Window()


sys.exit(app.exec())
