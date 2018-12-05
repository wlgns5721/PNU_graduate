from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
import sys
import cv2
import os
import errno

from pages.complete_page import CompletePage
from utils import *

class RunPage(QDialog):
    DEFAULT_DIRECTORY = "/home/visbic/shoh/cracky_test"
    directory = ""

    def __init__(self, option):
        super(RunPage, self).__init__()
        self.option = option
        self.setGeometry(700, 400, 450, 150)
        self.progress = QProgressBar(self)
        text = QLabel("분석 중입니다...")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.progress)
        self.setLayout(mainLayout)

        if(option[0]=="directory" and option[1]==""):
            self.directory = self.DEFAULT_DIRECTORY
        elif(option[0]=="directory"):
            self.directory = option[1]

        self.various_thread = VariousThread(self,option)
        self.various_thread.taskEvent.connect(self.threadEventHandler)
        self.various_thread.start()

        # self.task_progress = TaskThread(self)
        # self.task_progress.taskEvent.connect(self.threadEventHandler)
        # self.task_progress.start()

        self.setWindowTitle("concrete crack detection")




    @pyqtSlot(int)
    def threadEventHandler(self, value):
        self.progress.setValue(value)





class VariousThread(QThread):
    taskEvent = pyqtSignal(int)
    DEFAULT_DIRECTORY = "/home/visbic/shoh/cracky_test"
    directory = ""
    NOT_CRACK = 2
    CRACK = 0
    DRAW = 1

    def __init__(self, parent,option):
        super().__init__()
        self.n = 0
        # self.main = parent
        self.isRun = True
        self.option = option

    def run(self):
        self.processing()

    def processing(self):
        image_list = []
        self.taskEvent.emit(10)

        self.complete_list = []
        if (self.option[0] == "capture"):
            capture_image = cv2.imread(option[1])
            image_list.append(capture_image)
        elif (self.option[0] == "directory"):
            image_list, classify_list = classification(self.DEFAULT_DIRECTORY)

        # 파일을 열고 clahe 적용 후 저장
        # 균열 부분 검출하는 부분 추가할것
        # self.directory_timestamp = str(time.time()).replace('.','_')
        self.directory_timestamp = "result/" + str(time.time()).replace('.', '_')
        self.taskEvent.emit(90)
        time.sleep(0.5)
        try:
            if not (os.path.isdir(self.directory_timestamp)):
                os.makedirs(os.path.join(self.directory_timestamp))
                os.makedirs(os.path.join(self.directory_timestamp+"/draw"))
                os.makedirs(os.path.join(self.directory_timestamp+"/crack"))
                os.makedirs(os.path.join(self.directory_timestamp+"/not_crack"))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise

        for i in range(len(image_list)):
            timestamp = str(time.time()).replace('.', '_')
            if(classify_list[i]==self.CRACK):
                cv2.imwrite(self.directory_timestamp + "/crack/" + timestamp + ".jpg", image_list[i])
            elif (classify_list[i] == self.NOT_CRACK):
                cv2.imwrite(self.directory_timestamp + "/not_crack/" + timestamp + ".jpg", image_list[i])
            elif (classify_list[i] == self.DRAW):
                cv2.imwrite(self.directory_timestamp + "/draw/" + timestamp + ".jpg", image_list[i])
        self.taskEvent.emit(100)
        time.sleep(1.0)
        complete = CompletePage(self.directory_timestamp)
        complete.exec_()


class TaskThread(QThread):
    taskEvent = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.n = 0
        self.main = parent
        self.isRun = True
    def run(self):
        # instead of sleeping do the long running loop

        while(self.isRun):
            self.n+=3
            time.sleep(0.05)
            self.taskEvent.emit(self.n)

