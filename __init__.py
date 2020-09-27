# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BnicNancy
                                 A QGIS plugin
 Ensemble d'outils utilsés par la Brigade Nationale d'Intervention Cadastrale de Nancy
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-02-24
        copyright            : (C) 2020 by Marius François-Marchal
        email                : m.francois.marchal@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load BnicNancy class from file BnicNancy.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .BnicNancy import BnicNancy
    return BnicNancy(iface)