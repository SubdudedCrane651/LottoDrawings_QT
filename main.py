import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal

# Custom QLabel class
class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Define a signal

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit the clicked signal

# Load the UI file
FormClass, _ = uic.loadUiType("Lotteries.ui")

class MyWindow(QtWidgets.QMainWindow, FormClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Find the QLabel by its name (img649)
        self.img649 = self.findChild(QLabel, 'img649')

        # Set the correct path to your image file
        image_path = 'images/649.png'
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Image not found at {image_path}")
        else:
            # Set pixmap directly if the label is already created in the UI file
            self.img649.setPixmap(pixmap)
            self.img649.setScaledContents(True)

            # Create an instance of ClickableLabel and bind it to the QLabel
            self.clickable_img649 = ClickableLabel(self.img649.parent())
            self.clickable_img649.setObjectName('img649')
            self.clickable_img649.setGeometry(self.img649.geometry())
            self.clickable_img649.setPixmap(self.img649.pixmap())
            self.clickable_img649.setScaledContents(True)

            # Replace the QLabel with ClickableLabel
            layout = self.img649.parent().layout()
            if layout is not None:
                layout.replaceWidget(self.img649, self.clickable_img649)
                self.img649.deleteLater()  # Remove the old QLabel

            # Connect the clicked signal to a slot function
            self.clickable_img649.clicked.connect(self.on_image_click)

    def on_image_click(self):
        print("Image clicked!")

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
