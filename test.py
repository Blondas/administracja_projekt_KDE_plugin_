#!/usr/bin/env python

import sys

from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication, KMainWindow

from PyQt4.QtGui import QLabel

runner = True
        
helpText = """Program sluzacy do polaczenia sie z siecia AGH-WPA
"""        



class MainWindow (KMainWindow):
    def __init__ (self):
        KMainWindow.__init__ (self)

        self.resize (640, 480)
        label = QLabel ("This is a simple PyKDE4 program", self)
        # label.setGeometry (10, 10, 200, 40)

#--------------- main ------------------



if __name__ == '__main__':

    appName     = "KApplication"
    catalog     = ""
    programName = ki18n ("KApplication")
    version     = "1.0"
    description = ki18n ("AGH-WPA connect")
    license     = KAboutData.License_GPL
    copyright   = ki18n ("(c) 2014 Krzysiek Nowakowski, Krystian Ujma, Roger Barlik")
    text        = ki18n ("none")
    homePage    = "krisdrum.com"
    bugEmail    = "n.krzysiek@gmail.com"
    
    aboutData   = KAboutData (appName, catalog, programName, version, description,
                                license, copyright, text, homePage, bugEmail)
    
        
    KCmdLineArgs.init (sys.argv, aboutData)
        
    app = KApplication ()
    mainWindow = MainWindow ()



    mainWindow.show ()
    app.exec_ ()