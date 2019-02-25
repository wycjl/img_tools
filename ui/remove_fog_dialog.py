#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets,QtGui,Qt,QtCore
import numpy as np
import cv2
class yolo_param(QtWidgets.QWidget):
    # 自定义信号
    mySignal = QtCore.pyqtSignal(np.ndarray)
    mySignal_1 = QtCore.pyqtSignal(np.ndarray)
    def __init__(self):
        super(yolo_param,self).__init__()
        self.initUI()
        self.model_path = ''
        self.method = ''
    def initUI(self):
        self.vbox = QtWidgets.QVBoxLayout()

        # 图片：按钮+文本框
        self.btn_model_path = QtWidgets.QPushButton()
        self.btn_model_path.setText("输入图片：")
        self.btn_model_path.clicked.connect(self.btn_model_path_clicked)
        self.qle_model_path = QtWidgets.QLineEdit()
        self.qle_model_path.textChanged.connect(self.set_model_path)
        # self.qle_model_path.setText('yolo_package/model_data/trained_weights_final.h5')

        self.lbl = QtWidgets.QLabel()
        self.lbl.setStyleSheet(
            "font:12pt '楷体';border-width: 3px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.lbl.setText("算法选择：")

        self.combo = QtWidgets.QComboBox()
        self.combo.addItem('')
        self.combo.addItem('1')
        self.combo.addItem('2')
        self.combo.activated[str].connect(self.onActivated)


        # ok + cancel
        self.button_ok = QtWidgets.QPushButton()
        self.button_ok.setText("输入完毕")
        self.button_ok.clicked.connect(self.btn_ok)
        self.button_cancel = QtWidgets.QPushButton()
        self.button_cancel.setText("取消输入")
        self.button_cancel.clicked.connect(self.btn_cancel)
        # self.button_cancel.setEnabled(False)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.btn_model_path)
        self.hbox.addWidget(self.qle_model_path)

        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addWidget(self.button_ok)
        self.hbox1.addWidget(self.button_cancel)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addWidget(self.lbl)
        self.hbox2.addWidget(self.combo)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox1)

        self.setLayout(self.vbox)

        self.setGeometry(700,400,300,100)
        self.setWindowTitle(u'输入图片')
        # self.setWindowIcon(QtGui.QIcon('icon\\trend.png'))

    def btn_ok(self):
        import src.remove_fog as rf
        import src.remove_fog_2 as rf_2
        if self.model_path != '' and self.method != '':
            self.close()
            if self.method == '1':
                self.arr, self.J = rf.run(self.model_path)
                content = self.J
                self.mySignal.emit(content)
            elif self.method == '2':
                self.y = rf_2.deHaze(cv2.imread(self.model_path) / 255.0)*255
                content = self.y
                self.mySignal.emit(content)
        else:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"输入图片为空，退出前请输入图片", buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
    def btn_cancel(self):
        # self.qle_model_path.clear()
        return
    def set_model_path(self):
        self.model_path = self.qle_model_path.text()

    def btn_model_path_clicked(self):
        absolute_path = Qt.QFileDialog.getOpenFileName(self, 'open image', '.',"image (*.*)")
        self.qle_model_path.setText(absolute_path[0])
        img = cv2.imread(absolute_path[0])
        self.mySignal_1.emit(img)

    def onActivated(self,text):
        if text == '1':
            self.method = '1'
        elif text == '2':
            self.method = '2'











