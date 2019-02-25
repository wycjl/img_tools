# -*- coding: utf-8 -*-
# 引入外部库
import cv2
import numpy as np
import sys
from PyQt5 import QtGui,QtWidgets,Qt,QtCore
# 引入自己模块

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # 菜单栏
        exitAction = QtWidgets.QAction(QtGui.QIcon('Y:\image_tool\icon\start.png'), '&暗通道图像去雾（Kaiming）', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Kaiming早在09年以MSRA实习生的身份获得CVPR best paper，其成果就是给图像去雾。当时并没有用深度学习，却能实现让人震惊的效果。')
        exitAction.triggered.connect(self.run_rf)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&去雾算法')
        fileMenu.addAction(exitAction)
        # 工具栏
        # 状态栏
        self.statusBar()
        # 主界面
        self.hbox = QtWidgets.QHBoxLayout()
        self.lbl_left = QtWidgets.QLabel()
        self.lbl_left.setStyleSheet(
            "font:20pt '楷体';border-width: 3px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.lbl_left.setAutoFillBackground(True)
        # self.lbl_left.setFixedSize(1000, 1000)
        self.lbl_right = QtWidgets.QLabel()
        self.lbl_right.setStyleSheet(
            "font:20pt '楷体';border-width: 3px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.lbl_right.setAutoFillBackground(True)
        # self.lbl_right.setFixedSize(1000, 1000)
        self.hbox.addWidget(self.lbl_left)
        self.hbox.addWidget(self.lbl_right)
        self.setLayout(self.hbox)
        # 布局
        widget = QtWidgets.QWidget()
        widget.setLayout(self.hbox)
        self.setCentralWidget(widget)
        # 设置主窗口大小、位置、标题
        self.setGeometry(10, 10, 2000, 1000)
        self.setWindowTitle('Statusbar')
        self.showMaximized()
        self.show()

    def run_rf(self):
        from ui.remove_fog_dialog import yolo_param as yp
        self.temp = yp() # 这里一定要声明类成员变量，否则窗口会一闪而过
        self.temp.mySignal.connect(self.getDialogSignal)
        self.temp.mySignal_1.connect(self.getDialogSignal_1)
        self.temp.show()


    def getDialogSignal(self,connect):
        # print(connect)
        cv2.imwrite('temp.jpg',connect)
        self.img = cv2.imread('temp.jpg')
        result_label_left = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        # # cv2.imshow('a',result_label_left)
        # #
        showImage = QtGui.QImage(result_label_left.data, result_label_left.shape[1], result_label_left.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 将frame转换成Qimage格式
        self.lbl_right.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_right.setPixmap(QtGui.QPixmap.fromImage(showImage).scaled(self.lbl_left.size(), QtCore.Qt.KeepAspectRatio,
                                                                          QtCore.Qt.SmoothTransformation))

    def getDialogSignal_1(self,connect):
        # print(connect)
        result_label_left = cv2.cvtColor(connect, cv2.COLOR_BGR2RGB)

        # # cv2.imshow('a',result_label_left)
        # #
        showImage = QtGui.QImage(result_label_left.data, result_label_left.shape[1], result_label_left.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 将frame转换成Qimage格式
        self.lbl_left.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_left.setPixmap(QtGui.QPixmap.fromImage(showImage).scaled(self.lbl_left.size(), QtCore.Qt.KeepAspectRatio,
                                                                          QtCore.Qt.SmoothTransformation))
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())
