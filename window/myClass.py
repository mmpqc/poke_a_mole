import operator
from functools import reduce
from random import Random

from PyQt5 import QtWidgets

# 2D显示容器  QGraphicsView  QGraphicsScene  QGraphicsItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QCursor


# 坐标体系
# 1. 当场景（scene）小于视图（view）时：
#   QGraphicsView的坐标原点在中心点
#   scene的原点也在中心点（我们指定scene的位置，指定的是scene的原点的位置）
# 2. 当场景大于视图时：
#   两者的坐标原点都在左上角


class MyScene(QtWidgets.QGraphicsScene):   # 场景类  坐标原点在中心点，但
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.bg = QPixmap(r".\img\bg.jpg")
        self.mole = QPixmap(r".\img\mole.jpg")

        self.items = []  # 定义数组存储图元

        self.w = 6      # w 表示 图元行列数
        for y in range(self.w):
            self.items.append([])
            for x in range(self.w):
                mp = MyPixmapItem(parent)
                mp.setPos(mp.boundingRect().width()*x, mp.boundingRect().height()*y)
                self.addItem(mp)
                self.items[y].append(mp)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showMole)

    def startGame(self):
        self.timer.start(1000)
        for item in reduce(operator.add, self.items):
            item.start = True

    def pauseGame(self):
        self.timer.stop()
        for item in reduce(operator.add, self.items):
            item.start = False

    def stopGame(self):
        for item in reduce(operator.add, self.items):
            item.setPixmap(self.bg)
            item.isMole = False
            item.start = False
        self.timer.stop()
        self.parent.score = 0
        self.parent.lcdNumber.display(self.parent.score)

    def showMole(self):
        for item in reduce(operator.add, self.items):
            item.setPixmap(self.bg)
            item.isMole = False

        for i in range(Random().randint(1, 3)):
            x = Random().randint(0, self.w - 1)
            y = Random().randint(0, self.w-1)
            self.items[y][x].setPixmap(QPixmap(self.mole))
            self.items[y][x].isMole = True


class MyPixmapItem(QtWidgets.QGraphicsPixmapItem):      # 像素 图元类
    def __init__(self, parent):
        super().__init__()
        self.setPixmap(QPixmap(r".\img\bg.jpg"))
        self.setCursor(QCursor(QPixmap("./img/cz_up.png")))

        self.parent = parent

        self.__isMole = False       # 标识图片是否是老鼠
        self.__start = False        # 标识游戏是否正在进行中

    @property
    def isMole(self):
        return self.__isMole

    @isMole.setter
    def isMole(self,value):
        self.__isMole = value

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    def mousePressEvent(self, event):
        # QtWidgets.QMessageBox().question(None, "提示", "鼠标按下", QtWidgets.QMessageBox.Yes)   # 注意None不能是self。
        self.setCursor(QCursor(QPixmap("./img/cz_down.png")))
        if self.__start:
            if self.__isMole == True:
                self.__isMole = False
                self.parent.score += 10
                self.parent.lcdNumber.display(self.parent.score)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.setCursor(QCursor(QPixmap("./img/cz_up.png")))
