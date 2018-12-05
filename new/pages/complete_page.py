from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import glob
import cv2

class CompletePage(QDialog):

    def __init__(self,directory_name):
        super(CompletePage, self).__init__()
        self.directory_name = directory_name
        self.index = 0
        self.current_list = []
        self.crack_list = []
        self.not_crack_list = []
        self.draw_list = []
        self.origin_image_files = []
        NOT_CRACK = 2
        CRACK = 0
        DRAW = 1
        self.DEFAULT_DIRECTORY = "/home/visbic/shoh/cracky_test"

        #해당 디렉토리에 있는 모든 이미지파일을 모은다.
        for image_file in glob.glob(self.directory_name+"/crack/*.jpg"):
            crack_pix_image = QPixmap(image_file)
            self.crack_list.append(crack_pix_image)

        # overall_image_files = os.listdir(self.DEFAULT_DIRECTORY)  # 분류하고 싶은 이미지가 저장된 폴더
        # for k in overall_image_files:
        #     image = cv2.imread(self.DEFAULT_DIRECTORY + '/' + k)
        #     origin_pix_image = QPixmap(image_file)
        #     self.origin_image_files.append(origin_pix_image)


        for image_file in glob.glob(self.DEFAULT_DIRECTORY+"/*"):
            origin_pix_image = QPixmap(image_file)
            self.origin_image_files.append(origin_pix_image)


        self.default_image = QPixmap("default.JPG")
        self.default_image = self.default_image.scaled(500, 500, Qt.KeepAspectRatio)
        self.setGeometry(500, 250, 1250, 750)

        self.current_list = self.crack_list
        self.size = len(self.current_list)
        image = self.current_list[self.index]
        scaled_image = image.scaled(500,500, Qt.KeepAspectRatio)
        origin_image = self.origin_image_files[self.index]
        origin_scaled_image = origin_image.scaled(500, 500, Qt.KeepAspectRatio)

        self.origin_label = QLabel(self)
        self.origin_label.setPixmap(origin_scaled_image)
        self.origin_label.move(50, 50)
        self.label = QLabel(self)
        self.label.setPixmap(scaled_image)
        self.label.move(700,50)
        self.next_button = QPushButton("next",self)
        self.next_button.move(1100,700)
        self.next_button.clicked.connect(self.next)
        self.previous_button = QPushButton("previous",self)
        self.previous_button.move(990,700)
        self.previous_button.clicked.connect(self.previous)
        self.previous_button.setDisabled(True)
        if(self.size<=1):
            self.next_button.setDisabled(True)

        self.setWindowTitle("concrete crack detection")

    def previous(self):
        self.index-=1
        if(self.index<=0):
            self.previous_button.setDisabled(True)
        self.next_button.setDisabled(False)
        image = self.current_list[self.index]
        scaled_image = image.scaled(500, 500, Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_image)
        origin_image = self.origin_image_files[self.index]
        origin_scaled_image = origin_image.scaled(500,500,Qt.KeepAspectRatio)
        self.origin_label.setPixmap(origin_scaled_image)
        self.update()

    def next(self):
        self.index+=1
        self.previous_button.setDisabled(False)
        if (self.index + 1 >= self.size):
            self.next_button.setDisabled(True)
        image = self.current_list[self.index]
        scaled_image = image.scaled(500, 500, Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_image)
        origin_image = self.origin_image_files[self.index]
        origin_scaled_image = origin_image.scaled(500, 500, Qt.KeepAspectRatio)
        self.origin_label.setPixmap(origin_scaled_image)
        self.update()
    #
    # def on_combobox_changed(self, value):
    #     if(value=="균열"):
    #         self.current_list = self.crack_list
    #     elif(value=="비균열"):
    #         self.current_list = self.not_crack_list
    #     elif(value=="낙서"):
    #         self.current_list = self.draw_list
    #     self.size = len(self.current_list)
    #     if(self.size==0):
    #         self.label.setPixmap(self.default_image)
    #         self.previous_button.setDisabled(True)
    #         self.next_button.setDisabled(True)
    #         return
    #     self.index=0
    #     self.previous_button.setDisabled(True)
    #     if(len(self.current_list)>1):
    #         self.next_button.setDisabled(False)
    #     else:
    #         self.next_button.setDisabled(True)
    #
    #     image = self.current_list[0]
    #     scaled_image = image.scaled(500, 500, Qt.KeepAspectRatio)
    #     self.label.setPixmap(scaled_image)
    #     self.update()

    def set_current_list(self,dest,src):
        for i in src:
            dest.apped(i)
