#Yet Another Rigging Tool or shortly yart 
import bdRig.system.guide as guide

import pymel.core as pm
import pymel.core.datatypes as dt
import re,os,shutil,glob,sys,inspect

import logging

#import shiboken
import sip
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import maya.OpenMayaUI
import utils as utils
reload(utils)

import widgets.characterWidget as characterWidget
reload(characterWidget)

'''
def get_maya_window():
    maya_window_util = maya.OpenMayaUI.MQtUtil.mainWindow()
    maya_window = shiboken.wrapInstance( long( maya_window_util ), QtGui.QWidget )
    return maya_window
'''

def get_maya_window():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


yartWin = 'yartWindow'

class YartUI(QtGui.QMainWindow):
    def __init__(self,parent=get_maya_window()):
        super(YartUI,self).__init__(parent)

        self.setObjectName(yartWin)
        self.setWindowTitle('Rigging Kit 0.1')
        
        centralWidget = QtGui.QWidget()
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        # --- char widget -----#
        charWidget = characterWidget.CharacterWidget()

        leftSideLayout = QtGui.QVBoxLayout()
        #middle right side layout will hold the functionality 
        rightSideLayout = QtGui.QVBoxLayout()

        #middle layout
        middleLayout = QtGui.QHBoxLayout()
        #middleLayout.setFrameStyle(QtGui.QFrame.StyledPanel)
        middleLayout.addLayout(leftSideLayout)
        middleLayout.addLayout(rightSideLayout)


        self.createLeftSideUi(leftSideLayout)
        self.createRightSideUi(rightSideLayout)


        mainLayout.addWidget(charWidget)
        mainLayout.addLayout(middleLayout)
        
        #mainLayout.addLayout(splitterLayout)

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        
        #menu bar
        #self.addMenu()

        self.show()
        self.resize(300,600)

    def addMenu(self):
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('File')
        self.fileMenu.addAction('Load skeleton')
        self.fileMenu.addAction('Save skeleton')
        self.toolsMenu = self.menuBar.addMenu('Tools')
        self.toolsMenu.addAction('Create Picking Geometry')
    
    def createLeftSideUi(self,parentLayout):
        label = QtGui.QLabel('Create modules')
        label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        label.setStyleSheet("QLabel { background-color : green; color : white; }")
        label.setFixedHeight(20)
        labelLayout = QtGui.QVBoxLayout()
        labelLayout.addWidget(label)
    
        modulesGroup = QtGui.QGroupBox()
        modulesGroupLayout = QtGui.QVBoxLayout()
        modulesGroupLayout.setAlignment(QtCore.Qt.AlignTop)
        modulesGroupLayout.setContentsMargins(0,0,0,0)
        
        separator = QtGui.QFrame()
        separator.setFrameShape(QtGui.QFrame.HLine)
        separator.setFrameShadow(QtGui.QFrame.Sunken)
        

        
        modulesGroupLayout.addLayout(labelLayout)
        self.addmodulesBtns(modulesGroupLayout)
        modulesGroupLayout.addWidget(separator)

        
        modulesGroup.setLayout(modulesGroupLayout)
    
        parentLayout.addWidget(modulesGroup)
        
    def addmodulesBtns(self,modulesGroupLayout):
        uiScriptFile = os.path.realpath(__file__)
        uiScriptPath,_ = os.path.split(uiScriptFile)
        modulesPath = uiScriptPath.replace('ui','modules')
        
        moduleFiles = [ py for py in os.listdir(modulesPath) if py.endswith('.py') and '__init__' not in py]
        
        if moduleFiles:
            modulesLayout = QtGui.QVBoxLayout()
            modulesLayout.setContentsMargins(10,0,10,0)
            btnGridLayout = QtGui.QGridLayout()
            modulesLayout.addLayout(btnGridLayout)
            modulesGroupLayout.addLayout(modulesLayout)

            numBtn = len(moduleFiles)
            #build a button grid with 3 columns
            for i in range(numBtn):
                name = moduleFiles[i][:-3]
                btn = QtGui.QPushButton(name)
                row = i / 3
                col = i % 3
                btnGridLayout.addWidget(btn,row,col)
                btn.clicked.connect(self.createModule)


    def createRightSideUi(self,parentLayout):
        label = QtGui.QLabel('modules List ')
        label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        label.setStyleSheet("QLabel { background-color : green; color : white; }")  
        label.setFixedHeight(20)
        labelLayout = QtGui.QVBoxLayout()
        labelLayout.addWidget(label)
    
        modulesGroup = QtGui.QGroupBox()
        self.modulesGroupLayout = QtGui.QVBoxLayout()
        self.modulesGroupLayout.setAlignment(QtCore.Qt.AlignTop)
        self.modulesGroupLayout.setContentsMargins(0,0,0,0)
        self.modulesGroupLayout.addLayout(labelLayout)
        
        modulesGroup.setLayout(self.modulesGroupLayout)
    
        parentLayout.addWidget(modulesGroup)

    def createModule(self):
        moduleName = str(self.sender().text())
        toImport =  'bdRig.modules.' + moduleName

        try:
            mod = __import__(toImport, {}, {},[moduleName])
            reload(mod)
            for name,obj in inspect.getmembers(mod):
                if inspect.isclass(obj):
                    baseclass =  obj.__bases__[0].__name__
                    if 'UI' in baseclass:
                        print baseclass
                        mod.createUI()
        except:
            pm.error("Did not find any modules")        
        
    def createNewGuide(self):
        print 'Creating New Guide Template'
        import bdRig.ui.templateUI as templateUI
        reload(templateUI)
        templateUI.create() 



      
        
def createUI():
    if pm.window( yartWin, exists = True, q = True ):
        pm.deleteUI( yartWin)

    YartUI()