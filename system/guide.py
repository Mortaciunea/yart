import pymel.core as pm
import maya.OpenMaya as om
import json
import utils as utils
reload(utils)

class Guide:
    def __init__(self,*args,**kargs):
        self.name = kargs.setdefault('name','guide')
        self.parent = kargs.setdefault('parent',None)
        self.jointOrient = kargs.setdefault('jointOrient','xyz')
        self.shader = kargs.setdefault('shader',None)
        self.moduleParent = kargs.setdefault('moduleParent',None)
        
        self.guideInfo = {}
        self.position = []
        self.transform = None
        self.hasConnection = 0
        self.guideGrp = None
        
    
    def saveGuideInfo(self):
        self.guideInfo['name'] = self.name
        if self.parent:
            self.guideInfo['parent'] = self.parent.name()
        else:
            self.guideInfo['parent'] = ''
            
        self.guideInfo['jointOrient'] = self.jointOrient
        if self.shader:
            self.guideInfo['shader'] = self.shader.name()
        else:
            self.guideInfo['shader'] = ''
        self.guideInfo['position'] = self.position
        self.guideInfo['transform'] = self.transform.name()
        self.guideInfo['hasConnection'] = self.hasConnection
        self.guideInfo['guideGrp'] = self.guideGrp.name()
        
        saveInfo = json.dumps(self.guideInfo)
        utils.addStringAttr(self.guideGrp,'guideInfo',saveInfo)
        
    def restoreGuide(self):
        self.guideGrp = pm.ls(self.name + '_grp',type='transform')[0]
        self.guideInfo = self.guideGrp.attr('guideInfo').get()
        print self.guideInfo 


    def drawGuide(self):
        pm.select(cl=1)
        self.guideGrp = pm.group(n=self.name + '_grp')
        sphere = pm.sphere(name = self.name + '_center', ax =  [0, 1, 0] , r=0.8,ch=0)[0]
        if self.shader:
            pm.sets( self.shader, e=True, forceElement = sphere)
        axes = self.drawAxes()
        pm.parent(sphere.getShape(),axes,r=1,s=1)
        pm.delete(sphere)
        axes.rename(self.name)
        self.transform = axes
        
        pm.parent(self.transform,self.guideGrp)
        pm.select(cl=1)
        self.saveGuideInfo()

    def drawAxes(self):
        xShd,yShd,zShd = self.getAxesShd()
        
        xLine = pm.cylinder(ax =  [1, 0, 0], r=0.1,hr=12, p=[0.6,0,0], n = self.name + '_line_x')[0]
        pm.sets( xShd , e=True, forceElement = xLine)  
        xLine.setPivots([0,0,0])
        pm.makeIdentity(a=1,t=1)
        
        
        yLine = pm.cylinder(ax =  [0, 1, 0], r=0.1,hr=12, p=[0,0.6,0], n = self.name + '_line_y')[0]
        pm.sets( yShd , e=True, forceElement = yLine)
        yLine.setPivots([0,0,0])
        pm.makeIdentity(a=1,t=1)
        pm.parent(yLine.getShape(),xLine,r=1,s=1)
        pm.delete(yLine)
        
        zLine = pm.cylinder(ax =  [0, 0, 1], r=0.1,hr=12, p=[0,0,0.6], n = self.name + '_line_z')[0]
        pm.sets( zShd , e=True, forceElement = zLine)
        zLine.setPivots([0,0,0])
        pm.makeIdentity(a=1,t=1)
        pm.parent(zLine.getShape(),xLine,r=1,s=1)
        pm.delete(zLine)
        
        xCap = pm.cone(ax =  [1, 0, 0], r=0.2,hr=4, p=[1.5,0,0], n = self.name + '_cap_x')[0]
        pm.sets( xShd , e=True, forceElement = xCap)
        xCap.setPivots([0,0,0])
        pm.makeIdentity(a=1,t=1)
        pm.parent(xCap.getShape(),xLine,r=1,s=1)
        pm.delete(xCap)
        
        yCap = pm.cone(ax =  [0, 1, 0], r=0.2,hr=4, p=[0,1.5,0], n = self.name + '_cap_y')[0]
        pm.sets( yShd , e=True, forceElement = yCap)
        yCap.setPivots([0,0,0])
        pm.makeIdentity(a=1,t=1)
        pm.parent(yCap.getShape(),xLine,r=1,s=1)
        pm.delete(yCap)

        zCap = pm.cone(ax =  [0, 0, 1], r=0.2,hr=4, p=[0,0,1.5], n = self.name + '_cap_z')[0]
        pm.sets( zShd , e=True, forceElement = zCap)
        zCap.setPivots([0,0,0])
        pm.makeIdentity(a=1,t=1)
        pm.parent(zCap.getShape(),xLine,r=1,s=1)
        pm.delete(zCap)
        
        return xLine
        
    def getAxesShd(self):
        xShd = yShd = zShd = None
        
        shd = pm.ls('x_axis_lmb_shd')
        if not shd:
            mat = pm.shadingNode('lambert',asShader = 1,name = 'x_axis_lmb')
            mat.color.set([1,0,0])
            shader = pm.sets( renderable=True, noSurfaceShader=True, empty=True, name=mat.name() + '_shd' )
            mat.outColor >> shader.surfaceShader
            xShd = shader
        else:
            xShd = shd[0]
    
        shd = pm.ls('y_axis_lmb_shd')
        if not shd:
            mat = pm.shadingNode('lambert',asShader = 1,name = 'y_axis_lmb')
            mat.color.set([0,1,0])
            shader = pm.sets( renderable=True, noSurfaceShader=True, empty=True, name=mat.name() + '_shd' )
            mat.outColor >> shader.surfaceShader
            yShd = shader
        else:
            yShd = shd[0]

        shd = pm.ls('z_axis_lmb_shd')
        if not shd:
            mat = pm.shadingNode('lambert',asShader = 1,name = 'z_axis_lmb')
            mat.color.set([0,0,1])
            shader = pm.sets( renderable=True, noSurfaceShader=True, empty=True, name=mat.name() + '_shd' )
            mat.outColor >> shader.surfaceShader
            zShd = shader
        else:
            zShd = shd[0]
            
        return xShd,yShd,zShd

    def setPos(self,pos):
        pm.move(self.guideGrp,pos[0],pos[1],pos[2])
        pm.makeIdentity(self.guideGrp,apply=True, translate=True )
        self.position = pos
        
    def getPos(self):
        pos = pm.xform(self.guideGrp,q=1,a=1,ws=1,rp=1)
        return pos

    def setConnection(self,val):
        self.hasConnection = val
    
    @classmethod
    def getLength(cls,g1,g2):
        g1Pos = utils.toVector(g1.getPos())
        g2Pos = utils.toVector(g2.getPos())
        
        length = (g1Pos-g2Pos).length()
        return length
        
    def drawConnectionTo(self,toGuide):
        pm.select(cl=1)
        conMainGrp = pm.group(n=self.name + '_con_grp')
        
        g1Pos = self.getPos()
        g2Pos = toGuide.getPos()
        
        con = pm.polyCone( r = 0.35,h = 2, sx = 4, sy = 1, sz = 0, ax = [0, 0, 1], rcp = 0, cuv =  2, ch = 0,n=self.name + '_con')[0]
        con.setTranslation([g1Pos[0],g1Pos[1],g1Pos[2] + 2])
        con.overrideEnabled.set(1)
        con.overrideDisplayType.set(2)
        
        length = Guide.getLength(self,toGuide)
        
        pm.move(con.name() + '.vtx[5]',[0,0,length-4],r=1)
        pm.makeIdentity(a=1,t=1,s=1,r=1)
        
        
        pm.select(cl=1)
        startClsGrp = pm.group(name = con.name() + '_start_loc_grp')
        pm.select(con.name() + '.vtx[0:3]')
        startClsHandle = pm.cluster(name = con.name() + '_start_cls')[1]

        pm.select(cl=1)
        endClsGrp = pm.group(name = con.name() + '_end_loc_grp')
        pm.select(con.name() + '.vtx[5]')
        endClsHandle = pm.cluster(name = con.name() + '_end_cls')[1]
        pm.select(cl=1)
        
        vtx1Pos = pm.xform(con.name() + '.vtx[0]',q=1,t=1,a=1,ws=1)
        vtx2Pos = pm.xform(con.name() + '.vtx[5]',q=1,t=1,a=1,ws=1)
        
        startClsGrp.setPivots(g1Pos,ws = 1)
        endClsGrp.setPivots(g2Pos, ws = 1)
        
        pm.aimConstraint(self.name,endClsGrp,mo=1)
        pm.aimConstraint(toGuide.name,startClsGrp,mo=1)
        
        pm.pointConstraint(self.name,startClsGrp,mo=1)
        pm.pointConstraint(toGuide.name,endClsGrp,mo=1)
        
        pm.parent(startClsHandle,startClsGrp)
        pm.parent(endClsHandle,endClsGrp)
        pm.select(cl=1)
        pm.parent([con,startClsGrp,endClsGrp,],conMainGrp)
        pm.select(cl=1)
        
        startClsGrp.visibility.set(0)
        endClsGrp.visibility.set(0)
        #pm.parent(conMainGrp,g1.guideGrp)
        #pm.aimConstraint(toGuide.name,g1.guideGrp,mo=1)
        self.setConnection(1)
        
        pm.select(cl=1)
        return conMainGrp
    
    def setParent(self,parentsList):
        pass