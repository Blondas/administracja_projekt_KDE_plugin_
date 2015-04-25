import os
from subprocess import call
import subprocess
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import urllib

class Form:
    def __init__(self):
        self.app = QApplication(sys.argv)

        win = QWidget()
        layout = QGridLayout(win)

        self.button1 = QPushButton(win)
        self.button1.setText("Install AGH certificate")
        layout.addWidget(self.button1)

        self.passwordField = QLineEdit()
        self.passwordField.setObjectName("sudo_password")
        self.passwordField.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordField)

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
        Certificate.downloadCertificate(Certificate, self.passwordField.text())




class Certificate:
    urlHandler = urllib.URLopener()
    certificateUrl = "https://panel.agh.edu.pl/CA-AGH/CA-AGH.der"
    certificateFile = "/usr/local/share/ca-certificates/CA-AGH.der"


    @staticmethod
    def downloadCertificate(self, sudo_password):
        temp_file = "/tmp/etc_hosts.tmp"

        self.urlHandler.retrieve(self.certificateUrl, temp_file)

        command_mv = "echo " + str(sudo_password) + "| sudo -S -k mv " + temp_file + " " + self.certificateFile

        # with open(os.devnull, 'wb') as devnull:
        #     subprocess.check_call([command_mv], stdout=devnull, stderr=subprocess.STDOUT)
        os.system(command_mv)


    @staticmethod
    def reloadCertificates(sudo_password):
        command = "echo " + str(sudo_password) + "| sudo -S -k update-ca-certificates"
        os.system(command)



form = Form()



