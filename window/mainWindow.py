from window import mainWindow_ui, myClass
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 窗体属性设置
        self.resize(883, 806)
        # 为视图添加场景
        self.scene = myClass.MyScene(self)
        self.graphicsView.setScene(self.scene)
        # 为按钮绑定事件
        self.pushButton.clicked.connect(self.scene.startGame)
        self.pushButton_2.clicked.connect(self.scene.pauseGame)
        self.pushButton_3.clicked.connect(self.scene.stopGame)

        self.score = 0
        self.lcdNumber.display(self.score)

    def closeEvent(self, event):
        re = QtWidgets.QMessageBox().warning(self, "提示", "确定关闭吗？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if re == QtWidgets.QMessageBox.No:
            event.ignore()
