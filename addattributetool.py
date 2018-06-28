# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.PyQt.QtCore import *
import math
import resources
import sys

## Import own classes and tools.
from addattributegui import AddAttributeGui
import utils

class AddAttributeTool:
    
    def __init__(self, iface,  toolBar):
        self.iface = iface
        self.layer = self.iface.activeLayer()
        self.canvas = self.iface.mapCanvas()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  
        self.ctrl = AddAttributeGui(self.iface.mainWindow(),  flags)
        self.attribute = self.ctrl.attribute_list
        
        self.act_addattribute = QAction(QIcon(":/plugins/QuickDigitize/icon.png"), QCoreApplication.translate("ctools", "Add Attributes"),  self.iface.mainWindow())
        try:
            if self.layer.isEditable():
                self.act_addattribute.setEnabled(True)
                
                self.layer.editingStopped.connect(self.toggle)
        except:
            pass
            
        else:
            self.act_addattribute.setEnabled(False)
            # self.act_s2v.setEnabled(False)
            self.layer.editingStarted.connect(self.toggle)
             
        self.act_addattribute.triggered.connect(self.showDialog)
        self.iface.currentLayerChanged["QgsMapLayer *"].connect(self.toggle)
        self.canvas.selectionChanged.connect(self.toggle)
        


        toolBar.addSeparator()
        toolBar.addAction(self.act_addattribute)
        # self.iface.editMenu().addAction(self.act_addattribute)


        


    def toggle(self):
        if self.layer and self.layer.type() == self.layer.VectorLayer:
            # disconnect all previously connect signals in current layer
            try:
                self.layer.editingStarted.disconnect(self.toggle)
            except:
                pass
            try:
                self.layer.editingStopped.disconnect(self.toggle)
            except:
                pass
            
            # check if current layer is editable and has selected features
            # and decide whether the plugin button should be enable or disable
            if self.layer.isEditable():
                self.act_addattribute.setEnabled(True)
                self.layer.editingStopped.connect(self.toggle)
            # layer is not editable    
            else:
                self.act_addattribute.setEnabled(False)
                self.layer.editingStarted.connect(self.toggle)
        else:
            self.act_addattribute.setEnabled(False)

    def showDialog(self):
        self.ctrl.initGui()
        self.ctrl.show()
        self.ctrl.accept()
        
        self.ctrl.okButton.clicked.connect(self.newattribute)
        self.ctrl.okButton.clicked.connect(self.close_func)
        pass


    def newattribute(self):
        self.attribute = self.ctrl.attribute_list
        self.newfeature = QgsFeature(self.layer.fields())
        self.newfeature_list = self.layer.selectedFeatures()
        self.newfeature = self.newfeature_list[0]
        # self.layer.startEditing()
        self.layer.updateFields()
        
        self.newfeature.setAttributes(self.attribute)
        self.layer.updateFeature(self.newfeature)
        # self.layer.commitChanges()
        del self.newfeature
        del self.attribute


    def close_func(self):
        self.ctrl.close()

    
    
