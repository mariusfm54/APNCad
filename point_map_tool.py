"""
/***************************************************************************
 SnappingMapToolEmitPoint
                                 A QGIS plugin
 Applicatif destiné à la prise de notes sur tablette numérique lors des opérations de terrain réalisées pendant le remaniement cadastral
                             -------------------
        begin                : 2020-02-24
        git sha              : https://github.com/mariusfm54/APNCad
        copyright            : (C) 2020 by Marius François-Marchal
        email                : m.francois.marchal@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsPointXY
from qgis.gui import QgsMapToolEmitPoint, QgsSnapIndicator


class PointMapTool(QgsMapToolEmitPoint):
    snap_clicked = pyqtSignal(QgsPointXY, Qt.MouseButton)

    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas

        # noinspection PyUnresolvedReferences
        self.canvasClicked.connect(self.snap_click)
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.snapper = self.canvas.snappingUtils()

    def canvasMoveEvent(self, e):
        snap_match = self.snapper.snapToMap(e.pos())
        self.snapIndicator.setMatch(snap_match)

    @pyqtSlot(QgsPointXY, Qt.MouseButton)
    def snap_click(self, point, button):
        if self.snapIndicator.match().type():
            point = self.snapIndicator.match().point()
        self.snap_clicked.emit(point, button)
