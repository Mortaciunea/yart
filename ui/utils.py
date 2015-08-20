import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import pymel.core as pm

def uiCreateLabeledBox(labelText,settings=0):
    boxGroup = QtGui.QGroupBox()
    boxGroupLayout = QtGui.QVBoxLayout()
    boxGroupLayout.setSpacing(3)
    boxGroupLayout.setAlignment(QtCore.Qt.AlignTop)
    boxGroupLayout.setObjectName(labelText.replace(' ','') + '_main_layout')

    titleLayout = QtGui.QHBoxLayout()
    titleLayout.setContentsMargins(0,0,0,0)
    titleFrame = QtGui.QFrame()
    titleFrame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
    titleFrame.setStyleSheet("QFrame { background-color : green; color : white; }")
    label = QtGui.QLabel(labelText)
    label.setFixedHeight(20)
        
    titleLayout.addWidget(label)

    if settings:
        settingsBtn = QtGui.QPushButton('+')
        settingsBtn.setObjectName('settingsButton')
        settingsBtn.setFixedWidth(20)
        settingsBtn.setStyleSheet("QPushButton { background-color : green; color : white; border: none }")
        titleLayout.addWidget(settingsBtn)
    
    titleFrame.setLayout(titleLayout)
    
    boxGroupLayout.addWidget(titleFrame)
    boxGroup.setLayout(boxGroupLayout)
    
    return boxGroup

def uiGetMainLayout(widgetGroup,widgetLabel):
    layout =  widgetGroup.findChild(QtGui.QVBoxLayout,widgetLabel.replace(' ','') + '_main_layout')
    if layout:
        return layout
    return None


def uiGetButton(widgetGroup,buttonName):
    btn =  widgetGroup.findChild(QtGui.QPushButton,buttonName)
    if btn:
        return btn
    
    return None

def uiAddWidgetSizeAnim(widget,onoff,size,size_offset=0):
    size_anim = None
    try:
        print widget
        size_anim = QtCore.QPropertyAnimation(widget,'geometry')
    except:
        pm.warning('Failed to create QPropertyAnimation ')
    geometry = widget.geometry()        
    width = geometry.width()
    x,y,_,_ = geometry.getCoords()
    size_start = QtCore.QRect(x,y,width,int(not(onoff))*size + size_offset)
    size_end = QtCore.QRect(x,y,width,onoff *size +  size_offset)
    
    size_anim.setStartValue(size_start)
    size_anim.setEndValue(size_end)
    size_anim.setDuration(200)
    
    size_anim_curve = QtCore.QEasingCurve()
    if onoff:
        size_anim_curve.setType(QtCore.QEasingCurve.InQuad)
    else:
        size_anim_curve.setType(QtCore.QEasingCurve.OutQuad)

    size_anim.setEasingCurve(size_anim_curve)
    
    return size_anim