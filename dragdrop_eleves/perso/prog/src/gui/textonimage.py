# -*- coding: utf8 -*-
'''
Created on 17 sept. 2014

@author: gtheurillat
'''


from PyQt4 import QtGui, QtCore
import sys, os
import pickle
import cPickle
from perso.prog.src.model.labelnom import dropZone
from perso.prog.src.model.listphotos import draggableList, simple_model
from perso.prog.src.model.listphotos2 import DropPhotosList, CustomQListWidgetItem
from perso.prog.src.controller.imageutil import ImageUtil
import random





class Test(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__()
        self.setWindowTitle(u"Glissé - Déposé")
        
        window_icon = QtGui.QIcon("images/icon2.ico") 
        self.setWindowIcon(window_icon) 
        
        myQWidget = QtGui.QWidget()
        myCenterBoxLayout = QtGui.QVBoxLayout()
        myBoxLayout = QtGui.QHBoxLayout()
        self.myBoxLayoutNomsG = QtGui.QVBoxLayout()
        self.myBoxLayoutNomsD = QtGui.QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)

        
       
        self.listPhotos = DropPhotosList()
        self.del_etiquette = False
       
        #on cree le menu
        self.createMenu()
       
        #on rempli les donnee
        #mapPhotos = self.get_photosMap()
        #self.fillin_data(mapPhotos)
        
        
        
        
        self.listPhotos.setIconSize(QtCore.QSize(200, 150))
        self.listPhotos.setFlow(QtGui.QListView.LeftToRight)
        self.listPhotos.setWrapping(True)
        self.listPhotos.setResizeMode(QtGui.QListView.Adjust);
        #self.listPhotos.setTextElideMode(QtCore.Qt.ElideMiddle);
        self.listPhotos.setViewMode(QtGui.QListView.IconMode)
        self.listPhotos.setAcceptDrops(True)
#         self.setMovement(QtGui.QListView.Static);
        font = QtGui.QFont('SansSerif', 15)
        
        font.setBold(True)

        self.listPhotos.setFont(font)
        
        self.listPhotos.setLayoutD(self.myBoxLayoutNomsD)
        self.listPhotos.setLayoutG(self.myBoxLayoutNomsG)
        self.listPhotos.setMode(self.del_etiquette)
        self.listPhotos.setStyleSheet("background:#34277D;")
        
        
        self.slider_size = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider_size.setRange(0, 200)
        self.slider_size.setValue(200)
        self.slider_size.valueChanged.connect(self.slider_moved)
        
        myCenterBoxLayout.addWidget(self.slider_size)
        myCenterBoxLayout.addWidget(self.listPhotos)
        
        myBoxLayout.addLayout(self.myBoxLayoutNomsG)
        myBoxLayout.addLayout(myCenterBoxLayout)      
        #myBoxLayout.addWidget(self.listPhotos)
        myBoxLayout.addLayout(self.myBoxLayoutNomsD)     


        #myMainBoxLayout.addLayout(myBoxLayout)
    
    def slider_moved(self):
        ""
        
        value = self.slider_size.value()
        print "slider move: {0}".format(value)
        
        #new value for list icon size
        new_height = (150 * int(value)) / 200
        self.listPhotos.setIconSize(QtCore.QSize(value, new_height))
        
    
    def createMenu(self):
        #gestion du menu
        #chargement des photso
        loadAction = QtGui.QAction(QtGui.QIcon(''), '&Charger les photos', self)        
        #exitAction.setShortcut('Ctrl+Q')
        loadAction.setStatusTip('Selectionne le repertoire des photos')
        loadAction.triggered.connect(self.select_inputFolder)
        
        #selection du mode
        self.modeAction = QtGui.QAction(QtGui.QIcon(''), '&Supprimer etiquettes', self)        
        #exitAction.setShortcut('Ctrl+Q')
        self.modeAction.setStatusTip('Supprimer etiquettes apres validation')
        self.modeAction.setCheckable(True)
        self.modeAction.triggered.connect(self.manage_mode)
        
        
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(self.modeAction)
    
    def fillin_data(self, mapPhotos):
        count = 0
        list_etiquette=[]
        for nom, photopath in mapPhotos.iteritems():
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8(photopath)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            photoItem = CustomQListWidgetItem(nom, icon)
            self.listPhotos.addItem(photoItem)
            
            list_etiquette.append(nom)
        
        #on melange la list
        random.shuffle(list_etiquette)#sthash.7I9UwiB9.dpuf.sort()
        for nom_etiquette in list_etiquette:
            newzone = dropZone(nom_etiquette, self.listPhotos)
            newzone.setmode(self.modeAction)
            if count <= len(mapPhotos)/2:
                self.myBoxLayoutNomsG.addWidget(newzone)
            else:
                self.myBoxLayoutNomsD.addWidget(newzone)
            
            count += 1
    
    def manage_mode(self):
        ##print "changement du mode des etiquette"
        if self.del_etiquette == False:
            self.del_etiquette = True
        else:
            self.del_etiquette = False
            
    
    def select_inputFolder(self):
        folder_path = QtGui.QFileDialog.getExistingDirectory(self, 'Select photos folder')
        if folder_path:
            
            reply = QtGui.QMessageBox.question(None,'Warning!!',u"Êtes vous certain de vouloir charger le contenu du répertoire '{0}'?\n La taille des photos présentes seront modifiées de maniére irréversible.".format(folder_path),QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                #print "selection du repertoire: {0}".format(folder_path)
                mapPhotos = self.get_photosMap(unicode(folder_path))
                self.fillin_data(mapPhotos)
                print 'Yes'
            else:
                print 'No'
            
            
    
    def get_photosMap(self, reppath):
        ""
        mapPhotos = {}
        rep = reppath#os.path.normpath("C:/Users/gtheurillat/Pictures/test")
        
        imageutil = ImageUtil()
        
        if os.path.exists(rep):
            for photos in os.listdir(rep):
                extension = os.path.splitext(photos)[-1]
                #print extension
                if extension.lower() == ".jpg":
                    path = os.path.join(rep, photos)
                    name = os.path.splitext(photos)[0]
                    mapPhotos[name] = path
                    #print name
                    
                    imageutil.resize(path, path, 600)
        return mapPhotos
    
    def _show_warning(self, path):
        self.msgBox = QtGui.QMessageBox(self)
        #self.msgBox.setStandardButtons(QtGui.QMessageBox.Ok);
        #self.msgBox.setStandardButtons(QtGui.QMessageBox.Ko);
        
        self.msgBox.addButton(QtGui.QPushButton('Oui'), QtGui.QMessageBox.YesRole)
        self.msgBox.addButton(QtGui.QPushButton('Non'), QtGui.QMessageBox.NoRole)
        
        self.msgBox.setText("Êtes vous certain de vouloir charger le contenu du répertoire '{0}'?\n La taille des photos présentes seront modifiées de maniére irréversible.".format(path))
        icon = QtGui.QPixmap("images/WARNING.png")
        self.msgBox.setIconPixmap(icon)
        self.msgBox.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog_1 = Test()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())
