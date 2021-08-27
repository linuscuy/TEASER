import os

from PySide2 import QtWidgets, QtGui, QtCore




def screenSizer(self, posx, posy, width, height, app):
    """func to get size of screen and scale window accordingly"""
    sizefactor = round(app.primaryScreen().size().height()*0.001)              # factor for scaling window, depending on height
    posx *= sizefactor
    posy *= sizefactor
    width *= sizefactor
    height *= sizefactor
    return posx, posy, width, height, sizefactor

def windowSetup(self, posx, posy, width, height, pypath, title, winFac = 1):
    """func for loading icon, setting size and title"""
    try:                                                                            # try to load e3d Icon
        self.setWindowIcon(QtGui.QIcon(os.path.join(pypath, r'pictures\e3dIcon.png')))
    except:
        print('error finding file icon')
    self.setGeometry(posx, posy, width * winFac, height * winFac)                   # setting window size
    self.setFixedSize(width * winFac, height * winFac)                                                # fixing window size
    self.setWindowTitle(title)                                                      # setting title



def divider ():
    div = QtWidgets.QLabel ('')
    div.setStyleSheet ("QLabel {background-color: #3e3e3e; padding: 0; margin: 0; border-bottom: 1 solid #666; border-top: 0 solid #2a2a2a;}")
    div.setMaximumHeight(1)
    return div