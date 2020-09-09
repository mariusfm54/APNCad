from qgis.gui import QgsMapToolEmitPoint, QgsSnapIndicator
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsPointXY
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class SnappingMapToolEmitPoint(QgsMapToolEmitPoint):
    snapClicked = pyqtSignal(QgsPointXY, Qt.MouseButton)

    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas
        self.canvasClicked.connect(self.snapClick)
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.snapper = self.canvas.snappingUtils()

    def canvasMoveEvent(self, e):
        snapMatch = self.snapper.snapToMap(e.pos())
        self.snapIndicator.setMatch(snapMatch)

    @pyqtSlot(QgsPointXY, Qt.MouseButton)
    def snapClick(self, point, button):
        if self.snapIndicator.match().type():
            point = self.snapIndicator.match().point()
        self.snapClicked.emit(point, button)

