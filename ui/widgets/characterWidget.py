
import pymel.core as pm
import pymel.core.datatypes as dt
import re,os,shutil,glob,sys,inspect

import logging

#import shiboken
import sip
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import maya.OpenMayaUI

from .. import utils as utils
reload(utils)

from ...system import characterX as character
reload(character)


class CharacterWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super(CharacterWidget,self).__init__(parent)
        self.currentCharacterName = ''
        self.charactersList = []
        self.charSettingsVisible = 0 
        self.charSettingsWidget = None
        self.characterGroup = None
        self.settings_size_anim = None  
        self.charGroup_size_anim = None
        self.currentCharacter = None
        self.create()
        self.updateChars()
        
    def create(self):
        characterWidgetLayout = QtGui.QHBoxLayout()
        characterWidgetLayout.setContentsMargins(0,0,0,0)
        self.characterGroup = utils.uiCreateLabeledBox('Character',settings=1)
        self.characterGroup.setFixedHeight(60)

        characterGroupLayout = utils.uiGetMainLayout(self.characterGroup,'Character')
        characterGroupLayout.setAlignment(QtCore.Qt.AlignTop)
        characterGroupLayout.setContentsMargins(0,0,0,0)
    
        nameLayout = QtGui.QHBoxLayout()
        nameLabel = QtGui.QLabel('Character name')
        nameLabel.setMaximumWidth(80)
        #self.charNameCombo = QtGui.QLineEdit()
        self.charNameCombo = QtGui.QComboBox()
        self.charNameCombo.setEditable(1)
        nameBtn = QtGui.QPushButton('Create character')
    
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.charNameCombo)
        nameLayout.addWidget(nameBtn)
    
        self.characterSettingWidget = QtGui.QWidget()
        self.characterSettingWidget.setContentsMargins(0,0,0,0)
        self.characterSettingWidget.setFixedHeight(0)
    
        characterGroupLayout.addWidget(self.characterSettingWidget)
        characterGroupLayout.addLayout(nameLayout)
        self.characterGroup.setLayout(characterGroupLayout)
        characterWidgetLayout.addWidget(self.characterGroup)
    
        settingsBtn = utils.uiGetButton(self.characterGroup, 'settingsButton')
        settingsBtn.clicked.connect(self.toggleCharSettingsUi)        
        
        self.setLayout(characterWidgetLayout)
        
        nameBtn.clicked.connect(self.createCharacter)
        
    def toggleCharSettingsUi(self):
        if not self.charSettingsVisible:
            self.charSettingsVisible = 1
            settingsBtn = utils.uiGetButton(self.characterGroup, 'settingsButton')
            settingsBtn.setText('-')
            self.addCharSettingsUi()
            ''' PySIde
            self.settings_size_anim= utils.uiAddWidgetSizeAnim(self.characterSettingWidget,1,20)
            self.settings_size_anim.valueChanged.connect(self.forceResize)
            self.settings_size_anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
            
            
            self.charGroup_size_anim= utils.uiAddWidgetSizeAnim(self.characterGroup,1,20,60)
            self.charGroup_size_anim.valueChanged.connect(self.charGroupForceResize)
            self.charGroup_size_anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
            '''
            #self.characterGroup.setFixedHeight(80)
        else:
            self.charSettingsVisible = 0
            settingsBtn = utils.uiGetButton(self.characterGroup, 'settingsButton')
            settingsBtn.setText('+')
            # ----------------- PyQt4
            self.characterSettingWidget.setFixedHeight(0)
            self.characterGroup.setFixedHeight(60)            
            ''' PySide
            self.settings_size_anim = utils.uiAddWidgetSizeAnim(self.characterSettingWidget,0,20)
            self.settings_size_anim.valueChanged.connect(self.forceResize)
            self.settings_size_anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
            
            self.charGroup_size_anim= utils.uiAddWidgetSizeAnim(self.characterGroup,0,20,60)
            self.charGroup_size_anim.valueChanged.connect(self.charGroupForceResize)
            self.charGroup_size_anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)            
            '''

    
    def addCharSettingsUi(self):
        charSettingsLayout = QtGui.QVBoxLayout()
        charSettingsLayout.setContentsMargins(0,0,0,0)
        charSidesStrings = QtGui.QLineEdit('Left,Right')
        charSettingsLayout.addWidget(charSidesStrings)
        self.characterSettingWidget.setLayout(charSettingsLayout)
        #PyQt4
        self.characterSettingWidget.setFixedHeight(30)
        self.characterGroup.setFixedHeight(80)


    def forceResize(self,new_height):
        self.characterSettingWidget.setFixedHeight(new_height.height())
        
    def charGroupForceResize(self,new_height):
        self.characterGroup.setFixedHeight(new_height.height())        
        
    def createCharacter(self):
        self.currentCharacterName =  self.charNameCombo.currentText()
        if self.currentCharacterName not in self.charactersList:
            self.charNameCombo.addItem(self.currentCharacterName)
            self.charactersList.append(self.currentCharacterName)
            self.currentCharacter = character.CharacterX(name=self.currentCharacterName)
            self.currentCharacter.createCharacterX()
        else:
            pm.warning('A character with %s name exists already'%self.currentCharacterName)
            
    
    def updateChars(self):
        characters = pm.ls('*CHAR')
        if characters:
            for char in characters:
                characterName = char.name().replace('_CHAR','')
                self.currentCharacter = character.CharacterX(name=characterName)
                self.currentCharacter.restoreCharacter()
                self.charNameCombo.addItem(characterName)