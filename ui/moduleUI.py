#import shiboken
import sip
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import pymel.core as pm
import maya.OpenMayaUI 

import utils as utils
reload(utils)

import bdRig.system.module as module
reload(module)

import json

'''
def get_maya_window():
    maya_window_util = maya.OpenMayaUI.MQtUtil.mainWindow()
    maya_window = shiboken.wrapInstance( long( maya_window_util ), QtGui.QWidget )
    return maya_window
'''

def get_maya_window():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


moduleWin = 'moduleWindow'


class ModuleUI(QtGui.QMainWindow):

    def __init__(self,title='Create New Module',parent=get_maya_window()):

        super(ModuleUI,self).__init__(parent)

        self.modulesList = {}

        self.setObjectName(moduleWin)
        self.setWindowTitle(title)
        self.setWindowFlags(QtCore.Qt.Tool)
        
        centralWidget = QtGui.QWidget()
        mainLayout = QtGui.QVBoxLayout()
        
        #top layout will hold the character name
        toplayout = QtGui.QVBoxLayout()
        self.createTopUi(toplayout)
        
        mainLayout.addLayout(toplayout)


        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.show()
        self.resize(300,300)
        
        '''
        dockWidget = QtGui.QDockWidget("Dock Widget")
        dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        dockWidget.setWidget(centralWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)
        '''
    def createTopUi(self,parentLayout):
        self.attrGroup  = utils.uiCreateLabeledBox('Attributes')
        attrGroupLayout = utils.uiGetMainLayout(self.attrGroup, 'Attributes')

        templateNameLayout = QtGui.QHBoxLayout()
        templateNameLayout.setContentsMargins(10,5,10,0)
        templateNameLabel = QtGui.QLabel('Template Name: ')
        templateNameEdit = QtGui.QLineEdit()
        templateNameEdit.setObjectName('moduleNameEdit')
        templateNameLayout.addWidget(templateNameLabel)
        templateNameLayout.addWidget(templateNameEdit)
        
        jointNumberLayout = QtGui.QHBoxLayout()
        jointNumberLayout.setContentsMargins(10,0,10,0)
        jointNumberLabel = QtGui.QLabel('Joint Number: ')
        jointNumberSpin = QtGui.QSpinBox()
        jointNumberSpin.setMinimum(1)
        jointNumberSpin.setObjectName('numJntSpin')
        jointNumberLayout.addWidget(jointNumberLabel)
        jointNumberLayout.addWidget(jointNumberSpin)

    
        separator = QtGui.QFrame()
        separator.setFrameShape(QtGui.QFrame.HLine)
        separator.setFrameShadow(QtGui.QFrame.Sunken)
    
        createModuleBtn = QtGui.QPushButton('Create')
        
        attrGroupLayout.addLayout(templateNameLayout)
        attrGroupLayout.addLayout(jointNumberLayout)
        attrGroupLayout.addWidget(separator)
        attrGroupLayout.addWidget(createModuleBtn)
        
        self.attrGroup.setLayout(attrGroupLayout)
    
        parentLayout.addWidget(self.attrGroup)
        
        createModuleBtn.clicked.connect(self.createModule)
        
        
    def createModule(self):
        moduleNameEdit = self.attrGroup.findChild(QtGui.QLineEdit,'moduleNameEdit')
        moduleName = str(moduleNameEdit.text())
        moduleNumJntSpin = self.attrGroup.findChild(QtGui.QSpinBox,'numJntSpin')
        moduleNumJnt = moduleNumJntSpin.value()
        
        if moduleName:
            moduleExists = pm.ls(moduleName)
            if not moduleExists:
                newModule = module.Module(name=moduleName,nJnt = moduleNumJnt)
                newModule.createModule()
                self.modulesList[newModule.name] = {'Joint Number':moduleNumJnt,'Module Controller':newModule.moduleCtrl}
            else:
                pm.warning('Module "%s" exists already'%moduleName)
    

    def closeEvent(self, event):
        print 'closing'
        event.accept() # let the window close
        
def createUI():
    if pm.window( moduleWin, exists = True, q = True ):
        pm.deleteUI( moduleWin)

    ModuleUI()
    
    