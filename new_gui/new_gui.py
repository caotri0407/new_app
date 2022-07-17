# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main1.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import threading
import time
import cv2
import keras
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import PoseModule as pm
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog

"""
Define variable global
"""
stylist_push_button = f"""
    color: rgb(231, 231, 231);
    border: 2px solid orange;
    padding: 5px;
    border-radius: 3px;
    opacity: 200;
    border-radius: 10px;
    """
play_thread = None
# Variable to detect landmarks and predict
count, no_right, no_wrong = 0, 0, 0
angle_list, filter_list = 0, 0

eval = False

running = True
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 720
VIDEO_X, VIDEO_Y = 50, 70
scale_rate = 1.5
VIDEO_WIDTH, VIDEO_HEIGHT = int(576 * scale_rate), int(320 * scale_rate)
model_up = keras.models.load_model("models/eff_loss_up.h5")
model_down = keras.models.load_model("models/eff_acc_down.h5")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(854, 583)
        MainWindow.setStyleSheet('background-image: url("icons/background.png");')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.videos_center = QtWidgets.QLabel(self.frame_4)
        # videos
        self.videos_center.setText("")
        self.videos_center.setScaledContents(True)
        self.videos_center.setObjectName("label")
        self.gridLayout_3.addWidget(self.videos_center, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem2, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_4, 1, 0, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 0, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem4, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.frame_5)
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton.setStyleSheet(stylist_push_button)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resume_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_5.addWidget(self.pushButton, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_2.setStyleSheet(stylist_push_button)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pause_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_5.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame_5, 2, 0, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.frame_6.setFont(font)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_6, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(36, 150, 241, 211))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_7.setAutoFillBackground(False)
        self.pushButton_7.setStyleSheet(stylist_push_button)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("file_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon2)
        self.pushButton_7.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_8.setAutoFillBackground(False)
        self.pushButton_8.setStyleSheet(stylist_push_button)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("camera_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon3)
        self.pushButton_8.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout.addWidget(self.pushButton_8)
        """
        self.pushButton_11 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy)
        self.pushButton_11.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_11.setAutoFillBackground(False)
        self.pushButton_11.setStyleSheet(stylist_push_button)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resume_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_11.setIcon(icon)
        self.pushButton_11.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout.addWidget(self.pushButton_11)
        self.gridLayout.addLayout(self.frame, 0, 1, 1, 2)
        self.frame_7 = QtWidgets.QFrame(self.centralwidget)
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_7.setObjectName("gridLayout_6")
        self.pushButton_11 = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_11.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        """
        self.pushButton_9 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_9.setAutoFillBackground(False)
        self.pushButton_9.setStyleSheet(stylist_push_button)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("stop_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon4)
        self.pushButton_9.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout.addWidget(self.pushButton_9)
        self.gridLayout.addWidget(self.frame, 0, 1, 2, 1)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_10.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_10.setStyleSheet(stylist_push_button)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("wrong_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon5)
        self.pushButton_10.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_6.addWidget(self.pushButton_10, 0, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem5, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_4.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_4.setStyleSheet(stylist_push_button)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("right_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon6)
        self.pushButton_4.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_6.addWidget(self.pushButton_4, 0, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem6, 0, 4, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_5.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_5.setStyleSheet(stylist_push_button)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("total_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon7)
        self.pushButton_5.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_6.addWidget(self.pushButton_5, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        """
        Define action for button push 
        """
        # For oopen file
        self.Worker1 = Worker1()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.no_wrong.connect(self.WrongLabel)
        self.Worker1.no_right.connect(self.RightLabel)
        self.Worker1.total.connect(self.TotalLabel)
        self.pushButton_7.clicked.connect(self.getfile)
        self.pushButton_8.clicked.connect(self.camera_ac)
        self.pushButton_9.clicked.connect(self.stop_button)
        self.pushButton_10.clicked.connect(self.resume_button)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Play      "))
        self.pushButton_2.setText(_translate("MainWindow", "Pause   "))
        self.label_2.setText(_translate("MainWindow", "Push-Up Evalution"))
        self.pushButton_7.setText(_translate("MainWindow", "OPEN FILE   "))
        self.pushButton_8.setText(_translate("MainWindow", "CAMERA      "))
        self.pushButton_9.setText(_translate("MainWindow", "STOP          "))
        self.pushButton_10.setText(_translate("MainWindow", "Wrong  "))
        self.pushButton_4.setText(_translate("MainWindow", "Right   "))
        self.pushButton_5.setText(_translate("MainWindow", "Total  "))

    def stop_button(self):
        self.Worker1.stop()

    def resume_button(self):
        self.Worker1.resume()

    def ImageUpdateSlot(self, Image):
        _translate = QtCore.QCoreApplication.translate
        self.videos_center.setPixmap(QPixmap.fromImage(Image))

    def WrongLabel(self, Wrong):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_10.setText(f"Wrong  {Wrong}")

    def RightLabel(self, Right):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_4.setText(f"Right  {Right}")

    def TotalLabel(self, Total):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_5.setText(f"Total  {Total}")

    def getfile(self):
        dlg = QFileDialog.getOpenFileName(None, "Open file", r"D:\code\freelancer\Tri_nguyen\new_gui",
                                          "All file (*);;; mp4 (*.mp4)")
        if dlg:
            file_name = dlg[0]
            self.Worker1.image_path = file_name
            self.Worker1.start()

    def camera_ac(self):
        self.Worker1.image_path = 0
        self.Worker1.start()

    def close_app(self):
        self.Worker1.stop()
        self.centralwidget.close()


"""
common function 
"""

"""
common function 
"""
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 720
VIDEO_X, VIDEO_Y = 50, 70
scale_rate = 1.5
VIDEO_WIDTH, VIDEO_HEIGHT = int(576 * scale_rate), int(320 * scale_rate)
model_up = keras.models.load_model("models/eff_loss_up.h5")
model_down = keras.models.load_model("models/eff_acc_down.h5")


def preprocessing_image(img):
    img = cv2.resize(img, dsize=(224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape(1, 224, 224, 3)
    return img


# test_img = cv2.imread("sample_images/img1.jpg")
# predict_test_image = preprocessing_image(test_img)
# model_up.predict(predict_test_image)
# model_down.predict(predict_test_image)

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    image_path = None
    no_wrong = pyqtSignal(object)
    no_right = pyqtSignal(object)
    total = pyqtSignal(object)
    eval = False
    def run(self):
        up_list, down_list = [], []
        angle_list, filter_list = [], []
        self.ThreadActive = True
        Capture = cv2.VideoCapture(self.image_path)
        pTime = 0
        check = 0
        count, no_right, no_wrong = 0, 0, 0
        detector = pm.poseDetector()
        frame_count = 0
        frame_skip_rate = 6
        angle_list = [160]
        filter_list = [140]
        T = 50
        color_tmp = (0, 255, 0)
        beta = 1 - frame_skip_rate / T

        high = True
        bar_height = 325
        up_right = True
        target_frame, target_angle = None, 0
        while self.ThreadActive:
            success, org_frame = Capture.read()
            if not success:
                break

            frame = cv2.resize(org_frame, dsize=(VIDEO_WIDTH, VIDEO_HEIGHT))
            frame = detector.findPose(frame, draw=False)
            lmList = detector.findPosition(frame, draw=False)
            if lmList:
                # frame, _ = detector.findBoundingBox(frame, draw=True)
                if not detector.left():
                    check = 0
                    cur_angle = detector.findAngle(frame, 12, 14, 16, draw=True)
                    tmp_angle = detector.findAngle(frame, 24, 26, 28, draw=True)
                    per = np.interp(cur_angle, (65, 150), (0, 100))
                    bar = np.interp(cur_angle, (65, 150), (bar_height, 100))
                else:
                    check = 1
                    cur_angle = detector.findAngle(frame, 11, 13, 15, draw=True)
                    tmp_angle = detector.findAngle(frame, 24, 26, 28, draw=True)
                    per = np.interp(cur_angle, (65, 150), (0, 100))
                    bar = np.interp(cur_angle, (65, 150), (bar_height, 100))
                if (frame_count + 1) % frame_skip_rate == 0:
                    cur_angle = max(60, cur_angle)
                    angle_list.append(cur_angle)

                    if high and cur_angle > target_angle:
                        target_frame, target_angle = org_frame, cur_angle
                    if not high and cur_angle < target_angle:
                        target_frame, target_angle = org_frame, cur_angle

                    Fn = beta * filter_list[-1] + (1 - beta) * cur_angle
                    filter_list.append(Fn)

                    if high and Fn > cur_angle:
                        count += 0.5
                        high = False
                        if per == 100:
                            color_tmp = (0, 255, 0)
                        predict_image = preprocessing_image(target_frame)
                        rate = model_up.predict(predict_image)[0][0]
                        if rate < 0.5 and tmp_angle > 160:
                            up_right = True
                            print("up right")
                        else:
                            up_right = False
                            print("up wrong", rate)
                        up_list.append((target_frame, up_right, rate))
                        target_angle = 200
                    if not high and Fn < cur_angle:
                        count += 0.5
                        high = True
                        if per == 0:
                            color_tmp = (0, 255, 0)
                        predict_image = preprocessing_image(target_frame)
                        rate = model_down.predict(predict_image)[0][0]
                        if rate < 0.5 and tmp_angle > 160:
                            down_right = True
                            print("down right")
                        else:
                            down_right = False
                            print("down wrong", rate)

                        down_list.append((target_frame, down_right, rate))

                        if up_right and down_right:
                            no_right += 1
                        else:
                            no_wrong += 1

                        target_angle = 0

                frame_count += 1
            bar_tmp = 720
            bar_tmp_2 = 758
            bar_tmp_3 = 643
            if check == 0:
                cv2.rectangle(frame, (bar_tmp, 100), (bar_tmp_2, bar_height), color_tmp, 3)
                cv2.rectangle(frame, (bar_tmp, int(bar)), (bar_tmp_2, bar_height), color_tmp, cv2.FILLED)
                cv2.putText(frame, f'{int(per)} %', (bar_tmp_3, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                            color_tmp, 4)
            else:
                cv2.rectangle(frame, (bar_tmp, 100), (bar_tmp_2, bar_height), color_tmp, 3)
                cv2.rectangle(frame, (bar_tmp, int(bar)), (bar_tmp_2, bar_height), color_tmp, cv2.FILLED)
                cv2.putText(frame, f'{int(per)} %', (bar_tmp_3, bar_tmp), cv2.FONT_HERSHEY_PLAIN, 4,
                            color_tmp, 4)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(frame, str(int(fps)), (30, 70), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)
            Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FlippedImage = cv2.flip(Image, 1)
            FlippedImage2times = cv2.flip(FlippedImage, 1)
            ConvertToQtFormat = QImage(FlippedImage2times.data, FlippedImage2times.shape[1], FlippedImage.shape[0],
                                       QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)
            self.no_wrong.emit(no_wrong)
            self.no_right.emit(no_right)
            self.total.emit(no_right + no_wrong)
            cv2.waitKey(1)
            self.eval = True
        if self.eval:
            # charts.showdialog(data=(angle_list, filter_list))
            # charts.evaluate(angle_list, filter_list, up_list, down_list)
            eval = False

    def stop(self):
        self.ThreadActive = False
        self.quit()

    def resume(self):
        self.ThreadActive = True
        self.run()
