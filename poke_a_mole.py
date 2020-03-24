import sys
from window import mainWindow
from PyQt5 import QtWidgets

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = mainWindow.MainWindow()
    win.show()
    exit(app.exec_())
