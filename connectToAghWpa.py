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


        self.sudoPasswordField = QLineEdit("BNBB..bm")
        self.sudoPasswordField.setObjectName("sudo_password")
        self.sudoPasswordField.setEchoMode(QLineEdit.Password)
        self.sudoPasswordField.setPlaceholderText("linux user password")
        layout.addWidget(self.sudoPasswordField)

        self.wpaUserField = QLineEdit("mamoni@student.agh.edu.pl")
        self.wpaUserField.setObjectName("wpa_user")
        self.wpaUserField.setPlaceholderText("wpa user")
        layout.addWidget(self.wpaUserField)

        self.wpaPasswordField = QLineEdit("Lufynuh")
        self.wpaPasswordField.setObjectName("wpa_password")
        self.wpaPasswordField.setPlaceholderText("wpa password")
        self.wpaPasswordField.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.wpaPasswordField)

        self.button_connect = QPushButton(win)
        self.button_connect.setText("Install AGH certificate")
        layout.addWidget(self.button_connect)

        self.button_exit = QPushButton(win)
        self.button_exit.setText("exit")
        layout.addWidget(self.button_exit)


        # Connect buttons to actions
        QObject.connect(self.button_connect, SIGNAL("clicked()"), self.button_connectAction)
        QObject.connect(self.button_exit, SIGNAL("clicked()"), self.app.exit)

        win.show()

        # Start the evnt loop
        sys.exit(self.app.exec_())


    def button_connectAction(self):
        # download and save certificate:
        Certificate.downloadCertificate(Certificate, self.sudoPasswordField.text())

        # update wpa_suppclicant config file:
        wpa_supplicant = Wpa_supplicant(self.wpaUserField.text(), self.wpaPasswordField.text())
        wpa_supplicant.insertEntry(self.sudoPasswordField.text())

        # restart wpa_supplicant:
        wpa_supplicant.restartWpaSupplicant(self.sudoPasswordField.text())

        # refresh DHCP:
        Dhcp.configureDHCP(self.sudoPasswordField.text())



class Certificate:
    urlHandler = urllib.URLopener()

    certificateUrl = "https://panel.agh.edu.pl/CA-AGH/CA-AGH.der"
    certificateFile = "/usr/local/share/ca-certificates/CA-AGH.der"


    @staticmethod
    def downloadCertificate(self, sudo_password):
        temp_file = "/tmp/etc_hosts.tmp"

        # download certificate and save to temp file:
        self.urlHandler.retrieve(self.certificateUrl, temp_file)

        # mv certificate to final location:
        command_mv = "echo " + str(sudo_password) + "| sudo -S -k mv " + temp_file + " " + self.certificateFile
        os.system(command_mv)


    # NOT USED:
    @staticmethod
    def reloadCertificates(sudo_password):
        command = "echo " + str(sudo_password) + "| sudo -S -k update-ca-certificates"
        os.system(command)



class Wpa_supplicant:
    supplicant_conf_file = "/etc/wpa_supplicant/wpa_supplicant.conf"

    def __init__(self, user, password):
        self.wpa_supplicant_entry = """
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=wheel
network={
    ssid="AGH-WPA"
    scan_ssid=1
    key_mgmt=WPA-EAP
    eap=PEAP
    identity="USER"
    password="PASSWORD"
    ca_cert="CERTIFICATE_FILE"
    phase1="peaplabel=0"
    phase2="auth=MSCHAPV2"
}
        """

        self.wpa_supplicant_entry = self.wpa_supplicant_entry.replace("USER", user)
        self.wpa_supplicant_entry = self.wpa_supplicant_entry.replace("PASSWORD", password)
        self.wpa_supplicant_entry = self.wpa_supplicant_entry.replace("CERTIFICATE_FILE", Certificate.certificateFile)


    #TODO:
    def insertEntry(self, sudo_password):
        # if file doesn't exist:
        ## write to temp file:
        temp = "/tmp/wpa_supplicant.tmp"
        temp_file = open(temp, "w")
        temp_file.write(self.wpa_supplicant_entry)
        temp_file.close()

        ## move file to final location:


        # if file exists:
        ## get file permissions:

        ## chmod to 666

        ## if entry exists replace entry:

        ## if entry doesn't exist replace entry:

        ## change file permissions to original:


    def restartWpaSupplicant(self, sudo_password):
        command = "echo " + str(sudo_password) + "| sudo -S -k wpa_supplicant -wlan0 -c" + self.supplicant_conf_file
        os.system(command)



class Dhcp:
    def configureDHCP(self, sudo_password):
        command = "echo " + str(self, sudo_password) + "| sudo -S -k dhclient wlan0"
        os.system(command)



form = Form()



