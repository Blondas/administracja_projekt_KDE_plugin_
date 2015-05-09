import os
import stat
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import urllib
import re


class Sudo:
    command = ""

    @staticmethod
    def setCommand(sudo_user):
        Sudo.command = sudo_command = "echo " + str(sudo_user) + "| sudo -S -k "



class Form:
    def __init__(self):
        self.app = QApplication(sys.argv)

        win = QWidget()
        layout = QGridLayout(win)


        self.sudoPasswordField = QLineEdit()
        self.sudoPasswordField.setObjectName("sudo_password")
        self.sudoPasswordField.setEchoMode(QLineEdit.Password)
        self.sudoPasswordField.setPlaceholderText("linux user password")
        layout.addWidget(self.sudoPasswordField)

        self.wpaUserField = QLineEdit()
        self.wpaUserField.setObjectName("wpa_user")
        self.wpaUserField.setPlaceholderText("wpa user")
        layout.addWidget(self.wpaUserField)

        self.wpaPasswordField = QLineEdit()
        self.wpaPasswordField.setObjectName("wpa_password")
        self.wpaPasswordField.setPlaceholderText("wpa password")
        self.wpaPasswordField.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.wpaPasswordField)

        self.button_connect = QPushButton(win)
        self.button_connect.setText("Install AGH certificate")
        layout.addWidget(self.button_connect)

        self.button_fix = QPushButton(win)
        self.button_fix.setText("Fix/reconnect to  your current wifi connection")
        layout.addWidget(self.button_fix)

        self.button_exit = QPushButton(win)
        self.button_exit.setText("exit")
        layout.addWidget(self.button_exit)


        # Connect buttons to actions
        QObject.connect(self.button_connect, SIGNAL("clicked()"), self.button_connectAction)
        QObject.connect(self.button_fix, SIGNAL("clicked()"), self.button_fixAction)
        QObject.connect(self.button_exit, SIGNAL("clicked()"), self.app.exit)

        win.show()

        # Start the evnt loop
        sys.exit(self.app.exec_())


    def button_connectAction(self):
        # create sudo command:
        Sudo.setCommand(self.sudoPasswordField.text())

        # download and save certificate:
        Certificate.downloadCertificate(Certificate)

        # update wpa_suppclicant config file:
        wpa_supplicant = Wpa_supplicant(self.wpaUserField.text(), self.wpaPasswordField.text())
        wpa_supplicant.insertEntry()

        # restart wpa_supplicant:
        NetworkManager.stop(NetworkManager)
        wpa_supplicant.restartWpaSupplicant()

        # refresh DHCP:
        Dhcp.configureDHCP(Dhcp)


    def button_fixAction(self):
        Sudo.setCommand(self.sudoPasswordField.text())

        Wpa_supplicant.kill(Wpa_supplicant)
        NetworkManager.start(NetworkManager)



class Certificate:
    urlHandler = urllib.URLopener()

    certificateUrl = "https://panel.agh.edu.pl/CA-AGH/CA-AGH.der"
    certificateFile = "/usr/local/share/ca-certificates/CA-AGH.der"


    @staticmethod
    def downloadCertificate(self):
        temp_file = "/tmp/etc_hosts.tmp"

        if not os.path.isfile(self.certificateFile):
            # download certificate and save to temp file:
            self.urlHandler.retrieve(self.certificateUrl, temp_file)

            # mv certificate to final location:
            command_mv = Sudo.command + "mv " + temp_file + " " + self.certificateFile
            os.system(command_mv)


    # NOT USED:
    @staticmethod
    def reloadCertificates(sudo_password):
        command = Sudo.command + "update-ca-certificates"
        os.system(command)



class Wpa_supplicant:
    supplicant_conf_file = "/etc/wpa_supplicant/wpa_supplicant.conf"

    def __init__(self, user, password):
        self.wpa_supplicant_entry = """
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


    def insertEntry(self):
        if os.path.isfile(self.supplicant_conf_file):
            # get file permissions, make file editable:
            # orig_permissions = oct(stat.S_IMODE(os.lstat(self.supplicant_conf_file).st_mode))
            orig_permissions = 666

            temp_permissions = 666
            chmod_command = Sudo.command + "chmod " + str(temp_permissions) + " " + self.supplicant_conf_file
            os.system(chmod_command)

            # replace AGH-WPA entry if exists or add entry:
            with open(self.supplicant_conf_file, 'r+') as myfile:
                data = myfile.read()
                pattern = 'network={.*?ssid="AGH-WPA".*?}'

                entry_exist = re.search(pattern, data, re.DOTALL)

                if entry_exist:
                    data = re.sub(pattern, self.wpa_supplicant_entry, data, re.DOTALL)

                else:
                    data += "\n" + self.wpa_supplicant_entry


            # save new/modified content to file:
            final_file = open(self.supplicant_conf_file, "w")
            final_file.write(data)
            final_file.close()


            # set file permissions back:
            chmod_command = Sudo.command + "chmod " + str(orig_permissions) + " " + self.supplicant_conf_file
            os.system(chmod_command)

        else:
            # write to temp file:
            temp = "/tmp/wpa_supplicant.tmp"
            temp_file = open(temp, "w")
            temp_file.write(self.wpa_supplicant_entry)
            temp_file.close()

            # move file to final location:
            move_command = Sudo.command + "mv " + temp + " " + self.supplicant_conf_file
            os.system(move_command)


    def restartWpaSupplicant(self):
        command = Sudo.command + "wpa_supplicant -iwlan0 -c" + self.supplicant_conf_file + " -B"
        os.system(command)

    @staticmethod
    def kill(self):
        command_fix = Sudo.command + "killall -w wpa_supplicant"
        os.system(command_fix)



class Dhcp:
    @staticmethod
    def configureDHCP(self):
        command = Sudo.command + "dhclient wlan0"
        os.system(command)



class NetworkManager:

    @staticmethod
    def start(self):
        command = Sudo.command + "start network-manager"
        os.system(command)

    @staticmethod
    def stop(self):
        command = Sudo.command + "stop network-manager"
        os.system(command)

    @staticmethod
    def restart(self):
        command = Sudo.command + "restart network-manager"
        os.system(command)




form = Form()



