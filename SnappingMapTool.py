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

from qgis.gui import QgsMapToolEmitPoint, QgsSnapIndicator
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsPointXY
from PyQt5.QtCore import pyqtSignal, pyqtSlot

#Outil fonctionnant avec accrochage
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

