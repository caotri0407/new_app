import sys
import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialog

import cv2
import numpy as np
from tkinter import Tk
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
Tk().withdraw()
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(data[0], data[1])

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

def showdialog(data):
    dlg = QDialog()
    sc = MplCanvas(dlg, width=5, height=4, dpi=100)
    hbox = QHBoxLayout()
    sc.axes.plot(data[0], data[1])
    hbox.addWidget(sc)
    dlg.setLayout(hbox)
    dlg.setWindowTitle("Dialog")
    dlg.setWindowModality(Qt.ApplicationModal)
    dlg.exec_()


def evaluate(agl_list, fil_list, u_list, d_list):
    plt.figure(figsize=(10, 10))
    plt.plot(agl_list)
    plt.plot(fil_list)
    plt.show()

    print('agl_list: ', agl_list)
    print('fil_list: ', fil_list)
    print('u_list: ', u_list)
    print('d_list: ', d_list)
    l = len(d_list)
    color = {"RIGHT": (255, 0, 0),
             "WRONG": (0, 0, 255)}

    for i in range(l):
        up_img, up_right, up_rate = u_list[i]
        down_img, down_right, down_rate = d_list[i]

        up_img = cv2.resize(up_img, dsize=(600, 400))
        down_img = cv2.resize(down_img, dsize=(600, 400))
        up_str = "RIGHT" if up_right else "WRONG"
        down_str = "RIGHT" if down_right else "WRONG"

        ver = np.concatenate((up_img, down_img), axis=0)
        ver = cv2.putText(ver, up_str, (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, color[up_str], 3)
        ver = cv2.putText(ver, str(up_rate), (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, color[up_str], 3)
        ver = cv2.putText(ver, down_str, (50, 450), cv2.FONT_HERSHEY_PLAIN, 3, color[down_str], 3)
        ver = cv2.putText(ver, str(down_rate), (50, 500), cv2.FONT_HERSHEY_PLAIN, 3, color[down_str], 3)

        lastname = f'{i}/{l}'
        cv2.destroyWindow(lastname)

        cur_name = f'{i + 1}/{l}'
        cv2.namedWindow(cur_name)
        cv2.moveWindow(cur_name, 300, 50)
        cv2.imshow(cur_name, ver)
        cv2.waitKey(1)
        cv2.destroyAllWindows()