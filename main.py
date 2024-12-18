import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
import json
import random
import requests

# Custom QLabel class
class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Define a signal

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit the clicked signal

# Load the UI file
FormClass, _ = uic.loadUiType("Lotteries.ui")
global drawnumbers
drawnumbers = []

global data

global lotto

pr = ""

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
                print(url)
                global lotto
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

class LottoDrawings():
    def __init__(self, rangenum, drawingnum, same, drawnumbers):
        self.rangenum = rangenum
        self.drawingnum = drawingnum
        self.same = same
        self.drawnumbers = drawnumbers

        def PrintStatus():
            print("|\r", end="")
            print("/\r", end="")
            print("|\r", end="")
            print("\\\r", end="")
            print("|\r", end="")
            print("/\r", end="")

        def PickLottoNumbers(samenumber, total):
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

                for pan in data:

                    PrintStatus()

                    hit = 0

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
                                File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False

                    #Grande Vie Drawings
                    elif lotto == 3:

                        if numbers[0] == int(pan["p1"]) and numbers[1] == int(pan["p2"]) \
                        and numbers[2] == int(pan["p3"]) and numbers[3] == int(pan["p4"])\
                        and numbers[4] == int(pan["p5"]):
                            PickNumbers = True
                            File.write(pan["Drawdate"] + ", ")
                            hits = +1
                        else:
                            PickNumbers = False

                        if numbers[0] == int(pan["p1"]) and numbers[1] == int(pan["p2"]) \
                        and numbers[2] == int(pan["p3"]) and numbers[3] == int(pan["p4"]) \
                        and numbers[4] == int(pan["p5"]) and numbers[5] == int(pan["gn"]):
                            PickNumbers = True
                            File.write(pan["Drawdate"] + ", ")
                            hits = +1
                        else:
                            PickNumbers = False

                        for num in range(0, 5):
                            if numbers[num] == int(pan["p1"]) or numbers[num] == int(pan["p2"]) \
                            or numbers[num] == int(pan["p3"]) or numbers[num] == int(pan["p4"]):
                                hit += 1
                            if hit == 2:
                                PickNumbers = True
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
                                File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False


class MyWindow(QtWidgets.QMainWindow, FormClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Find the QLabel by its name (img649)
        self.img649 = self.findChild(QLabel, 'img649')
        self.imgLottoMax = self.findChild(QLabel, 'imgLottoMax')
        self.imgGrandeVie = self.findChild(QLabel, 'imgGrandeVie')
        self.imgToutouRien = self.findChild(QLabel, 'imgToutouRien')
        self.lblResults = self.findChild(QLabel, 'lblResults') # Find the lblResults label

        # Create an instance of ClickableLabel and bind it to the QLabel
        self.clickable_img649 = ClickableLabel(self.img649.parent())
        self.clickable_img649.setObjectName('img649')
        self.clickable_img649.setGeometry(self.img649.geometry())
        self.clickable_img649.setPixmap(self.img649.pixmap())
        self.clickable_img649.setScaledContents(True)

        self.clickable_imgLottoMax = ClickableLabel(self.imgLottoMax.parent())
        self.clickable_imgLottoMax.setObjectName('imgLottoMax')
        self.clickable_imgLottoMax.setGeometry(self.imgLottoMax.geometry())
        self.clickable_imgLottoMax.setPixmap(self.imgLottoMax.pixmap())
        self.clickable_imgLottoMax.setScaledContents(True)

        self.clickable_imgGrandeVie = ClickableLabel(self.imgGrandeVie.parent())
        self.clickable_imgGrandeVie.setObjectName('imgGrandeVie')
        self.clickable_imgGrandeVie.setGeometry(self.imgGrandeVie.geometry())
        self.clickable_imgGrandeVie.setPixmap(self.imgGrandeVie.pixmap())
        self.clickable_imgGrandeVie.setScaledContents(True)

        self.clickable_imgToutouRien = ClickableLabel(self.imgToutouRien.parent())
        self.clickable_imgToutouRien.setObjectName('imgToutouRien')
        self.clickable_imgToutouRien.setGeometry(self.imgToutouRien.geometry())
        self.clickable_imgToutouRien.setPixmap(self.imgToutouRien.pixmap())
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

    def on_649image_click(self):
        Lotto=LottoChoose(1)
        print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults

    def on_LottoMaximage_click(self):
        Lotto=LottoChoose(2)
        print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults

    def on_GrandeVieimage_click(self):
        Lotto=LottoChoose(3)
        print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults    

    def on_ToutouRienimage_click(self):
        Lotto=LottoChoose(4)
        print(Lotto)
        self.lblResults.setText(Lotto) # Update the text of lblResults        

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
