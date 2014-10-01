'''
Created on 18 sept. 2014

@author: gtheurillat
'''

from PyQt4 import QtGui, QtCore
import pickle, cPickle
import random

class dropZone(QtGui.QLabel):
    def __init__(self, text, listphotos, parent=None):
        super(dropZone, self).__init__(parent)
        self.setMinimumSize(200,20)
        self.color = None
        #bleu, rose, violet pale, 
        #turquoise, marine, pomme,
        #orange fonces, orange, violet fonces,
        #rose fonce, rouge, vert fonces
#         self.list_bgColor = ["#156cab", "#FC6D98", "#D0B6FA", 
#                              "#C2EBFF", "#3EFAD8", "#A5FAB5", 
#                              "#FF9245", "#FFC069", "#7276FC",
#                              "#FF00D9", "#FF0000", "#0DFF00"]
        self.list_bgColor = ["#F2B1E8",
                            "#C464B6",
                            "#56ADF5",
                            "#60D6AF",
                            "#9E0AC7",
                            "#3D51C4",
                            "#37CC5C",
                            "#F5589F",
                            "#F7197D",
                            "#F5A453"]
        
        self.set_bg()
        self.text = text
        self.setText(text.upper())
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)
        
        self.listPhotos = listphotos
        #self.model = model
        self.mode = False
        
        font = QtGui.QFont('SansSerif', 15)
        
        font.setBold(True)

        self.setFont(font)
        self.to_delete = False
        
        
        
        
    def setmode(self, mode):
        self.mode = mode
    
    def startDrag(self, event):
        #print event 
        
       
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        # example 1 - the object itself

        pixmap = QtGui.QPixmap()
        
        rect =QtCore.QRect(0,0,200,50)
        pixmap = pixmap.grabWidget(self, rect)

        # example 2 -  a plain pixmap
        #pixmap = QtGui.QPixmap(100, self.height()/2)
        #pixmap.fill(QtGui.QColor("orange"))
        drag.setPixmap(pixmap)

        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)
        #drag.exec(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
        
        ##print result
        if result: # == QtCore.Qt.MoveAction:
            if self.mode.isChecked() == True:
                self.is_find_good_photo()
        #    ""
            #self.deleteLater()
            #self.model().updateRow(index.row())
    
    def is_find_good_photo(self):
        ""
        nb_photos = self.listPhotos.count()
        for i in range(nb_photos):
            itemPhoto = self.listPhotos.item(i)
            if itemPhoto.already_find == True and itemPhoto.nom == self.text:
                self.deleteLater()
    
    def mouseMoveEvent(self, event):
        #print event.pos().x()
        #print event.pos().y()
        
        self.startDrag(event)   

        

    def dragEnterEvent(self, event):
        #print "ca rentre dans ma liost"
        event.accept()
        

    def dragMoveEvent(self, event):
        #print event.pos().x()
        #print event.pos().y()
        
        event.accept()
       

    def dragLeaveEvent(self, event):
        #print "drag leave from label"
        
        event.accept()
        #self.set_bg()

    def dropEvent(self, event):
        #print "dropevent from label"
#         data = event.mimeData()
#         data_class = data.data("application/x-eleve")
#         bstream = data.retrieveData("application/x-eleve",
#             QtCore.QVariant.ByteArray)
#         selected = pickle.loads(bstream.toByteArray())
#         
#         self.set_bg()
#         if self.text() == selected.name:
#             selected.titre = self.text()
#             
#             for elem in self.model.list:
#                 if elem.name == self.text():
#                     elem.titre = elem.name
#                     elem.delete = True
#             
#             
#             self._show_ok()
#             event.accept()
#             #self.setText(str(selected))
#         else:
#             self._show_ko("Ce n'est pas ca, recommence!")
#         event.ignore()
        event.accept()

    def set_bg(self, active=False):
        if active:
            val = "background:yellow;color:black;"
        else:
            bg_color_hex = random.choice(self.list_bgColor);
            self.color = bg_color_hex
            val = "background:{0};color:white;".format(bg_color_hex)
        self.setStyleSheet(val)

    def _show_ko(self, message):
        self.msgBox = QtGui.QMessageBox(self)
        self.msgBox.setText("Non");
        self.msgBox.setInformativeText(message);
        self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok);
        
        icon = QtGui.QPixmap("images/KO.png")
        self.msgBox.setIconPixmap(icon)
        self.msgBox.show()
        
    def _show_ok(self):
        self.msgBox = QtGui.QMessageBox(self)
        self.msgBox.setText("Oui");
        self.msgBox.setInformativeText("BRAVO");
        self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok);
        
        icon = QtGui.QPixmap("images/OK.png")
        self.msgBox.setIconPixmap(icon)
        self.msgBox.show()