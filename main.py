from PyQt5 import QtWidgets, uic
import time
import threading
import cv2
import g2
g2.com("com1")
g2.open()
import sqlite3
import numpy as np

kernel = np.ones((5, 5), np.uint8)
# ct con chuyen led = [1,...,1] sang cmd co dang A*dataA*B*dataB* de gui xuong
def led2cmd(led):
    # chuyen doi led = [1,...,1] sang str '1...1'
    def list2str(list):
        # Converting integer led to string led
        s = [str(i) for i in list]
        # Join led items using join()
        res = str("".join(s))
        return res

    # tach du lieu cua led ra thanh ledA, ledB
    ledA = led[0:8]
    ledB = led[8:16]
    # chuyen list sang bin str co dang '11111111'
    binA = list2str(ledA)
    binB = list2str(ledB)
    # print(binA, binB)
    # chuyen bin sang int
    dataA = int(binA, 2)
    dataB = int(binB, 2)
    cmd = "A" + str(dataA) + "B" + str(dataB) + "*"
    return cmd

class window(QtWidgets.QMainWindow):
    sttStart = 0
    sttCheckBox = 0
    def __init__(self, nameUi):
        QtWidgets.QWidget.__init__(self)
        # load giao dien
        uic.loadUi(nameUi, self)
        self.btnStart.clicked.connect(self.btn_Start)
        self.btnSave.clicked.connect(self.btn_Save)
        self.comboBox.currentTextChanged.connect(self.LoadLoc)
        self.checkBox.stateChanged.connect(self.check_Box)
        self.show()

    def check_Box(self, state):
        if state:
            self.sttCheckBox = 1
            self.btnSave.setEnabled(True)
        else:
            self.btnSave.setEnabled(False)
            self.sttCheckBox = 0


    def btn_Start(self):
        if self.sttStart:
            self.sttStart = 0
            self.btnStart.setText("Start")
            self.btnStart.setStyleSheet("background-color: green")
        else:
            self.sttStart = 1
            Tcam1 = threading.Thread(target=cam1, name='thread 1')
            Tcam1.start()
            self.btnStart.setText("Stop")
            self.btnStart.setStyleSheet("background-color: red")

    def btn_Save(self):
        select = self.comboBox.currentText()
        SaveDataLoc(select)

    def LoadLoc(self):
        global dataLoc
        select = self.comboBox.currentText()
        LoadDataOnGui(select)
        dataLoc = getDataLoc(select)

def getDataLoc(name):
    # name la ten cua bo loc vd: Loc1
    conn = sqlite3.connect('data.db')
    # khoi tao con tro
    c = conn.cursor()
    sql = '''SELECT * FROM settingLoc where name = ''' + "'" + name + "'"
    print(sql)
    c.execute(sql)
    dataLoc = c.fetchall()
    c.close()
    conn.close()
    return dataLoc

def BoLoc(dataLoc, img,led):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if w.sttCheckBox:
        lh = w.horizontalSlider.value()
        ls = w.horizontalSlider_2.value()
        lv = w.horizontalSlider_3.value()
        uh = w.horizontalSlider_4.value()
        us = w.horizontalSlider_5.value()
        uv = w.horizontalSlider_6.value()
    else:
        lh = (dataLoc[0][1])
        ls = (dataLoc[0][2])
        lv = (dataLoc[0][3])
        uh = (dataLoc[0][4])
        us = (dataLoc[0][5])
        uv = (dataLoc[0][6])
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
            if radius > 10:

                # draw the circle and centroid on the frame,
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 1)
                cv2.circle(img, (int(x), int(y)), 3, (0, 0, 255), -1)
                cv2.putText(img, str(i) + "pos: ", (center[0] + 10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                            (0, 0, 255),
                            1)
                cv2.putText(img, "(" + str(int(x)) + "," + str(int(y)) + ")", (center[0] + 10, center[1] + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                ax = 0
                ay = 0
                # chieu rong cua phan vung kich
                aw = 40
                # chieu cao cua phan vung kich
                ah = 480
                # gom co 16 phan vung kich
                for a in range(16):
                    # neu nam trong vung doi tuong thi
                    if x > ax and x < ax + aw and y > ay and y < ay + ah:
                        # ve hinh vuong vung doi tuong
                        # cv2.rectangle(img, (ax, ay), (ax + aw, ay + ah), (255, 0, 0), 2)
                        # luu gia tri led vao list led, 0 co nghia la sang led
                        led[a] = 0
                    # toa do ax cua phan vung tiep theo
                    ax += 40
        # data = led2cmd(led)
        # g2.send(data)
        cv2.putText(img, '(0,0)', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.line(img, (50, 50), (50, 100), (0, 0, 255), 2)
        cv2.line(img, (50, 50), (100, 50), (0, 0, 255), 2)
        # cv2.imshow("Orgin", img)
        # cv2.imshow("Mask", mask)
        # cv2.waitKey(1)
    return led, mask

# khoi tao data cho bo loc ban dau
dataLoc1 = getDataLoc('Loc1')
dataLoc2 = getDataLoc('Loc2')
dataLoc3 = getDataLoc('Loc3')

def cam1():
    global dataLoc
    cam = cv2.VideoCapture(0)
    while w.sttStart:
        # fps1 = time.time()
        led = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        _, img = cam.read()

        led1, _ = BoLoc(dataLoc1, img, led)
        led2, mask2 = BoLoc(dataLoc2, img, led1)

        cv2.imshow("Orgin 1", img)
        cv2.imshow("Mask 1", mask2)

        data = led2cmd(led1)
        # # # print(data)
        g2.send(data)
        # fps = 1/(time.time() - fps1)
        # print(fps)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    print("DestroyAllWindow")

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

def SaveDataLoc(name):
    # tao ket noi
    conn = sqlite3.connect('data.db')

    # khoi tao con tro
    c = conn.cursor()

    lh = w.horizontalSlider.value()
    ls = w.horizontalSlider_2.value()
    lv = w.horizontalSlider_3.value()

    uh = w.horizontalSlider_4.value()
    us = w.horizontalSlider_5.value()
    uv = w.horizontalSlider_6.value()

    c.execute('''UPDATE settingLoc 
                    SET lh = ?,ls = ?, lv = ?, uh = ?, us = ?, uv = ?  
                    where name = ?''',(lh,ls,lv,uh,us,uv,name))
    conn.commit()
    print("Save ok")
    c.close()
    conn.close()

    global  dataLoc1, dataLoc2, dataLoc3
    # update data
    dataLoc1 = getDataLoc('Loc1')
    dataLoc2 = getDataLoc('Loc2')
    dataLoc3 = getDataLoc('Loc3')

def AppLose():
    print("AppClose")
    w.sttStart = 0

if __name__ == "__main__":

    # khoi tao app
    app = QtWidgets.QApplication([])
    # load UI
    w = window("main.ui")
    LoadDataOnGui('Loc1')
    # Tcam1 = threading.Thread(target=cam1, name='thread 1')
    # Tcam1.start()
    app.aboutToQuit.connect(AppLose)
    app.exec()