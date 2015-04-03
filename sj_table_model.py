#!/usr/bin/python3

################################################################################
# Copyright 2015 Mohamed Galal El-Din Ebrahim (mohamed.g.ebrahim@gmail.com)
################################################################################
# This file is part of siraj.
# 
#     siraj is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License.
#     
#     siraj is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     
#     You should have received a copy of the GNU General Public License
#     along with siraj.  If not, see <http://www.gnu.org/licenses/>.
# 
################################################################################
from PyQt4.QtCore import QAbstractTableModel, Qt
from PyQt4.QtGui import QColor
import logging

class MyTableModel(QAbstractTableModel):
    """
    This class subclasses QAbstractTableModel and provides the data to be 
    displayed in the table.
    """
    def __init__(self, datain, headerdata, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        """
        Returns the number of rows in the table
        """
        return len(self.arraydata)

    def columnCount(self, parent):
        """
        Returns the number of columns in a table.
        """
        return len(self.arraydata[0])

    def data(self, index, role):
        """
        Returns the data stored at the given index (row and column)
        """
        if(False == index.isValid()):
            return None
        else:
            if(role == Qt.DisplayRole):
                return self.arraydata[index.row()][index.column()]
            elif(role == Qt.ForegroundRole):
                row = index.row()
                return self.getForgroundColor(row)#QColor("red")
            else:
                return None

    def headerData(self, section, orientation, role):
        """
        Returns the header data
        """
        if(role == Qt.DisplayRole):
            if(orientation == Qt.Horizontal):
                return self.headerdata[section]
            elif(orientation == Qt.Vertical):
                return section
        return None

    def getForgroundColor(self, row):
        if(self.arraydata[row][0] == "DEBUG"):
            return QColor("red")
        else:            
            return QColor("green")

        