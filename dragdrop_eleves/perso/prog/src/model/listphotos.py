'''
Created on 18 sept. 2014

@author: gtheurillat
'''

from PyQt4 import QtGui, QtCore
import cPickle


class draggableList(QtGui.QListView):
    '''
    a listView whose items can be moved
    '''
    def ___init__(self, parent=None):
        super(draggableList, self).__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        
        
        

    def dragEnterEvent(self, event):
        print "dragevent dans photo"
        event.accept()

    def startDrag(self, event):
        index = self.indexAt(event.pos())
        
        if not index.isValid():
            return

        ## selected is the relevant eleve object
        selected = self.model().data(index,QtCore.Qt.UserRole)

        ## convert to  a bytestream
        bstream = cPickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-eleve", bstream)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)

        # example 1 - the object itself

        pixmap = QtGui.QPixmap()
        pixmap = pixmap.grabWidget(self, self.rectForIndex(index))

        # example 2 -  a plain pixmap
        #pixmap = QtGui.QPixmap(100, self.height()/2)
        #pixmap.fill(QtGui.QColor("orange"))
        drag.setPixmap(pixmap)

        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)
        result = drag.start(QtCore.Qt.MoveAction)
        
        
        if result: # == QtCore.Qt.MoveAction:
            self.model().updateRow(index.row())

    def dropEvent(self, event):
        print "drop photo on position: x: {0}, y: {1}".format(event.pos().x(), event.pos().y())
        element = self.indexAt(QtCore.QPoint(event.pos().x(), event.pos().y()))
        print element
        event.accept()
        
    def dragLeaveEvent(self, event):
        print "drag leave pthot"
        event.accept()

    def dragMoveEvent(self, event):
        
#         if event.mimeData().hasFormat("application/x-eleve"):
#             event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()
#         else:
#             event.ignore()

    def mouseMoveEvent(self, event):
        self.startDrag(event)
        
class eleve(object):
    '''
    a custom data structure, for example purposes
    '''
    def __init__(self, name, photo_path):
        self.name = name
        self.photo_path = photo_path
        self.titre = ""
        self.is_drop_ok = False
        self.delete = False
        
    def __repr__(self):
        return "%s\n%s\n"% (self.name, self.photo_path)

class simple_model(QtCore.QAbstractListModel):
    def __init__(self, map_eleves, parent=None):
        super(simple_model, self).__init__(parent)
        self.list = []
        for name, photo_path in map_eleves.iteritems():
            self.list.append(eleve(name, photo_path))
            
        self.setSupportedDragActions(QtCore.Qt.MoveAction)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role):
        
        if role == QtCore.Qt.DisplayRole: #show just the name
            eleve = self.list[index.row()]
            return QtCore.QVariant(eleve.titre)

            
        elif role == QtCore.Qt.UserRole:  #return the whole python object
            eleve = self.list[index.row()]
            return eleve
        
        elif role == QtCore.Qt.DecorationRole:
            eleve = self.list[index.row()]
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8(eleve.photo_path)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            return icon

        return QtCore.QVariant()

    def updateRow(self, position):
        elem = self.list[position]
        print elem.is_drop_ok
        #elem.titre = "toto"
        if elem.delete == True:
            self.list = self.list[:position] + self.list[position+1:]
        self.reset()
        ""