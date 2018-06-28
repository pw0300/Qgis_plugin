# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import math
import resources

## Import own classes and tools.
from vertexandobjectfindertool import VertexAndObjectFinderTool
from rotateobjectgui import RotateObjectGui
import utils

class RotateObjectTool:
    
    def __init__(self, iface,  toolBar):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.layer= self.iface.activeLayer()

        
        self.p1 = None
        self.m1 = None
        self.feat = None
        self.rb = None
        
        self.act_rotateobject = QAction(QIcon(":/plugins/cadtools/icons/rotatefeature.png"), QCoreApplication.translate("ctools", "Rotate Object"),  self.iface.mainWindow())
        self.act_selectvertexandobject= QAction(QIcon(":/plugins/cadtools/icons/selectvertexandfeature.png"), QCoreApplication.translate("ctools", "Select Vertex and Object"),  self.iface.mainWindow())
        self.act_selectvertexandobject.setCheckable(True)     
        try:
                if self.layer.isEditable():
                    self.act_rotateobject.setEnabled(True)
                    self.act_selectvertexandobject.setEnabled(True)
                    self.layer.editingStopped.connect(self.toggle_1)
        except:
            pass
            
        else:
            self.act_rotateobject.setEnabled(False)
            self.act_selectvertexandobject.setEnabled(False)
            self.layer.editingStarted.connect(self.toggle_1)
             
        
        # self.iface.currentLayerChanged["QgsMapLayer *"].connect(self.toggle_1)
        # self.canvas.selectionChanged.connect(self.toggle_1)
             
        self.act_rotateobject.triggered.connect(self.showDialog)
        self.act_selectvertexandobject.triggered.connect(self.selectvertexandobject)
        self.canvas.mapToolSet.connect(self.deactivate)

        toolBar.addSeparator()
        toolBar.addAction(self.act_selectvertexandobject)
        toolBar.addAction(self.act_rotateobject)
                    
        self.tool = VertexAndObjectFinderTool(self.canvas)   


    def toggle_1(self):
            if self.layer:
                # disconnect all previously connect signals in current layer
                try:
                    self.layer.editingStarted.disconnect(self.toggle_1)
                except:
                    pass
                try:
                    self.layer.editingStopped.disconnect(self.toggle_1)
                except:
                    pass
                
                # check if current layer is editable and has selected features
                # and decide whether the plugin button should be enable or disable
                if self.layer.isEditable():
                    self.act_rotateobject.setEnabled(True)
                    self.act_selectvertexandobject.setEnabled(True)
                    self.layer.editingStopped.connect(self.toggle_1)
                # layer is not editable    
                else:
                    self.act_rotateobject.setEnabled(False)
                    self.act_selectvertexandobject.setEnabled(False)
                    self.layer.editingStarted.connect(self.toggle_1)
            else:
                self.act_rotateobject.setEnabled(False)
                self.act_selectvertexandobject.setEnabled(False)

    def selectvertexandobject(self):
        mc = self.canvas
        mc.setMapTool(self.tool)
        
        self.act_selectvertexandobject.setChecked(True)       
 
        self.tool.vertexAndObjectFound.connect(self.storeVertexAndObject)
 
        pass
        
    def storeVertexAndObject(self,  result):
        self.p1 = result[0]
        self.feat = result[1]
        self.m1 = result[2]
        self.rb = result[3]
    
    
    def showDialog(self):

        if self.p1 == None or self.feat == None:
            QMessageBox.information(None, QCoreApplication.translate("ctools", "Cancel"), QCoreApplication.translate("ctools", "Not enough objects selected."))
        else:
            #az = Azimuth.calculate(self.p1,  self.p2)
            
            flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  
            self.ctrl_1 = RotateObjectGui(self.iface.mainWindow(),  flags)
            self.ctrl_1.initGui()
            self.ctrl_1.show()

            self.ctrl_1.okClicked.connect(self.rotateObject)
            self.ctrl_1.unsetTool.connect(self.unsetTool)
        
        pass


    def rotateObject(self,  angle):
        geom = utils.rotate(self.feat.geometry(), self.p1,  angle * math.pi / 180)
        if geom <> None:
            utils.addGeometryToLayer(geom,self.iface)
            self.canvas.refresh()

        
    def unsetTool(self):
        self.m1 = None
        self.rb.reset()
        mc = self.canvas
        mc.unsetMapTool(self.tool)             
        
        
    def deactivate(self):
        self.p1 = None
        self.act_selectvertexandobject.setChecked(False)
    
