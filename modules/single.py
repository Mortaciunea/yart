import pymel.core as pm

import bdRig.system.module as module
reload(module)

import bdRig.ui.moduleUI as moduleUI
reload(moduleUI)


moduleWin = 'moduleWindow'

class SingleModule(module.Module):
    def __init__(self,*args,**kargs):
        print 'Creating single module'
        super(SingleModule,self).__init__(*args,**kargs)
        self.nJnt = 1
        self.moduleType = 'single'

class SingleModule_UI(moduleUI.ModuleUI):
    def __init__(self):
        super(SingleModule_UI,self).__init__(title='Create Single Module')



def createUI():
    if pm.window( moduleWin, exists = True, q = True ):
        pm.deleteUI( moduleWin)

    ui = SingleModule_UI()
    