from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from qgis.PyQt.QtCore import Qt
from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsWkbTypes,
    QgsPointXY,
)
from qgis.gui import QgsMapTool, QgsRubberBand, QgsSnapIndicator
from qgis.utils import iface


# Create a map tool to draw the polyline
class PolygonMapTool(QgsMapTool):
    polygon_finished = pyqtSignal(QgsFeature)

    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas
        self.nb_pts_poly = 100
        self.points = []
        self.rb = QgsRubberBand(canvas, QgsWkbTypes.PolygonGeometry)
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
            snap_match = self.snapper.snapToMap(e.pos())
            self.snapIndicator.setMatch(snap_match)
            if self.snapIndicator.match().type():
                current_point = self.snapIndicator.match().point()
            self.points.append(current_point)
            self.rb.addPoint(self.points[-1])
            self.rb.show()
            if len(self.points) == self.nb_pts_poly:
                self.finish_polygon()

    def canvasReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            self.finish_polygon()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.points = []
            self.rb.reset(QgsWkbTypes.PolygonGeometry)

    def canvasMoveEvent(self, e):
        # Try to snap to an existing vertex
        snap_match = self.snapper.snapToMap(e.pos())
        self.snapIndicator.setMatch(snap_match)
        if len(self.points) > 0:
            current_point = self.toMapCoordinates(e.pos())
            if self.snapIndicator.match().type():
                current_point = self.snapIndicator.match().point()
            self.rb.movePoint(current_point)

    def finish_polygon(self):
        if len(self.points) > 1:
            feat = QgsFeature(iface.activeLayer().fields())
            feat.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(p) for p in self.points]]))
            self.rb.reset(QgsWkbTypes.LineGeometry)
            self.polygon_finished.emit(feat)
        self.points = []
        self.rb.reset(QgsWkbTypes.PolygonGeometry)
