from qgis.core import QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsWkbTypes, QgsPoint, QgsPointXY, \
    QgsSnappingUtils, QgsSnappingConfig, QgsTolerance
from qgis.gui import QgsMapCanvas, QgsMapTool, QgsRubberBand, QgsMapToolEmitPoint, QgsSnapIndicator
from qgis.PyQt.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor
from qgis.utils import iface


# Create a map tool to draw the polyline
class PolylineMapTool(QgsMapTool):
    polylineFinished = pyqtSignal(QgsFeature)

    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas
        self.nb_pts_poly = 100
        self.points = []
        self.rb = QgsRubberBand(canvas, QgsWkbTypes.LineGeometry)
        self.rb.setColor(QColor(255, 0, 0))
        self.rb.setLineStyle(Qt.DotLine)
        self.rb.setWidth(1)
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.snapper = canvas.snappingUtils()
        self.rb.show()

    def canvasPressEvent(self, e):
        current_point = self.toMapCoordinates(e.pos())
        if e.button() == Qt.LeftButton:
            # Try to snap to an existing vertex
            snapMatch = self.snapper.snapToMap(e.pos())
            self.snapIndicator.setMatch(snapMatch)
            if self.snapIndicator.match().type():
                current_point = self.snapIndicator.match().point()
            self.points.append(current_point)
            self.rb.addPoint(self.points[-1])
            self.rb.show()
            if len(self.points) == self.nb_pts_poly:
                self.finishPolyline()

    def canvasReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            self.finishPolyline()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.points = []
            self.rb.reset(QgsWkbTypes.LineGeometry)

    def canvasMoveEvent(self, e):
        # Try to snap to an existing vertex
        snapMatch = self.snapper.snapToMap(e.pos())
        self.snapIndicator.setMatch(snapMatch)
        if len(self.points) > 0:
            current_point = self.toMapCoordinates(e.pos())
            if self.snapIndicator.match().type():
                current_point = self.snapIndicator.match().point()
            self.rb.movePoint(current_point)

    def finishPolyline(self):
        if len(self.points) > 1:
            feat = QgsFeature(iface.activeLayer().fields())
            feat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(p) for p in self.points]))
            # iface.activeLayer().dataProvider().addFeatures([feat])
            # self.canvas.refresh()
            # iface.activeLayer().triggerRepaint()
            self.rb.reset(QgsWkbTypes.LineGeometry)
            # self.polylineFinished.emit(self.points)
            self.polylineFinished.emit(feat)
        self.points = []
        self.rb.reset(QgsWkbTypes.LineGeometry)
