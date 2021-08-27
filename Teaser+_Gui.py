# -*- coding: utf-8 -*-
"""
The GUI for TEASER+
Contact:
M.Sc. Avichal Malhotra: malhotra@e3d.rwth-aachen.de
B.Sc. Maxim Shamovich: maxim.shamovich@rwth-aachen.de


www.e3d.rwth-aachen.de
Mathieustr. 30
52074 Aachen
"""

# import of libraries
import os
import sys
import PySide2
from PySide2 import QtWidgets, QtGui
import gui_functions as gf


# setting environment variable for PySide2
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


# positions and dimensions of window
posx = 275
posy = 100
width = 600
height = 350
sizefactor = 0
sizer = True

pypath = os.path.dirname(os.path.realpath(__file__))        # path of script


class mainWindow(QtWidgets.QWidget):
    def __init__(self):
        #initiate the parent
        super(mainWindow,self).__init__()
        self.initUI()


    def initUI(self):
        global posx, posy, width, height, sizefactor, sizer

        # setup of gui / layout
        if sizer:
            posx, posy, width, height, sizefactor = gf.screenSizer(self, posx, posy, width, height, app)
            sizer = False
        gf.windowSetup(self, posx, posy, width, height, pypath, 'TEASER+')

        #Setting main layout
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.vbox)

        #Setting Layout
        self.uGrid = QtWidgets.QGridLayout()

        #Adding Label and button for file selection
        self.label_selectfile = QtWidgets.QLabel("Select File")
        self.uGrid.addWidget(self.label_selectfile, 0, 0, 1, 1)

        self.btn_selectfile = QtWidgets.QPushButton("Click to select")
        self.uGrid.addWidget(self.btn_selectfile, 0, 1, 1, 1)

        #Adding label and combobox for building selection
        self.label_selectbuilding = QtWidgets.QLabel("Select Building")
        self.uGrid.addWidget(self.label_selectbuilding, 1, 0, 1, 1)

        self.dropdown_buildings = QtWidgets.QComboBox()
        self.uGrid.addWidget(self.dropdown_buildings, 1, 1, 1, 1)

        #Adding horizontal partition
        self.uGrid.addWidget(gf.divider(), 2, 0, 1, 2)

        #Adding Enrichment
        self.label_enrichment = QtWidgets.QLabel("Enrichment")
        self.uGrid.addWidget(self.label_enrichment, 3, 0, 1, 1)

        #Adding enrichment options
        self.checkbox_gml = QtWidgets.QCheckBox("Select GML File")
        self.uGrid.addWidget(self.checkbox_gml, 4, 0, 1, 1)

        self.checkbox_ade = QtWidgets.QCheckBox("Select CityGML + Energy ADE")
        self.uGrid.addWidget(self.checkbox_ade, 4, 1, 1, 1)

        #Adding horizontal partition
        self.uGrid.addWidget(gf.divider(), 5, 0, 1, 2)

        #Add select dwelling
        self.label_dwelling = QtWidgets.QLabel("Select Dwelling Archetype")
        self.uGrid.addWidget(self.label_dwelling, 6, 0, 1, 1)

        self.combobox_dwelling = QtWidgets.QComboBox()
        self.combobox_dwelling.addItems(["SFD", "MFD", "etc"])
        self.uGrid.addWidget(self.combobox_dwelling, 6, 1, 1, 1)

        #Adding horizontal partition
        self.uGrid.addWidget(gf.divider(), 7, 0, 1, 2)

        #Add select weather
        self.label_weather = QtWidgets.QLabel("Select weather file")
        self.uGrid.addWidget(self.label_weather, 8, 0, 1, 1)

        self.btn_weather = QtWidgets.QPushButton("Click to select")
        self.uGrid.addWidget(self.btn_weather, 8, 1, 1, 1)

        # Adding horizontal partition
        self.uGrid.addWidget(gf.divider(), 9, 0, 1, 2)

        #Add select weather
        self.label_custom = QtWidgets.QLabel("Custom Enrichment")
        self.uGrid.addWidget(self.label_custom, 10, 0, 1, 1)

        self.btn_custom = QtWidgets.QPushButton("Click for custom enrichment")
        self.uGrid.addWidget(self.btn_custom, 10, 1, 1, 1)

        # Adding horizontal partition
        self.uGrid.addWidget(gf.divider(), 11, 0, 1, 2)

        # Adding output options
        self.checkbox_withsimulation = QtWidgets.QCheckBox("With Simulation (only if Dymola installed locally)")
        self.uGrid.addWidget(self.checkbox_withsimulation, 12, 0, 1, 1)

        self.checkbox_modelica = QtWidgets.QCheckBox("Modelica Model")
        self.uGrid.addWidget(self.checkbox_modelica, 12, 1, 1, 1)

        self.checkbox_gml_ade_file = QtWidgets.QCheckBox("CityGML Energy ADE")
        self.uGrid.addWidget(self.checkbox_gml_ade_file, 13, 0, 1, 1)

        self.checkbox_csv = QtWidgets.QCheckBox("CSV Results (only if Dymola installed locally)")
        self.uGrid.addWidget(self.checkbox_ade, 13, 1, 1, 1)

        # Adding horizontal partition
        self.uGrid.addWidget(gf.divider(), 14, 0, 1, 2)

        self.btn_execute = QtWidgets.QPushButton("Click to execute")
        self.uGrid.addWidget(self.btn_execute, 15, 0, 1, 1)




        #Adding grid to main layout
        self.vbox.addLayout(self.uGrid)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    widget = mainWindow()
    widget.show()
    sys.exit(app.exec_())