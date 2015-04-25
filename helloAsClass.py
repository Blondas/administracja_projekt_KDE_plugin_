from subprocess import call
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import urllib

class Form:
    def __init__(self):
        self.app = QApplication(sys.argv)

        win = QWidget()
        layout = QGridLayout(win)

        self.passwordField = QLineEdit()
        self.passwordField.setObjectName("sudo_password")
        self.passwordField.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordField)

        self.button1 = QPushButton(win)
        self.button1.setText("Install AGH certificate")
        layout.addWidget(self.button1)

        self.button2 = QPushButton(win)
        self.button2.setText("exit")
        layout.addWidget(self.button2)


        # Connect buttons to actions
        QObject.connect(self.button1, SIGNAL("clicked()"), self.button1Action)
        QObject.connect(self.button2, SIGNAL("clicked()"), self.app.exit)

        win.show()


        # Start the evnt loop
        sys.exit(self.app.exec_())


    def button1Action(self):
        print(self.passwordField.text())




form = Form()



