import pymel.core as pm

import guide 
reload(guide)
from guide import Guide 

import utils
reload(utils)

import json

class Module(object):
    def __init__(self,*args,**kargs):
        print 'Base Module class'
        self.moduleRebuildInfo = {}
        self.guidesList = []
        self.shader = None
        self.moduleGrp = None
        self.moduleCtrl = None
        self.moduleCtrlGrp = None
        self.moduleGuidesGrp = None
        self.moduleConnectionsGrp = None
        self.moduleType = ''
        
        self.name = kargs.setdefault('name','new')
        self.mirror = kargs.setdefault('mirror',0)
        self.parent = kargs.setdefault('parent',None)
        self.nJnt = kargs.setdefault('nJnt',1)
        self.nCtrl = kargs.setdefault('nCtrl',1)
        self.spaceSwitch = kargs.setdefault('spaceSwitch',0)
        self.jointOrient = kargs.setdefault('jointOrient','xyz')
        self.color = kargs.setdefault('color',[1,1,0])
        self.position = kargs.setdefault('position',[0,0,0])

    #  ---------------------------------------------------------------------CREATION-------------------------------------------------------------------------------#
    def createModule(self):
        self.createGroups()
        self.createModuleShader()
        self.createGuides()
        pm.select(cl=1)
        self.saveModuleInfo()
    
    def createGroups(self):
        pm.select(cl=1)
        self.moduleGrp = pm.group(name=self.name + '_module')
        self.moduleRebuildInfo['module_group'] = self.moduleGrp.name()
        pm.select(cl=1)
        self.moduleGuidesGrp = pm.group(name=self.name + '_guides_grp')
        self.moduleRebuildInfo['module_guides_group'] = self.moduleGuidesGrp.name()
        pm.parent(self.moduleGuidesGrp,self.moduleGrp )
        pm.select(cl=1)
        self.moduleConnectionsGrp= pm.group(name=self.name + '_connections_grp')
        self.moduleRebuildInfo['module_connections_group'] = self.moduleConnectionsGrp.name()
        pm.parent(self.moduleConnectionsGrp,self.moduleGrp )
        pm.select(cl=1)        
        
   
    def createModuleShader(self):
        shd = pm.ls(self.name + '_lmb_shd')
        if not shd:
            mat = pm.shadingNode('lambert',asShader = 1,n=self.name + '_lmb')
            mat.color.set(self.color)
            shader = pm.sets( renderable=True, noSurfaceShader=True, empty=True, name=mat.name() + '_shd' )
            mat.outColor >> shader.surfaceShader
            self.shader = shader
            self.moduleRebuildInfo['module_shader'] = self.shader.name()
        else:
            self.shader = shd[0]
            self.moduleRebuildInfo['module_shader'] = self.shader.name()

    def createGuides(self):
        prevGuide = None
        for i in range(self.nJnt):
            guide = Guide(shader = self.shader,name=self.name + '_guide_' + (str(i)).zfill(2),moduleParent = self.name)
            guide.drawGuide()
            pos = [0,0,i*10]
            if i == 0:
                self.moduleCtrl ,self.moduleCtrlGrp = utils.buildBoxController(guide.name,self.name + '_ctrl',2)
                pm.parent(self.moduleCtrlGrp,self.moduleGrp)
                pm.parent(self.moduleGuidesGrp,self.moduleCtrl)
            guide.setPos(pos)
            self.guidesList.append(guide.name)
            pm.parent(guide.guideGrp,self.moduleGuidesGrp)
            attrName = 'guide_' + (str(i)).zfill(2) 
            pm.addAttr(self.moduleCtrl,ln=attrName,at='message')
            guide.transform.message.connect( self.moduleCtrl.attr(attrName))
            
            if i > 0:
                connectionGrp = prevGuide.drawConnectionTo(guide)
                pm.parent(connectionGrp,self.moduleConnectionsGrp)
            
            prevGuide = guide
                
        self.moduleRebuildInfo['guidesList'] = self.guidesList
        self.moduleCtrlGrp.setTranslation(self.position,space='world')
        
        
    #  ---------------------------------------------------------------------ACTIONS--------------------------------------------------------------------------------#
    def reorientGuides(self):
        for i in range(len(self.guidesList)-1):
            guidePos = pm.xform(self.guidesList[i].name,q=1,rp=1,ws=1)
            self.guidesList[i].guideGrp.setPivots(guidePos,worldSpace=1)
            tempAim = pm.aimConstraint(self.guidesList[i+1].name,self.guidesList[i].guideGrp,offset = [0,0,0],aimVector = [1,0,0],upVector=[0,1,0],worldUpType='scene')
            pm.delete(tempAim)
        guidePos = pm.xform(self.guidesList[-1].name,q=1,rp=1,ws=1)
        self.guidesList[-1].guideGrp.setPivots(guidePos,worldSpace=1)

        tempAim = pm.aimConstraint(self.guidesList[-2].name,self.guidesList[-1].guideGrp,offset = [0,0,0],aimVector = [-1,0,0],upVector=[0,1,0],worldUpType='scene')
        pm.delete(tempAim)
        
    def renameModule(self,newname):
        allChildren = pm.listRelatives(self.moduleGrp,ad=1)
        print allChildren 
        
    #-------------------------------------------------------------------SAVE MODULE INFO ---------------------------------------------------------------------------#
    def saveModuleInfo(self):
        saveInfo = json.dumps(self.moduleRebuildInfo)
        utils.addStringAttr(self.moduleGrp,'moduleInfo',saveInfo)
    
    #-------------------------------------------------------------------RESTORE MODULE ---------------------------------------------------------------------------#
    def restoreModule(self):
        print self.name
        self.moduleGrp = pm.ls(self.name + '_module')[0]
        self.moduleRebuildInfo = json.loads(self.moduleGrp.attr('moduleInfo').get())
        self.guidesList = self.moduleRebuildInfo['guidesList']
        for guideName in self.guidesList:
            restoreGuide = guide.Guide(name=guideName)
            restoreGuide.restoreGuide() 
        
