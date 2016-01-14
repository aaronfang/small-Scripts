import pymel.core as pm
import math

class lineUpUVs(object):
	def __init__(self):
		self.Sels=[]
		self.W=[]
		self.H=[]
		pass
	
	def _UI(self):
		if pm.window("lineUpWin",exists=1):
			pm.deleteUI("lineUpWin",window=1)
		w=180
		self.window=pm.window("lineUpWin",t="AlignUVs",s=0,mb=1,rtf=1,wh=(w,25))

		pm.columnLayout("mainColumn",p="lineUpWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		pm.rowLayout(p="mainColumn",w=w,h=25,numberOfColumns=4,columnWidth4=(30,30,30,40),adjustableColumn=1, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
		self.floatField=pm.floatField("gapValueField",v=0.003)
		self.button=pm.button(l="U",c=self.lineUpU)
		self.button=pm.button(l="V",c=self.lineUpV)
		self.button=pm.button(l="UDIM",c=self.layoutUVsToUDIM)
		
		pm.separator(p="mainColumn",style='in')
		pm.rowLayout(p="mainColumn",w=w,h=25,numberOfColumns=4,columnWidth4=(30,30,30,40),adjustableColumn=1, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
		self.button=pm.button(l="Scale2Src",c=self.RK_ScaleToSrc)
		self.button=pm.button(l="G",c=self.RK_Geometric)
		self.button=pm.button(l="O",c=self.RK_Organic)
		self.button=pm.button(l="S",c=self.RK_Straighten)
		
		pm.separator(p="mainColumn",style='in')
		pm.button(p="mainColumn",l="Store / Select",c=self.selMesh)
		
		pm.showWindow(self.window)
		
	def layoutUVsToUDIM(self,*args):
		sels = pm.ls(sl=1)
		for i, x in enumerate(sels):
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			pm.polyEditUV(u=i % 10, v=int(math.floor(i / 10)))
		pm.select(sels,r=1)

	def lineUpU(self,*args):
		sels = pm.ls(sl=1)
		gap = pm.floatField("gapValueField",q=True,v=True)
		
		for x in sels:
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			w = abs(buv[0][1] - buv[0][0])
			self.W.append(w)
			
		for i, x in enumerate(sels):
			initGap = 0.003
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			if i==0:
				pm.polyEditUV(u=-buv[0][0]+initGap,v=-buv[1][0]+initGap)
			else:
				width = sum(self.W[0:i])
				pm.polyEditUV(u=-buv[0][0]+initGap+width+gap*i,v=-buv[1][0]+initGap)
		pm.select(sels,r=1)
		self.W=[]

	def lineUpV(self,*args):
		sels = pm.ls(sl=1)
		gap = pm.floatField("gapValueField",q=True,v=True)
		
		for x in sels:
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			h = abs(buv[1][1] - buv[1][0])
			self.H.append(h)
			
		for i, x in enumerate(sels):
			initGap = 0.003
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			if i==0:
				pm.polyEditUV(v=-buv[1][1]-initGap,u=-buv[0][0]+initGap)
			else:
				width = sum(self.H[0:i])
				pm.polyEditUV(v=-buv[1][1]-initGap-width-gap*i,u=-buv[0][0]+initGap)
		pm.select(sels,r=1)
		self.H=[]

	def RK_Geometric(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProGeometric")

	def RK_Organic(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProOrganic")

	def RK_Straighten(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProStraighten")

	def RK_ScaleToSrc(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProScaleToSource")
	
	def selMesh(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		if len(getSel)==0:
			pm.select(self.Sels,r=1)
			print self.Sels
		elif len(getSel)>=1:
			self.Sels=getSel
			print self.Sels

lineUpUVs()._UI()
