from PyQt5 import QtWidgets, uic
import Program as pg
from PyQt5.QtWidgets import QMessageBox
import time
import threading
import cv2
import g2
g2.com("COM1")
g2.open()
import sqlite3
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QThread, pyqtSignal, pyqtSlot
kernel = np.ones((5, 5), np.uint8)

class MyThread(QThread):
    # bien data
    data = pyqtSignal(str)
    # bien ngat cua vong lap while
    STT = 1
    # ham duoc chay khi goi self.start()
    def run(self):
        while self.STT:
            if g2.s.in_waiting:  # Or: while ser.inWaiting():
                data = g2.read()
                self.data.emit(data)
            else:
                time.sleep(1)
class window(QtWidgets.QMainWindow):
    sttStart = 0
    sttCheckBox = 0
    data = []
    def __init__(self, nameUi):
        QtWidgets.QWidget.__init__(self)
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        # load giao dien
        uic.loadUi(nameUi, self)
        self.Tcam1 = threading.Thread(target=cam1, name='thread 1')
        self.BoardIO = MyThread()
        self.BoardIO.data.connect(self.setStatus)
        self.BoardIO.start()
        self.btnStart.clicked.connect(self.btn_Start)
        self.btnChup.clicked.connect(self.btn_Chup)
        self.btnSave.clicked.connect(self.btn_Save)
        self.btnDelete.clicked.connect(self.btn_Delete)
        self.cbb_Program.currentTextChanged.connect(self.LoadLoc)
        self.checkBox.stateChanged.connect(self.check_Box)

        namepg = pg.get_all_nameTableDB()
        name = namepg[::-1]
        if len(name) > 0:
            self.loadDataOnGui(name[0])
            self.cbb_Program.addItems(name)
            self.cbb_Mauthu1.addItems(name)
            self.cbb_Mauthu2.addItems(name)
            self.cbb_Mauthu3.addItems(name)
        self.show()

    def setStatus(self, c):
        data = c
        self.lb_Time.setText(data)
        self.bar.setValue(int(data))
        if data == 'Cap':
            print(data)
            # self.lb_data.setText(str(data))
            self.btnChup.click()
            named_tuple = time.localtime()  # get struct_time
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            self.lb_Time.setText(time_string)

    def btn_Chup(self):
        mauphathien = "None"
        ret, img = self.cam.read()
        ret, img = self.cam.read()

        name = self.cbb_Mauthu1.currentText()
        data = pg.read_from_db(name)
        _, phathien = BoLoc(data, img)

        if phathien:
            mauphathien = name
            g2.send("A")
        else:
            name = self.cbb_Mauthu2.currentText()
            data = pg.read_from_db(name)
            _, phathien = BoLoc(data, img)

            if phathien:
                mauphathien = name
                g2.send("B")
            else:
                name = self.cbb_Mauthu3.currentText()
                data = pg.read_from_db(name)
                _, phathien = BoLoc(data, img)

                if phathien:
                    mauphathien = name
                    g2.send("C")

                else:
                    mauphathien = "None"

        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get frame infos
        height, width, channel = frame.shape
        step = channel * width
        # create QImage from RGB frame
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.lb_Img.setPixmap(QPixmap.fromImage(qImg))
        self.lb_Mauphathien.setText(mauphathien)
        # print("chup")


    def check_Box(self, state):
        if state:
            self.sttCheckBox = 1
            self.btnSave.setEnabled(True)
            self.btnDelete.setEnabled(True)
        else:
            self.btnSave.setEnabled(False)
            self.btnDelete.setEnabled(False)
            self.sttCheckBox = 0



    def btn_Start(self):
        if self.sttStart:
            self.sttStart = 0
            self.btnStart.setText("Start")
            self.btnStart.setStyleSheet("background-color: green")
            # self.cam0.quit()
            # self.cam0.wait()
        else:
            self.sttStart = 1
            # self.cam0.start()
            if self.Tcam1.is_alive() == False:
                self.Tcam1.start()
            self.btnStart.setText("Stop")
            self.btnStart.setStyleSheet("background-color: red")
        # self.cam0.start()
    def btn_Save(self):
        #lay ten ct
        namepg = self.cbb_Program.currentText()
        #xoa chuong trinh ten do
        pg.del_and_update(namepg)
        #tao ct vs ten do
        pg.create_table(namepg)
        #Lay data
        lh = self.horizontalSlider.value()
        ls = self.horizontalSlider_2.value()
        lv = self.horizontalSlider_3.value()
        uh = self.horizontalSlider_4.value()
        us = self.horizontalSlider_5.value()
        uv = self.horizontalSlider_6.value()
        data = [lh, ls, lv, uh, us, uv]
        pg.data_entry(namepg, data)
        pg.conn.commit()
        message = namepg + " save Ok"
        QMessageBox.about(self, "Save", message)
        name2 = pg.get_all_nameTableDB()
        self.cbb_Program.clear()
        self.cbb_Program.addItems(name2[::-1])

        self.cbb_Mauthu1.clear()
        self.cbb_Mauthu1.addItems(name2[::-1])
        self.cbb_Mauthu2.clear()
        self.cbb_Mauthu2.addItems(name2[::-1])
        self.cbb_Mauthu3.clear()
        self.cbb_Mauthu3.addItems(name2[::-1])
        self.loadDataOnGui(namepg)
    def btn_Delete(self):
        name1 = self.cbb_Program.currentText()
        pg.del_and_update(name1)
        self.cbb_Program.clear()
        name2 = pg.get_all_nameTableDB()
        self.cbb_Program.addItems(name2[::-1])
        self.loadDataOnGui(name2[0])

    def loadDataOnGui(self, name):
        global data
        data = pg.read_from_db(name)
        self.horizontalSlider.setValue(data[0][0])
        self.horizontalSlider_2.setValue(data[0][1])
        self.horizontalSlider_3.setValue(data[0][2])
        self.horizontalSlider_4.setValue(data[0][3])
        self.horizontalSlider_5.setValue(data[0][4])
        self.horizontalSlider_6.setValue(data[0][5])
        self.label_16.setText(str(data[0][0]))
        self.label_17.setText(str(data[0][1]))
        self.label_18.setText(str(data[0][2]))
        self.label_19.setText(str(data[0][3]))
        self.label_20.setText(str(data[0][4]))
        self.label_21.setText(str(data[0][5]))
        # except:
        #     QMessageBox.about(self, "Load Error", "File name no found!")

    def LoadLoc(self):
        global dataLoc
        namepg = self.cbb_Program.currentText()
        try:
            self.loadDataOnGui(namepg)
        except:
            print("error")

def BoLoc(data, img):
    phathien = False
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if w.sttCheckBox:
        lh = w.horizontalSlider.value()
        ls = w.horizontalSlider_2.value()
        lv = w.horizontalSlider_3.value()
        uh = w.horizontalSlider_4.value()
        us = w.horizontalSlider_5.value()
        uv = w.horizontalSlider_6.value()
    else:
        lh = (data[0][0])
        ls = (data[0][1])
        lv = (data[0][2])
        uh = (data[0][3])
        us = (data[0][4])
        uv = (data[0][5])
    res = cv2.inRange(hsv, (lh, ls, lv), (uh, us, uv))
    mask = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    # loai bo cac diem den trong doi tuong
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # tim doi tuong
    _, cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # neu co doi tuong
    if len(cnts) > 0:

        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        # # print co bao nhieu doi tuong
        # print(len(cnts))
        # quet tat ca cac doi tuong
        for i in range(0, len(cnts)):
            c = cnts[i]
            # xuat ra toa do x,y va tam cua duong tron bao quanh duong vien
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size

            if radius > 1:
                # draw the circle and centroid on the frame,
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 1)
                cv2.circle(img, (int(x), int(y)), 3, (0, 0, 255), -1)
                cv2.putText(img, str(i) + "pos: ", (center[0] + 10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                            (0, 0, 255),
                            1)
                cv2.putText(img, "(" + str(int(x)) + "," + str(int(y)) + ")", (center[0] + 10, center[1] + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                # cv2.rectangle(img, (270, 215), (270 + 50, 215 + 30), (0, 255, 0), 2)
                phathien = True

    return mask, phathien

def LoadDataOnGui(name):
    # tao ket noi sql
    conn = sqlite3.connect('data.db')

    # khoi tao con tro
    c = conn.cursor()
    sql = '''SELECT * FROM settingLoc where name = ''' +"'" + name + "'"
    print(sql)
    c.execute(sql)
    data = c.fetchall()
    print(data)
    c.close()
    conn.close()

    # load Loc1
    w.horizontalSlider.setValue(data[0][1])
    w.horizontalSlider_2.setValue(data[0][2])
    w.horizontalSlider_3.setValue(data[0][3])
    w.horizontalSlider_4.setValue(data[0][4])
    w.horizontalSlider_5.setValue(data[0][5])
    w.horizontalSlider_6.setValue(data[0][6])
    w.label_16.setText(str(data[0][1]))
    w.label_17.setText(str(data[0][2]))
    w.label_18.setText(str(data[0][3]))
    w.label_19.setText(str(data[0][4]))
    w.label_20.setText(str(data[0][5]))
    w.label_21.setText(str(data[0][6]))

def cam1():
    # cam = cv2.VideoCapture(0)
    while True:
        if w.sttStart:
            ret, img = w.cam.read()
            mask, _ = BoLoc(data, img)
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
            # get frame infos
            height, width, channel = frame.shape
            step = channel * width
            # create QImage from RGB frame
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            w.lb_Cam.setPixmap(QPixmap.fromImage(qImg))
            w.lb_Cam_2.setPixmap(QPixmap.fromImage(qImg))
            if w.sttCheckBox:
                cv2.imshow("Mask 1", mask)
                cv2.waitKey(1)
            else:
                cv2.destroyWindow("Mask 1")
        else:
            time.sleep(1)
            pass

        # time.sleep(0.01)

def AppLose():
    print("AppClose")
    w.sttStart = 0
    w.cam.release()
    g2.close()
if __name__ == "__main__":
    # khoi tao app
    app = QtWidgets.QApplication([])
    # load UI
    w = window("main.ui")
    # LoadDataOnGui('Co Chi')
    app.aboutToQuit.connect(AppLose)
    app.exec()
