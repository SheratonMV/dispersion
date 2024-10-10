import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PIL import Image
from mpi4py import MPI
global comm
comm = MPI.COMM_WORLD

class ProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(ProxyModel,self).__init__(parent)
        self._root_path = ""

    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()
        if self._root_path and isinstance(source_model, QtWidgets.QFileSystemModel):
            root_index = source_model.index(self._root_path).parent()
            if root_index == source_parent:
                index = source_model.index(source_row, 0, source_parent)
                return index.data(QtWidgets.QFileSystemModel.FilePathRole) == self._root_path
        return True

    @property
    def root_path(self):
        return self._root_path

    @root_path.setter
    def root_path(self, p):
        self._root_path = p
        self.invalidateFilter()



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.model = QtGui.QStandardItemModel()
        uic.loadUi("form.ui", self)
        self.treeView.setObjectName("Folder View")
        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setRootPath(QtCore.QDir.rootPath())
        self.dirModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs | QtCore.QDir.Files)
        self.proxy = ProxyModel(self.dirModel)
        self.proxy.setSourceModel(self.dirModel)
        self.treeView.setModel(self.proxy)

        self.gvzoom = 0
        self.gvempty = True
        self.gv1.scene = QtWidgets.QGraphicsScene(self)
        self.gvphoto = QtWidgets.QGraphicsPixmapItem()
        self.gv1.scene.addItem(self.gvphoto)
        self.gv1.setScene(self.gv1.scene)
        self.gv1.setTransformationAnchor(self.gv1.AnchorUnderMouse)
        self.gv1.setResizeAnchor(self.gv1.AnchorUnderMouse)
        self.gv1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv1.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.gv1.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.lv1.setModel(self.model)
        self.pb1.clicked.connect(self.openFileNamesDialog)

    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.filelist, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                          "All Files (*);;Python Files (*.py)", options=options)

        self.model.clear()

        for i in self.filelist:
            item = QtGui.QStandardItem(i)
            self.model.appendRow(item)
        self.firstfile = os.path.dirname(self.filelist[0])
        #removedbg = bgrem.run(self.filelist[0])
        try:
            #im = Image.open(self.filelist[0])
            # self.bgremimage = QtGui.QImage(removedbg, removedbg.shape[1], removedbg.shape[0], QtGui.QImage.Format_RGB888)
            # self.setPhoto(QtGui.QPixmap.fromImage(self.bgremimage))
            a=0
        except IOError:
            pass
        self.setfiletree()
        self.process_files()

    def process_files(self):
        global comm
        size = comm.Get_size()
        print (size)
        a=1

    def setfiletree(self):
        path = self.firstfile

        root_index = self.dirModel.index(path).parent()
        self.proxy.root_path = path
        proxy_root_index = self.proxy.mapFromSource(root_index)
        self.treeView.setRootIndex(proxy_root_index)
        #self.treeView.setHeaderHidden(True)
        self.treeView.clicked.connect(self.tree_click)
    # @pyqtSlot(QtCore.QModelIndex)
    def tree_click(self, index):
        ix = self.proxy.mapToSource(index)

        try:
            im = Image.open(ix.data(QtWidgets.QFileSystemModel.FilePathRole))
            self.setPhoto(QtGui.QPixmap(ix.data(QtWidgets.QFileSystemModel.FilePathRole)))
        except IOError:
            pass
    def hasPhoto(self):
        return not self.gvempty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self.gvphoto.pixmap().rect())
        if not rect.isNull():
            self.gv1.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.gv1.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.gv1.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.gv1.viewport().rect()
                scenerect = self.gv1.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.gv1.scale(factor, factor)
            self.gvzoom = 0

    def setPhoto(self, pixmap=None):
        self.gvzoom = 0
        if pixmap and not pixmap.isNull():
            self.gvempty = False
            self.gv1.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.gvphoto.setPixmap(pixmap)
        else:
            self.gvempty = True
            self.gv1.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.gvphoto.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self.gvzoom += 1
            else:
                factor = 0.8
                self.gvzoom -= 1
            if self.gvzoom > 0:
                self.gv1.scale(factor, factor)
            elif self.gvzoom == 0:
                self.fitInView()
            else:
                self.gvzoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self.gvphoto.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(open("stylesheet.qss").read())
window = MainWindow()
window.show()
app.exec_()
