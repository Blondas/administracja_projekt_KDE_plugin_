import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import urllib


class Form:
    def __init__(self):
        self.app = QApplication(sys.argv)

        win = QWidget()
        layout = QGridLayout(win)

        self.sudoPasswordField = QLineEdit()
        self.sudoPasswordField.setObjectName("sudo_password")
        self.sudoPasswordField.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sudoPasswordField)

        self.wpaUserField = QLineEdit()
        self.wpaUserField.setObjectName("wpa_user")
        layout.addWidget(self.wpaUserField)

        self.wpaPasswordField = QLineEdit()
        self.wpaPasswordField.setObjectName("wpa_password")
        self.wpaPasswordField.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.wpaPasswordField)

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
        Certificate.downloadCertificate(Certificate, self.sudoPasswordField.text())
        wpa_supplicant = Wpa_supplicant(self.wpaUserField.text(), self.wpaPasswordField.text())
        wpa_supplicant.insertEntry(self.sudoPasswordField.text())



class Certificate:
    urlHandler = urllib.URLopener()
    certificateUrl = "https://panel.agh.edu.pl/CA-AGH/CA-AGH.der"
    certificateFile = "/usr/local/share/ca-certificates/CA-AGH.cer"


    @staticmethod
    def downloadCertificate(self, sudo_password):
        temp_file = "/tmp/etc_hosts.tmp"

        self.urlHandler.retrieve(self.certificateUrl, temp_file)

        command_mv = "echo " + str(sudo_password) + "| sudo -S -k mv " + temp_file + " " + self.certificateFile

        # with open(os.devnull, 'wb') as devnull:
        #     subprocess.check_call([command_mv], stdo    @staticmethodut=devnull, stderr=subprocess.STDOUT)
        os.system(command_mv)


    @staticmethod
    def reloadCertificates(sudo_password):
        command = "echo " + str(sudo_password) + "| sudo -S -k update-ca-certificates"
        os.system(command)



class Wpa_supplicant:
    supplicant_conf_file = "/etc/wpa_supplicant/agh_wpa.conf"

    def __init__(self, user, password):
        self.wpa_supplicant_entry = """
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=wheel
network={
    ssid="example"
    scan_ssid=1
    key_mgmt=WPA-EAP
    eap=PEAP
    identity="USER"
    password="PASSWORD"
    ca_cert="/usr/local/share/ca-certificates/CA-AGH.cer"
    phase1="peaplabel=0"
    phase2="auth=MSCHAPV2"
}
        """

        self.wpa_supplicant_entry = self.wpa_supplicant_entry.replace("USER", user)
        self.wpa_supplicant_entry = self.wpa_supplicant_entry.replace("PASSWORD", password)


    def insertEntry(self, sudo_password):
        # write to temp file:
        temp = "/tmp/wpa_supplicant.tmp"
        temp_file = open(temp, "w")
        temp_file.write(self.wpa_supplicant_entry)
        temp_file.close()

        command_mv = "echo " + str(sudo_password) + "| sudo -S -k mv " + temp + " " + self.supplicant_conf_file
        os.system(command_mv)




form = Form()



