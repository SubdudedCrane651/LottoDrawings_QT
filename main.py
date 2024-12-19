import sys,os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel,QMessageBox,QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal,QTimer,QObject
import json,time
import random
import requests

#logging.basicConfig(level=logging.DEBUG)

# Custom QLabel class
class ClickableLabel(QLabel):
    global label_global
    clicked = pyqtSignal()  # Define a signal

    def __init__(self, parent=None):
        global label_global
        super().__init__(parent)

    def mousePressEvent(self, event):
        global label_global
        self.clicked.emit()  # Emit the clicked signal

# Load the UI file
global drawnumbers
drawnumbers = []

global data

global lotto

timer_global = None

global_label = None

pr = ""

def stop_timer():
     global timer_global
     if timer_global and timer_global.isActive():
         timer_global.stop()

def PrintText():
    global timer_global
    print("|\r", end="")
    print("/\r", end="")
    print("|\r", end="")
    print("\\\r", end="")
    print("|\r", end="")
    print("/\r", end="")
  
def PrintStatus(count2):
            #pass
            global label_global
            global reset

            if label_global:
                if count2==0:
                    label_global.setText("<p>Picking </p>")
                    reset=True
                elif count2==1:    
                    label_global.setText("<p>Picking .</p>")
                elif count2==2:    
                    label_global.setText("<p>Picking ..</p>")
                elif count2==3:    
                    label_global.setText("<p>Picking ...</p>")
                elif count2==4:    
                    label_global.setText("<p>Picking ....</p>")
                elif count2==5:    
                    label_global.setText("<p>Picking ......</p>")
                    reset=False

def choose(i):
    switcher = {
        1: 'Lotto649.json',
        2: 'LottoMax.json',
        3: 'Grande_Vie.json',
        4: 'ToutouRien.json'
    }
    return switcher.get(i, 'Invalid Number')

def LottoChoose(choice):
    try:
                jsonfile = choose(choice)
                url = "https://richard-perreault.com/Documents/" + jsonfile
                #print(url)
                global lotto
                global label_global
                global timer_global
                global Stop
                lotto=int(choice)
                response = requests.get(url)
                global data
                data = json.loads(response.text)
                global count
                count = len(data)
                #Lotto 6/49 Drawings
                global drawnumbers
                global pr
                if lotto == 1:
                    lottonumbers = LottoDrawings(7, 49, -5, drawnumbers)
                    pr = "<p>The winning 6/49 numbers are <br>" + str(
                        lottonumbers.drawnumbers) + "<br>in a total of " + str(
                            count) + " drawings</p>"

                #Lotto Max Drawings
                if lotto == 2:
                    lottonumbers = LottoDrawings(8, 50, -6, drawnumbers)
                    pr = "<p>The Lotto Max winning numbers are <br>" + str(
                        lottonumbers.drawnumbers) + "<br>in a total of " + str(
                            count) + " drawings</p>"

                #Grande Vie Drawings
                if lotto == 3:
                    lottonumbers = LottoDrawings(6, 49, -4, drawnumbers)
                    pr = "<p>The winning Grande Vie numbers are <br>" + str(
                        lottonumbers.drawnumbers) + "<br>in a total of " + str(
                            count) + " drawings</p>"

                #Tout ou rien Drawings
                if lotto == 4:
                    lottonumbers = LottoDrawings(13, 24, -11, drawnumbers)
                    pr = "<p>The winning Tout ou rien numbers are <br>" + str(
                        lottonumbers.drawnumbers) + "<br>in a total of " + str(
                            count) + " drawings</p>"
    except Exception as e:
                #errors.append(
                #    "Unable to get URL. Please make sure it's valid and try again."
                #)
                print(f"An unexpected error occurred: {e}")
                error_code = e.args[0] # If the error has additional arguments
                print(f"Error code: {error_code}")

    
    print(pr)
    return pr

class LottoDrawings(QObject):
    update_label_signal = pyqtSignal(int)
    computation_done_signal = pyqtSignal(str)

    def __init__(self, rangenum, drawingnum, same, drawnumbers):
        super().__init__()
        self.rangenum = rangenum
        self.drawingnum = drawingnum
        self.same = same
        self.drawnumbers = drawnumbers
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_data)

        stop_timer()

        # Connect the signals to their respective slots
        self.update_label_signal.connect(self.update_label_text)
        #self.computation_done_signal.connect(self.computation_done)

        def PickLottoNumbers(samenumber, total):
            global label_global,Stop
            samenumber = 1
            count2 = 0
            for number in numbers:
                if numbers[count2 - 1] == number and count2 != 0:
                    rnd = random.randint(1, total)
                    numbers[count2] = rnd
                    rnd = random.randint(1, total)
                    samenumber += 1
                else:
                    samenumber -= 1
                count2 += 1
                numbers.sort()
            return numbers, samenumber

        PickNumbers = True

        hits = 0
        

        while PickNumbers or hits > 0:

            global label_global,Stop

            numbers = []

            hits = 0

            for count in range(1, rangenum):
                rnd = random.randint(1, drawingnum)
                samenumber = 0
                numbers2 = PickLottoNumbers(samenumber, drawingnum)
                numbers2[0].append(rnd)
                numbers2[0].sort()
                samenumber = 0
            while samenumber != same:
                numbers2 = PickLottoNumbers(samenumber, drawingnum)
                samenumber = numbers2[1]
            numbers = numbers2[0]

            if same == -4:
                rnd = random.randint(1, 6)
                numbers.append(rnd)

            self.drawnumbers = numbers

            with open("LottoDrawings.txt", 'w+') as File:
                global label_global,timer_global

                global reset
                reset=True
                count2=0

                for pan in data:

                    #PrintText()

                    #PrintStatus(count2)

                    hit = 0

                    count2+=1

                    if not reset:
                        count2=0
                    
                    #Lotto 6/49 Drawings
                    if lotto == 1:

                        for num in range(0, 6):
                            if numbers[num] == int(pan["P1"]) or numbers[num] == int(pan["P2"]) \
                            or numbers[num] == int(pan["P3"]) or numbers[num] == int(pan["P4"]) \
                            or numbers[num] == int(pan["P5"]) or numbers[num] == int(pan["P6"]) \
                            or numbers[num] == int(pan["P7"]):
                                hit += 1
                        if hit == 6:
                            PickNumbers = True
                            with open("LottoDrawings.txt", 'a+') as File:
                                File.write(pan["Drawdate"] + ", ")
                            hits += 1
                        else:
                            PickNumbers = False

                    #LottoMax Drawings
                    if lotto == 2:

                        for num in range(0, 7):
                            if numbers[num] == int(pan["P1"]) or numbers[num] == int(pan["P2"]) \
                            or numbers[num] == int(pan["P3"]) or numbers[num] == int(pan["P4"]) \
                            or numbers[num] == int(pan["P5"]) or numbers[num] == int(pan["P6"] \
                            or numbers[num] == int(pan["P7"])):
                                hit += 1
                            if hit == 4 or hit == 7:
                                PickNumbers = True
                                with open("LottoDrawings.txt", 'a+') as File:
                                    File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False

                    #Grande Vie Drawings
                    if lotto == 3:

                        for num in range(0, 5):
                            if numbers[num] == int(pan["p1"]) or numbers[num] == int(pan["p2"]) \
                            or numbers[num] == int(pan["p3"]) or numbers[num] == int(pan["p4"]) \
                            or numbers[num]==int(pan["p5"]):
                                hit += 1
                            if hit == 3 or hit==5: 
                                PickNumbers = True
                                with open("LottoDrawings.txt", 'a+') as File:
                                   File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False

                    #Tout ou Rien Drawings
                    if lotto == 4:
                        for num in range(0, 12):
                            if numbers[num] == int(pan["p1"]) or numbers[num] == int(pan["p2"]) \
                            or numbers[num] == int(pan["p3"]) or numbers[num] == int(pan["p4"]) \
                            or numbers[num] == int(pan["p5"]) or numbers[num] == int(pan["p6"]) \
                            or numbers[num] == int(pan["p7"]) or numbers[num] == int(pan["p8"]) \
                            or numbers[num] == int(pan["p9"]) or numbers[num] == int(pan["p10"]) \
                            or numbers[num] == int(pan["p11"]) or numbers[num] == int(pan["p12"]):
                                hit += 1
                            if hit == 12:
                                PickNumbers = True
                                with open("LottoDrawings.txt", 'a+') as File:
                                   File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False

    
    def start_timer(self):
        self.timer.start(100)  # Update every 100 milliseconds

    def stop_timer(self):
        self.timer.stop()

    def process_data(self):
        global reset, global_label                                

    def update_label_text(self, count2):
            global global_label
            if global_label:
                if count2 == 0:
                    global_label.setText("<p>Picking .</p>")
                    print("|\r", end="")
                elif count2 == 1:
                    global_label.setText("<p>Picking ..</p>")
                    print("/\r", end="")
                elif count2 == 2:
                    global_label.setText("<p>Picking ..</p>")
                    print("|\r", end="")
                elif count2 == 3:
                    global_label.setText("<p>Picking ...</p>")
                    print("\\\r", end="")
                elif count2 == 4:
                    global_label.setText("<p>Picking ....</p>")
                    print("|\r", end="")
                elif count2 == 5:
                    global_label.setText("<p>Picking ......</p>")
                    print("/\r", end="")                                
                                
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setupUi(self)
        global Stop

        try:
            #QMessageBox.information(self, "Debug", "Attempting to load UI file")
            ui_path = os.path.join(os.path.dirname(__file__), "Lotteries.ui")
            uic.loadUi(ui_path, self)
            #self.initUI()
            #QMessageBox.information(self, "Debug", "UI file loaded successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load UI file: {e}")


        # Find the QLabel by its name (img649)
        self.img649 = self.findChild(QLabel, 'img649')
        self.imgLottoMax = self.findChild(QLabel, 'imgLottoMax')
        self.imgGrandeVie = self.findChild(QLabel, 'imgGrandeVie')
        self.imgToutouRien = self.findChild(QLabel, 'imgToutouRien')
        global label_global,timer_global
        self.lblResults = self.findChild(QLabel, 'lblResults') # Find the lblResults label
        self.txtPicking = self.findChild(QLabel, 'txtPicking') # Find the lblResults label
        # label_global=QLabel("<p>Picking</p>",self)
        # font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        # label_global.setFont(font)
        # label_global.setFixedSize(300, 50)
        # Create an instance of ClickableLabel and bind it to the QLabel
        self.clickable_img649 = ClickableLabel(self.img649.parent())
        self.clickable_img649.setObjectName('img649')
        self.clickable_img649.setGeometry(self.img649.geometry())
        img649_path = os.path.join(os.path.dirname(__file__), "images", "649.png")
        pixmap=QtGui.QPixmap(img649_path)
        self.clickable_img649.setPixmap(pixmap)
        self.clickable_img649.setScaledContents(True)

        self.clickable_imgLottoMax = ClickableLabel(self.imgLottoMax.parent())
        self.clickable_imgLottoMax.setObjectName('imgLottoMax')
        self.clickable_imgLottoMax.setGeometry(self.imgLottoMax.geometry())
        imgLotto_Max_path = os.path.join(os.path.dirname(__file__), "images", "Lotto_Max.png")
        pixmap=QtGui.QPixmap(imgLotto_Max_path)
        self.clickable_imgLottoMax.setPixmap(pixmap)
        self.clickable_imgLottoMax.setScaledContents(True)

        self.clickable_imgGrandeVie = ClickableLabel(self.imgGrandeVie.parent())
        self.clickable_imgGrandeVie.setObjectName('imgGrandeVie')
        self.clickable_imgGrandeVie.setGeometry(self.imgGrandeVie.geometry())
        imgGrande_Vie_path = os.path.join(os.path.dirname(__file__), "images", "Grande_Vie.png")
        pixmap=QtGui.QPixmap(imgGrande_Vie_path)
        self.clickable_imgGrandeVie.setPixmap(pixmap)
        self.clickable_imgGrandeVie.setScaledContents(True)

        self.clickable_imgToutouRien = ClickableLabel(self.imgToutouRien.parent())
        self.clickable_imgToutouRien.setObjectName('imgToutouRien')
        self.clickable_imgToutouRien.setGeometry(self.imgToutouRien.geometry())
        imgTout_ou_rien_path = os.path.join(os.path.dirname(__file__), "images", "Tout_ou_rien.png")
        pixmap=QtGui.QPixmap(imgTout_ou_rien_path)
        self.clickable_imgToutouRien.setPixmap(pixmap)
        self.clickable_imgToutouRien.setScaledContents(True)

        # Replace the QLabel with ClickableLabel
        layout = self.img649.parent().layout()
        if layout is not None:
              layout.replaceWidget(self.img649, self.clickable_img649)
              self.img649.deleteLater()  # Remove the old QLabel

            # Connect the clicked signal to a slot function
        self.clickable_img649.clicked.connect(self.on_649image_click)

        layout = self.imgLottoMax.parent().layout()
        if layout is not None:
              layout.replaceWidget(self.imgLottoMax, self.clickable_imgLottoMax)
              self.imgLottoMax.deleteLater()  # Remove the old QLabel

            # Connect the clicked signal to a slot function
        self.clickable_imgLottoMax.clicked.connect(self.on_LottoMaximage_click)

        layout = self.imgGrandeVie.parent().layout()
        if layout is not None:
              layout.replaceWidget(self.imgGrandeVie, self.clickable_imgGrandeVie)
              self.imgGrandeVie.deleteLater()  # Remove the old QLabel

            # Connect the clicked signal to a slot function
        self.clickable_imgGrandeVie.clicked.connect(self.on_GrandeVieimage_click)

        layout = self.imgToutouRien.parent().layout()
        if layout is not None:
              layout.replaceWidget(self.imgToutouRien, self.clickable_imgToutouRien)
              self.imgToutouRien.deleteLater()  # Remove the old QLabel

            # Connect the clicked signal to a slot function
        self.clickable_imgToutouRien.clicked.connect(self.on_ToutouRienimage_click)

        #self.button = QPushButton("Start Animation", self)
        #layout.addWidget(self.button)
         # Connect the button's clicked signal to start the timer
        #self.button.clicked.connect(self.start_timer)

        timer_global = QTimer(self) 
        timer_global.timeout.connect(self.update_status)
        self.counter = 0

    def start_timer(self):
        timer_global.start(100) # Update every 100 milliseconds

    def stop_timer(self):
        timer_global.stop() # Stop the timeer    

    def update_status(self):
        PrintStatus(self.counter) 
        self.counter += 1 
        if self.counter > 6:
            self.counter = 0        

    def on_649image_click(self):
        #self.start_timer()
        self
        Lotto=LottoChoose(1)
        #print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults

    def on_LottoMaximage_click(self):
        #self.start_timer()
        Lotto=LottoChoose(2)
        #print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults

    def on_GrandeVieimage_click(self):
        #self.start_timer()
        Lotto=LottoChoose(3)
        #print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults

    def on_ToutouRienimage_click(self):
        #self.start_timer()
        Lotto=LottoChoose(4)
        #print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
