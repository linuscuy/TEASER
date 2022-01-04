# -*- coding: utf-8 -*-
"""
TEASER+
Contact:
M.Sc. Avichal Malhotra: malhotra@e3d.rwth-aachen.de
B.Sc. Maxim Shamovich: maxim.shamovich@rwth-aachen.de

www.e3d.rwth-aachen.de
Mathieustr. 30
52074 Aachen

Some GUI functions taken from CityLDT.
Please contact Avichal Malhotra or Simon Raming for any questions.
Original Repo for CityLDT: https://gitlab.e3d.rwth-aachen.de/e3d-software-tools/cityldt/cityldt.git
"""

# import of libraries
import os
import sys
import PySide2
from PySide2 import QtWidgets, QtGui
import gui_functions as gf
import tplusselection as sel


# setting environment variable for PySide2
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


# positions and dimensions of window
posx = 275
posy = 100
width = 650
height = 700
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

        # Setting main layout
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.vbox)

        # Loading banner
        gf.load_banner(self, os.path.join(pypath, r'pictures\TEASER+_header.png'), sizefactor)

        #Setting Layout
        self.uGrid = QtWidgets.QGridLayout()

        self.btn_selFile = QtWidgets.QPushButton('Select file')
        self.uGrid.addWidget(self.btn_selFile, 0, 0, 1, 1)

        self.btn_selDir = QtWidgets.QPushButton('Select folder')
        self.uGrid.addWidget(self.btn_selDir, 0, 1, 1, 1)

        self.txtB_inPath = QtWidgets.QLineEdit()
        self.txtB_inPath.setPlaceholderText('Path to file or folder')
        self.txtB_inPath.setReadOnly(True)
        self.uGrid.addWidget(self.txtB_inPath, 0, 2, 1, 4)

        self.lbl_scanLoD = QtWidgets.QLabel('LoD scan progress:')
        self.uGrid.addWidget(self.lbl_scanLoD, 1, 0, 1, 1)

        self.pB_scanLoD = QtWidgets.QProgressBar(self)
        self.uGrid.addWidget(self.pB_scanLoD, 1, 1, 1, 5)

        self.vbox.addLayout(self.uGrid)

        # for selecting all or individual buildings
        self.gB_buildings = QtWidgets.QGroupBox('')
        self.vbox.addWidget(self.gB_buildings)
        # self.gB_buildings.setToolTip('When unchecked transformation will be done for all buildings in the file(s)')

        self.bGrid = QtWidgets.QGridLayout()
        self.gB_buildings.setLayout(self.bGrid)

        self.rb_allBuildings = QtWidgets.QRadioButton('Transform all buildings')
        self.bGrid.addWidget(self.rb_allBuildings, 0, 0, 1, 1)
        self.rb_allBuildings.setChecked(True)

        self.rb_selectBuildings = QtWidgets.QRadioButton('Select individual buildings')
        self.bGrid.addWidget(self.rb_selectBuildings, 0, 3, 1, 1)


        self.tbl_buildings = QtWidgets.QTableWidget()
        self.tbl_buildings.setColumnCount(4)
        self.tbl_buildings.setHorizontalHeaderLabels(['File Name', 'Name of Building', 'Level of Detail (LoD)', ''])
        self.tbl_buildings.verticalHeader().hide()
        # self.tbl_buildings.horizontalHeader().hide()
        self.tbl_buildings.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbl_buildings.setEnabled(False)
        self.tbl_buildings.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tbl_buildings.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tbl_buildings.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.bGrid.addWidget(self.tbl_buildings, 1, 0, 1, 6)

        # Gridbox for lower grid
        self.lGrid = QtWidgets.QGridLayout()
        self.btn_next = QtWidgets.QPushButton('TEASER Enrichment')
        self.lGrid.addWidget(self.btn_next, 0, 0, 1, 1)
        self.btn_next.setEnabled(False)

        self.btn_teasereco = QtWidgets.QPushButton('TEASEREco')
        self.lGrid.addWidget(self.btn_teasereco, 0, 2, 1, 1)
        self.btn_teasereco.setEnabled(False)

        self.btn_about = QtWidgets.QPushButton('About')
        self.lGrid.addWidget(self.btn_about, 1, 0, 1, 1)

        self.btn_reset = QtWidgets.QPushButton('Reset')
        self.lGrid.addWidget(self.btn_reset, 1, 1, 1, 1)

        self.btn_exit = QtWidgets.QPushButton('Exit')
        self.lGrid.addWidget(self.btn_exit, 1, 2, 1, 1)

        # self.btn_next = QtWidgets.QPushButton('Next')
        # self.lGrid.addWidget(self.btn_next, 0, 3, 1, 1)
        # self.btn_next.setEnabled(False)

        self.vbox.addLayout(self.lGrid)
        self.btn_selFile.clicked.connect(self.func_selectFile)
        self.btn_selDir.clicked.connect(self.func_selectDir)
        self.rb_selectBuildings.toggled.connect(self.func_selB)
        self.btn_about.clicked.connect(self.func_about)
        self.btn_reset.clicked.connect(self.func_reset)
        self.btn_exit.clicked.connect(self.func_exit)
        self.btn_next.clicked.connect(self.func_next)
        self.btn_teasereco.clicked.connect(self.func_eco)
        # self.cB_curBuilding.currentTextChanged.connect(self.func_curBuildingChanged)

        # self.gB_buildings.toggled.connect(self.func_buildingSelection)



        # setting some defaults
        self.inpPath = ''
        self.inpDir = ''
        self.expPath = ''
        self.completedLoD = 0
        # table row index to comboBox index
        self.tableDict = {}

    def func_selectFile(self):
        res = sel.select_gml(self)
        if res:
            self.inpPath = res
            self.inpDir = os.path.dirname(res)
            sel.get_files(self)
        else:
            pass

    def func_selectDir(self):
        res = sel.select_folder(self)
        if res:
            self.inpPath = res
            self.inpDir = res
            sel.get_files(self)
        else:
            pass

    def func_selB(self):
        if self.rb_selectBuildings.isChecked():
            self.tbl_buildings.setEnabled(True)
        else:
            self.tbl_buildings.setEnabled(False)

    def func_about(self):
        global posx, posy
        posx, posy = gf.dimensions(self)
        gf.next_window(self, about(), False)

    def func_reset(self):
        global posx, posy
        self.reset_variables()
        posx, posy = gf.dimensions(self)
        gf.next_window(self, mainWindow())

    def reset_variables(self):
        self.inpPath = ''
        self.inpDir = ''
        self.completedLoD = 0

    def func_exit(self):
        gf.close_application(self)

    def func_next(self):
        global buildingDict, selAll, inpDir
        inpDir = self.inpDir
        selAll = self.rb_allBuildings.isChecked()
        buildingDict = self.buildingDict
        gf.next_window(self, enrichment())


    def func_eco(self):
        self.btn_teasereco.setEnabled(True)

    def onStateChanged(self):
        """gets called when a checkbox for a building is (un)checked to update the buildingDict"""
        ch = self.sender()
        ix = self.tbl_buildings.indexAt(ch.pos())
        self.buildingDict[ix.row()]["selected"] = ch.isChecked()
        curText = self.tbl_buildings.item(ix.row(), 1).text().split('/')[0]
        for i in range(self.tbl_buildings.rowCount()):
            if i != ix.row():
                if self.tbl_buildings.item(i, 1).text().split('/')[0] == curText:
                    self.cBoxes[i].setChecked(ch.isChecked())
                    self.buildingDict[i]["selected"] = ch.isChecked()
                    self.checkBoxChange(i, ch.isChecked())
        self.checkBoxChange(ix.row(), ch.isChecked())

    def checkBoxChange(self, row, state):
        """changes Table"""
        if state:
            colorCode = (251, 255, 0)

            # setting dummyValue to get right index of sorted list
            self.tableDict[row] = "dummyValue"
            # getting and sorting all indexes of selected buildings
            sortedList = sorted(list(self.tableDict.keys()))
            # getting the correceted Index location of the new building
            correctedIndex = sortedList.index(row) + 1
            # replacing the dummyValue
            self.tableDict[row] = correctedIndex
            # add item to comboBox
            # self.cB_curBuilding.insertItem(correctedIndex, self.buildingDict[row]["filename"] + "/" + self.buildingDict[row]["buildingname"])
            # self.btn_saveBuildingParamsAndNext.setEnabled(True)

            for y in self.tableDict:
                if y > row:
                    self.tableDict[y] = self.tableDict[y] + 1

        else:
            colorCode = (255, 255, 255)
            num = row

            # remove save building Parameters
            if row in self.buildingParamsDict:
                del self.buildingParamsDict[row]

            for y in self.tableDict:
                if y > num:
                    self.tableDict[y] = self.tableDict[y] - 1

            # remove item from comboBox
            self.cB_curBuilding.removeItem(self.tableDict[row])
            del self.tableDict[row]

            # if self.cB_curBuilding.count() == 1 or self.cB_curBuilding.currentIndex() == self.cB_curBuilding.count() - 1:
            #     self.btn_saveBuildingParamsAndNext.setEnabled(False)

        gf.setTableRowColor(self, colorCode, row)

class enrichment(QtWidgets.QWidget):
    """window for transformation options"""

    def __init__(self):
        super(enrichment, self).__init__()
        self.initUI()

    def initUI(self):
        global posx, posy, width, height, sizefactor, sizer
        if sizer:
            posx, posy, width, height, sizefactor = gf.screenSizer(self, posx, posy, width, height, app)
            sizer = False
        gf.windowSetup(self, posx, posy, width, height, pypath,
                       'CityLDT - CityGML LoD Transformation Tool - Transformation')

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.vbox)

        gf.load_banner(self, os.path.join(pypath, r'pictures\TEASER+_header.png'), sizefactor)

        self.uGrid = QtWidgets.QGridLayout()

        self.vbox.addLayout(self.uGrid)
        ttl = 'Number of selected buildings - ' + str(len(buildingDict))
        # building parameters
        self.gB_buildingParameters = QtWidgets.QGroupBox(ttl)
        self.vbox.addWidget(self.gB_buildingParameters)
        self.vBox_forBPgB = QtWidgets.QVBoxLayout()
        self.gB_buildingParameters.setLayout(self.vBox_forBPgB)

        # building selection
        self.pGrid = QtWidgets.QGridLayout()

        self.lbl_curBuilding = QtWidgets.QLabel('Current building:')
        self.pGrid.addWidget(self.lbl_curBuilding, 0, 0, 1, 1)

        self.cB_curBuilding = QtWidgets.QComboBox()
        self.cB_curBuilding.addItems(['all (selected) buildings'])
        self.pGrid.addWidget(self.cB_curBuilding, 0, 1, 1, 2)

        presenetLoDs = []
        # adding selected buildings to the comboBox
        for key in buildingDict:
            if selAll:
                self.cB_curBuilding.insertItem(self.cB_curBuilding.count(),
                                               buildingDict[key]["filename"] + "/" + buildingDict[key]["buildingname"])
                if buildingDict[key]["values"]["LoD"] not in presenetLoDs:
                    presenetLoDs.append(buildingDict[key]["values"]["LoD"])
            elif buildingDict[key]["selected"]:
                self.cB_curBuilding.insertItem(self.cB_curBuilding.count(),
                                               buildingDict[key]["filename"] + "/" + buildingDict[key]["buildingname"])
                if buildingDict[key]["values"]["LoD"] not in presenetLoDs:
                    presenetLoDs.append(buildingDict[key]["values"]["LoD"])
            else:
                pass
        self.buildingDict = buildingDict

        # update title of groubbox according to number of buildings
        ttl = 'Number of selected buildings - ' + str(self.cB_curBuilding.count() - 1)
        self.gB_buildingParameters.setTitle(ttl)

        self.vBox_forBPgB.addLayout(self.pGrid)

        # Enrichmet properties
        self.dB_enrichment = QtWidgets.QGroupBox('Building Enrichment')
        self.vBox_forBPgB.addWidget(self.dB_enrichment)

        self.dGrid = QtWidgets.QGridLayout()
        self.dB_enrichment.setLayout(self.dGrid)

        self.lbl_year_of_construction = QtWidgets.QLabel('Year of Construction')
        self.dGrid.addWidget(self.lbl_year_of_construction, 0, 0, 1, 1)

        self.txtb_year_of_construction = QtWidgets.QLineEdit()
        # self.txtb_year_of_construction.setFixedWidth(250)
        self.txtb_year_of_construction.setPlaceholderText('Select individual building to overwrite')
        self.txtb_year_of_construction.setReadOnly(True)
        self.dGrid.addWidget(self.txtb_year_of_construction, 0, 1, 1, 1)

        self.lbl_dwelling_archetype = QtWidgets.QLabel('Select Archetype')
        self.dGrid.addWidget(self.lbl_dwelling_archetype, 0, 2, 1, 1)

        self.combobox_dwelling = QtWidgets.QComboBox()
        self.combobox_dwelling.addItems([" ", "IWU Single Family Dwelling", "TABULA Single Family House", "TABULA Multi Family House", "TABULA Terraced House", "TABULA Apartment Block"])
        self.dGrid.addWidget(self.combobox_dwelling, 0, 3, 1, 1)

        self.lbl_weather = QtWidgets.QPushButton('Select Weather file')
        self.dGrid.addWidget(self.lbl_weather, 1, 0, 1, 1)

        self.txt_weather = QtWidgets.QLineEdit('')
        self.dGrid.addWidget(self.txt_weather, 1, 1, 1, 3)

        self.lbl_enrichment = QtWidgets.QLabel('Enrich models using pre-defined archetypes')
        self.dGrid.addWidget(self.lbl_enrichment, 2, 0, 1, 2)

        self.btn_enrich = QtWidgets.QPushButton('Click to custom enrich')
        self.dGrid.addWidget(self.btn_enrich, 2, 2, 1, 2)

        self.grp_out = QtWidgets.QGroupBox('Output Options')
        self.vBox_forBPgB.addWidget(self.grp_out)

        self.mGrid = QtWidgets.QGridLayout()
        self.grp_out.setLayout(self.mGrid)

        # Adding output options
        self.checkbox_modelica = QtWidgets.QCheckBox("Modelica Model")
        self.mGrid.addWidget(self.checkbox_modelica, 0, 0, 1, 1)

        self.checkbox_withsimulation = QtWidgets.QCheckBox("With Simulation (if Dymola installed locally)")
        self.mGrid.addWidget(self.checkbox_withsimulation, 0, 1, 1, 1)

        self.checkbox_gml_ade_file = QtWidgets.QCheckBox("CityGML Energy ADE")
        self.mGrid.addWidget(self.checkbox_gml_ade_file, 0, 2, 1, 1)

        self.lbl_dymola = QtWidgets.QPushButton('Select Dymola path')
        self.mGrid.addWidget(self.lbl_dymola, 1, 0, 1, 1)
        self.lbl_dymola.setEnabled(False)

        self.txt_dymola = QtWidgets.QLineEdit('')
        self.mGrid.addWidget(self.txt_dymola, 1, 1, 1, 2)
        self.txt_dymola.setEnabled(False)

        self.grp_save = QtWidgets.QGroupBox('Save As')
        self.vBox_forBPgB.addWidget(self.grp_save)

        self.m1Grid = QtWidgets.QGridLayout()
        self.grp_save.setLayout(self.m1Grid)

        # Adding save as options
        self.checkbox_excel = QtWidgets.QCheckBox(".anything else")
        self.m1Grid.addWidget(self.checkbox_excel, 0, 0, 1, 1)

        self.checkbox_CSV = QtWidgets.QCheckBox(".csv")
        self.m1Grid.addWidget(self.checkbox_CSV, 0, 1, 1, 1)

        self.checkbox_excel = QtWidgets.QCheckBox(".xsls")
        self.m1Grid.addWidget(self.checkbox_excel, 0, 2, 1, 1)


        self.lbl_outputpath = QtWidgets.QPushButton('Select Output path')
        self.m1Grid.addWidget(self.lbl_outputpath, 1, 0, 1, 1)
        self.lbl_outputpath.setEnabled(False)

        self.txt_outputpath = QtWidgets.QLineEdit('')
        self.m1Grid.addWidget(self.txt_outputpath, 1, 1, 1, 2)
        self.txt_outputpath.setEnabled(False)

        # Gridbox for lower grid
        self.lGrid = QtWidgets.QGridLayout()

        self.btn_back = QtWidgets.QPushButton('Main Window')
        self.lGrid.addWidget(self.btn_back, 0, 0, 1, 1)

        self.btn_teasereco = QtWidgets.QPushButton('TEASEREco')
        self.lGrid.addWidget(self.btn_teasereco, 0, 1, 1, 1)

        self.btn_next = QtWidgets.QPushButton('Execute')
        self.lGrid.addWidget(self.btn_next, 0, 2, 1, 1)

        self.btn_about = QtWidgets.QPushButton('About')
        self.lGrid.addWidget(self.btn_about, 1, 0, 1, 1)

        self.btn_reset = QtWidgets.QPushButton('Reset')
        self.lGrid.addWidget(self.btn_reset, 1, 1, 1, 1)

        self.btn_exit = QtWidgets.QPushButton('Exit')
        self.lGrid.addWidget(self.btn_exit, 1, 2, 1, 1)

        self.vbox.addLayout(self.lGrid)



        # #Adding Label and button for file selection
        # self.label_selectfile = QtWidgets.QLabel("Select File")
        # self.uGrid.addWidget(self.label_selectfile, 0, 0, 1, 1)
        #
        # self.btn_selectfile = QtWidgets.QPushButton("Click to select")
        # self.uGrid.addWidget(self.btn_selectfile, 0, 1, 1, 1)
        #
        # #Adding label and combobox for building selection
        # self.label_selectbuilding = QtWidgets.QLabel("Select Building")
        # self.uGrid.addWidget(self.label_selectbuilding, 1, 0, 1, 1)
        #
        # self.dropdown_buildings = QtWidgets.QComboBox()
        # self.uGrid.addWidget(self.dropdown_buildings, 1, 1, 1, 1)
        #
        # #Adding horizontal partition
        # self.uGrid.addWidget(gf.divider(), 2, 0, 1, 2)

        # #Adding Enrichment
        # self.label_enrichment = QtWidgets.QLabel("Enrichment")
        # self.uGrid.addWidget(self.label_enrichment, 3, 0, 1, 1)
        #
        # #Adding enrichment options
        # self.checkbox_gml = QtWidgets.QCheckBox("Select GML File")
        # self.uGrid.addWidget(self.checkbox_gml, 4, 0, 1, 1)
        #
        # self.checkbox_ade = QtWidgets.QCheckBox("Select CityGML + Energy ADE")
        # self.uGrid.addWidget(self.checkbox_ade, 4, 1, 1, 1)
        #
        # #Adding horizontal partition
        # self.uGrid.addWidget(gf.divider(), 5, 0, 1, 2)
        #
        # #Add select dwelling
        # self.label_dwelling = QtWidgets.QLabel("Select Dwelling Archetype")
        # self.uGrid.addWidget(self.label_dwelling, 6, 0, 1, 1)
        #
        # self.combobox_dwelling = QtWidgets.QComboBox()
        # self.combobox_dwelling.addItems(["SFD", "MFD", "etc"])
        # self.uGrid.addWidget(self.combobox_dwelling, 6, 1, 1, 1)
        #
        # #Adding horizontal partition
        # self.uGrid.addWidget(gf.divider(), 7, 0, 1, 2)
        #
        # #Add select weather
        # self.label_weather = QtWidgets.QLabel("Select weather file")
        # self.uGrid.addWidget(self.label_weather, 8, 0, 1, 1)
        #
        # self.btn_weather = QtWidgets.QPushButton("Click to select")
        # self.uGrid.addWidget(self.btn_weather, 8, 1, 1, 1)
        #
        # # Adding horizontal partition
        # self.uGrid.addWidget(gf.divider(), 9, 0, 1, 2)
        #
        # #Add select weather
        # self.label_custom = QtWidgets.QLabel("Custom Enrichment")
        # self.uGrid.addWidget(self.label_custom, 10, 0, 1, 1)
        #
        # self.btn_custom = QtWidgets.QPushButton("Click for custom enrichment")
        # self.uGrid.addWidget(self.btn_custom, 10, 1, 1, 1)
        #
        # # Adding horizontal partition
        # self.uGrid.addWidget(gf.divider(), 11, 0, 1, 2)
        #
        # # Adding output options
        # self.checkbox_withsimulation = QtWidgets.QCheckBox("With Simulation (only if Dymola installed locally)")
        # self.uGrid.addWidget(self.checkbox_withsimulation, 12, 0, 1, 1)
        #
        # self.checkbox_modelica = QtWidgets.QCheckBox("Modelica Model")
        # self.uGrid.addWidget(self.checkbox_modelica, 12, 1, 1, 1)
        #
        # self.checkbox_gml_ade_file = QtWidgets.QCheckBox("CityGML Energy ADE")
        # self.uGrid.addWidget(self.checkbox_gml_ade_file, 13, 0, 1, 1)
        #
        # self.checkbox_csv = QtWidgets.QCheckBox("CSV Results (only if Dymola installed locally)")
        # self.uGrid.addWidget(self.checkbox_ade, 13, 1, 1, 1)
        #
        # # Adding horizontal partition
        # self.uGrid.addWidget(gf.divider(), 14, 0, 1, 2)
        #
        # self.btn_execute = QtWidgets.QPushButton("Click to execute")
        # self.uGrid.addWidget(self.btn_execute, 15, 0, 1, 1)




        #Adding grid to main layout
        self.vbox.addLayout(self.uGrid)


class about(QtWidgets.QWidget):
    def __init__(self):
        super(about, self).__init__()
        self.initUI()

    def initUI(self):
        global posx, posy, width, height, sizefactor

        gf.windowSetup(self, posx + 10, posy + 10, width, height, pypath, 'CityBIT - About')

        # creating main layout
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.vbox)

        gf.load_banner(self, os.path.join(pypath, r'pictures\e3dHeader.png'), sizefactor)

        self.textwidget = QtWidgets.QTextBrowser()
        self.vbox.addWidget(self.textwidget)
        self.textwidget.setFontPointSize(14)
        with open(os.path.join(pypath, 'about/about.txt'), 'r') as file:
            text = file.read()
        self.textwidget.setText(text)

        self.lGrid = QtWidgets.QGridLayout()

        self.btn_repo = QtWidgets.QPushButton('Open repository')
        self.lGrid.addWidget(self.btn_repo, 0, 0, 1, 1)

        self.btn_close = QtWidgets.QPushButton('Close')
        self.lGrid.addWidget(self.btn_close, 0, 1, 1, 1)

        self.vbox.addLayout(self.lGrid)

        self.btn_repo.clicked.connect(self.open_repo)
        self.btn_close.clicked.connect(self.close_about)

    def open_repo(self):
        os.startfile('www.e3d.rwth-aachen.de')

    def close_about(self):
        self.hide()


if __name__ == "__main__":
    
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    
    app.setStyle('Fusion')
    widget = mainWindow()
    widget.show()
    sys.exit(app.exec_())