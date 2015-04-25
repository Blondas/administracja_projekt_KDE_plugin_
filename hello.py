from subprocess import call
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import urllib





# Definitions:
def main():
    # Create a QApplication and QPushButton
    app = QApplication(sys.argv)

    win = QWidget()
    layout = QGridLayout(win)

    passwordField = QLineEdit()
    passwordField.setObjectName("sudoPassword")
    passwordField.setEchoMode(QLineEdit.Password)
    layout.addWidget(passwordField)

    button1 = QPushButton(win)
    button1.setText("Install AGH certificate")
    layout.addWidget(button1)

    button2 = QPushButton(win)
    button2.setText("exit")
    layout.addWidget(button2)



    # Connect buttons to actions
    QObject.connect(button1, SIGNAL("clicked()"), button1Action)
    QObject.connect(button2, SIGNAL("clicked()"), app.exit)

    win.show()


    # Start the evnt loop
    sys.exit(app.exec_())

def button1Action():
    print("")
    # downloadCertificate()

def downloadCertificate():
    certificateFile = urllib.URLopener()
    certificateFile.retrieve("https://panel.agh.edu.pl/CA-AGH/CA-AGH.der", "agh.cert")

def updateCertificate():
    call(["from subprocess import call", "-l"])

main()
downloadCertificate()





