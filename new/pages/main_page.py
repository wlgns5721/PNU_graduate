from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import sys
import cv2
import running_page

from pages.running_page import RunPage


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.createFormGroupBox()
        self.setGeometry(700, 500, 450, 150)
        self.run_btn = QPushButton("run")
        self.capture_btn = QPushButton("capture")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.run_btn)
        mainLayout.addWidget(self.capture_btn)
        self.setLayout(mainLayout)
        self.run_btn.clicked.connect(self.on_click_run)
        self.capture_btn.clicked.connect(self.on_click_capture)
        self.setWindowTitle("concrete crack detection")

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("이미지 경로")
        layout = QHBoxLayout()
        self.directory_edt = QLineEdit()
        self.directory_btn = QPushButton("경로 선택")
        layout.addWidget(self.directory_edt)
        layout.addWidget(self.directory_btn)
        self.formGroupBox.setLayout(layout)
        self.directory_btn.clicked.connect(self.on_click)

        # self.task_progress = TaskThread(self)
        # self.task_progress.taskEvent.connect(self.threadEventHandler)
        # self.task_progress.start()

    def on_click(self):
        file = QFileDialog().getExistingDirectory()
        self.directory_edt.setText(file)

    def on_click_run(self):
        option = ["directory",self.directory_edt.text()]
        test = RunPage(option)
        test.exec_()

    def on_click_capture(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            ret, frame = self.cap.read()
            cv2.imshow("capture", frame)
            if cv2.waitKey(1) > 0:
                cv2.imwrite("capture.jpg",frame)
                break

        self.cap.release()
        cv2.destroyAllWindows()
        option = ["capture","capture.jpg"]
        test = RunPage(option)
        test.exec_()

    # @pyqtSlot(int)
    # def threadEventHandler(self, n):
    #     self.value = n

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()