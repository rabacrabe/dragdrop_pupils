# -*- coding: utf8 -*-
'''
Created on 19 sept. 2014

@author: gtheurillat
'''
from PyQt4 import QtGui, QtCore

class CustomQListWidgetItem(QtGui.QListWidgetItem):
    ""
    def __init__(self, nom, icon):
        super(CustomQListWidgetItem, self).__init__(icon, "")
        self.nom = nom
        self.already_find = False
        
    def dragEnterEvent(self, event):
        #print "dragevent dans item"
        event.accept()
    

class DropPhotosList(QtGui.QListWidget):
    ""
    
    def __init__(self, parent=None):
        super(DropPhotosList, self).__init__(parent)
        self.setAcceptDrops(True)
        self.layoutG = None
        self.layoutD = None
        self.mode = False
        
    def dragEnterEvent(self, event):
        #print "dragevent dans photo"
        event.accept()
    
    
    def dropEvent(self, event):
        #print "drop photo on position: x: {0}, y: {1}".format(event.pos().x(), event.pos().y())
        element = self.itemAt(event.pos().x(), event.pos().y())
        if element is not None:
            #print "sur l'element: {0}".format(element.nom)
            
            data = event.mimeData()
            src_name = data.text()
            #print "src: {0}".format(src_name)
            #print data
            if src_name == element.nom:
                brush = QtGui.QBrush(QtGui.QColor(21,108,171))
                element.setBackground(brush)
                
                brush = QtGui.QBrush(QtGui.QColor(255,255,255))
                element.setForeground (brush)
                
                element.setText(src_name)
                element.already_find = True
                
                #self.findAnddeleteSticker(src_name)
                
                self._show_ok()
                self.uncolor_all()
                
                event.accept()
                
            else:
                self._show_ko()
                self.uncolor_all()
                
                #event.ignore()
        else:
            #print "Aucun element"
            self.uncolor_all()
            #event.ignore()
            
        
        
        
    def dragLeaveEvent(self, event):
        #print "drag leave pthot"
        self.uncolor_all()
        event.accept()

    def dragMoveEvent(self, event):
        #print "drag move event"
        #print "mouse position x: {0}, y: {1}".format(event.pos().x(), event.pos().y())
        
        self.uncolor_all()
        
        element = self.itemAt(event.pos().x(), event.pos().y())
        if element is not None and element.already_find == False:
            brush = QtGui.QBrush(QtGui.QColor(255,255,0))
            element.setBackground(brush)
        
            
        event.accept()
    
    def uncolor_all(self):
        brush = QtGui.QBrush(QtGui.QColor("#34277D"))
        nb_item = self.count()
        
        for i in range(nb_item):
        
            item = self.item(i)
            if item.already_find == False:
                item.setBackground(brush)   
    
    def findAnddeleteSticker(self, stickername):
        nbD =  self.layoutD.count()
        for i in range(nbD):
            stickerD = self.layoutD.itemAt(i)
            #del stickerD
            
    
    def mouseMoveEvent(self, event):
        #print "mouse position x: {0}, y: {1}".format(event.pos().x(), event.pos().y())
        
        event.accept()
        
    def _show_ko(self):
        self.msgBox = QtGui.QMessageBox(self)
        #self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok);
        
        self.msgBox.setStyleSheet ("QPushButton {background : white;")
        
        button = QtGui.QPushButton('RECOMMENCE')
        button.setMinimumSize(250, 100)
        button.setStyleSheet ("QPushButton {background : #F2B1E8; font-size:35px;}")  
        
        self.msgBox.addButton(button, QtGui.QMessageBox.YesRole)
        
        icon = QtGui.QPixmap("images/KO.png")
        self.msgBox.setIconPixmap(icon)
        self.msgBox.show()
        
    def _show_ok(self):
        self.msgBox = QtGui.QMessageBox(self)
        #self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok);
        
        self.msgBox.setStyleSheet ("QPushButton {background : white;")
        
        button = QtGui.QPushButton('BRAVO')
        button.setMinimumSize(250, 100)
        button.setStyleSheet ("QPushButton {background : #F2B1E8; font-size:75px;}")  
        
        self.msgBox.addButton(button, QtGui.QMessageBox.YesRole)
        
        icon = QtGui.QPixmap("images/OK.png")
        self.msgBox.setIconPixmap(icon)
        self.msgBox.show()
        
    def _show_warning(self, path):
        self.msgBox = QtGui.QMessageBox(self)
        #self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok);
        #self.msgBox.setStandardButtons(QtGui.QMessageBox.Ko);
        
        self.msgBox.addButton(QtGui.QPushButton('Oui'), QtGui.QMessageBox.YesRole)
        self.msgBox.addButton(QtGui.QPushButton('Non'), QtGui.QMessageBox.NoRole)
        
        self.msgBox.setText("�tes vous certain de vouloir charger le contenu du r�pertoire '{0}'?\n La taille des photos pr�sentes seront modifi�es de mani�re irr�versible.".format(path))
        icon = QtGui.QPixmap("images/WARNING.png")
        self.msgBox.setIconPixmap(icon)
        self.msgBox.show()
    
    def setLayoutD(self, layoutD):
        self.layoutD = layoutD
        
    def setLayoutG(self, layoutG):
        self.layoutG = layoutG
        
    def setMode(self, mode):
        self.mode = mode