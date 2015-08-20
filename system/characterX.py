import pymel.core as pm
import json,inspect

from ..modules import single as single
reload(single)

import utils as utils
reload(utils)

import module as module
reload(module)

import guide as guide
reload(guide)


class CharacterX(object):
    def __init__(self,name):
        self.name = str(name)
        self.characterCtrl = ''
        self.modulesList = []
        self.characterInfo = {}
        self.characterRootGrp = None
        self.characterModulesGrp = None
        self.bpModelGrp = None
        self.bdSkeletonGrp = None
        
        self.characterInfo['Name'] = self.name
        
    
    def createCharacterX(self):
        self.createGroups()
        self.createRootModule()
        strInfo = json.dumps(self.characterInfo)
        utils.addStringAttr(self.characterRootGrp,'characterInfo',strInfo)
        
        
    def createGroups(self):
        pm.select(cl=1)
        self.characterRootGrp = pm.group(name=self.name + '_CHAR')
        self.characterInfo['characterRootGrp'] = self.characterRootGrp.name()
        pm.select(cl=1)
        self.characterModulesGrp = pm.group(name=self.name + '_modules_grp')
        self.characterInfo['characterModulesGrp'] = self.characterModulesGrp.name()
        pm.select(cl=1)
        pm.parent(self.characterModulesGrp,self.characterRootGrp)
        
        
    
    def createRootModule(self):
        rootModule = single.SingleModule(name=self.name)
        rootModule.createModule()
        self.modulesList.append({'name':rootModule.name,'type':rootModule.moduleType})
        self.characterCtrl,_ = utils.buildCircleController(rootModule.moduleCtrlGrp.name(),self.name + '_character_ctrl',10)
        pm.parent(self.characterModulesGrp,self.characterCtrl)
        self.characterInfo['characterCtrl'] = self.characterCtrl.name()
        self.characterInfo['modulesList'] = self.modulesList
    
    def restoreCharacter(self):
        self.characterRootGrp = pm.ls(self.name + '_CHAR',type='transform')[0]
        self.characterInfo = json.loads(self.characterRootGrp.attr('characterInfo').get())
        self.characterModulesGrp = pm.ls(self.characterInfo['characterModulesGrp'],type='transform')[0]
        self.characterCtrl = pm.ls(self.characterInfo['characterCtrl'],type='transform')[0]
        self.modulesList =  self.characterInfo['modulesList']
        self.restoreModulesList()
        
    def restoreModulesList(self):
        for mod in self.modulesList:
            moduleName = mod['name']
            print moduleName
            moduleType = mod['type']
            moduleClass = self.restoreModuleClass(moduleType )
            newModule  = moduleClass(name=moduleName)
            newModule.restoreModule()
            #restoredModule = module.Module(name=modName)
            #restoredModule.restoreModule()
            
    def restoreModuleClass(self,moduleType):
        moduleName = moduleType
        toImport =  'bdRig.modules.' + moduleName

        try:
            mod = __import__(toImport, {}, {},[moduleName])
            reload(mod)
            for name,obj in inspect.getmembers(mod):
                if inspect.isclass(obj):
                    if 'UI' not in obj.__name__:
                        return obj
        except:
            pm.error("Did not find any modules")
        
    def listCharacterInfo(self):
        pass