# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickDigitize
                                 A QGIS plugin
 Combines advanced digitization
                             -------------------
        begin                : 2018-06-18
        copyright            : (C) 2018 by Pratik and Sanjutha
        email                : sanjuthaindrajit97@gmail.com
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
    """Load QuickDigitize class from file QuickDigitize.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .quick_digitize import QuickDigitize
    return QuickDigitize(iface)
