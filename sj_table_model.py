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
from PyQt4.QtGui import QColor, QBrush
import logging

class MyTableModel(QAbstractTableModel):
    """
    This class subclasses QAbstractTableModel and provides the data to be 
    displayed in the table.
    """
    def __init__(self, datain, headerdata, conditional_formatting_config_dict, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata
        self.foreground_key_column          = conditional_formatting_config_dict["foreground_key_column"]
        self.foreground_color_dict          = conditional_formatting_config_dict["foreground_color_dict"]
        self.background_key_column          = conditional_formatting_config_dict["background_key_column"]
        self.background_color_dict          = conditional_formatting_config_dict["background_color_dict"]
        self.special_formatting_column      = conditional_formatting_config_dict["special_formatting_key_column"]
        self.special_formatting_color_dict  = conditional_formatting_config_dict["special_formatting_color_dict"]

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
                if((index.column() == self.special_formatting_column) and (index.data() in self.special_formatting_color_dict)):
                    return QColor(self.special_formatting_color_dict[index.data()]["foreground"])

                else:
                    return self.getConditionalFormattingColor(
                        index.row(),
                        self.foreground_color_dict,
                        self.foreground_key_column)
            elif(role == Qt.BackgroundRole):
                if((index.column() == self.special_formatting_column) and (index.data() in self.special_formatting_color_dict)):
                    return QBrush(QColor(self.special_formatting_color_dict[index.data()]["background"]))
                else:
                    return QBrush(self.getConditionalFormattingColor(
                        index.row(),
                        self.background_color_dict,
                        self.background_key_column))
            else:
                return None

    def headerData(self, section, orientation, role):
        """
        Returns the header data.
        """
        if(role == Qt.DisplayRole):
            if(orientation == Qt.Horizontal):
                return self.headerdata[section]
            elif(orientation == Qt.Vertical):
                return section
        return None

    def getConditionalFormattingColor(self, row, color_dict, key_column):
        """
        Returns a color to use in colorizing the given row's foreground/background
        based on the matching the key cell with the given color dictionary.
        """
        cell_value = self.arraydata[row][key_column]
        if(cell_value in color_dict):
            return QColor(color_dict[cell_value])

