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
# from PyQt4.QtCore import QAbstractTableModel, Qt
from PyQt4.QtGui import QSortFilterProxyModel
import logging

class MySortFilterProxyModel(QSortFilterProxyModel):
    
    """
    This class extends QSortFilterProxyModel by providing multi-column filtering
    """
    def __init__(self, parent = None):
        QSortFilterProxyModel.__init__(self, parent)
        self.is_filter_out = True
        self.filter_in_list = list()
        self.filter_out_list = list()
    def setSourceModel(self, model):
        QSortFilterProxyModel.setSourceModel(self, model)
        self.column_count = self.sourceModel().columnCount(None)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        
        if(self.is_filter_out):
            show_row = True
            for column, column_filter_out_set in enumerate(self.filter_out_list):
                index = self.sourceModel().index(sourceRow, column, sourceParent)
                if(index.data() in column_filter_out_set):
                    show_row = False
                    break
        else: # filter-in mode
            show_row = True
            for column, column_filter_in_set in enumerate(self.filter_in_list):
                if(len(column_filter_in_set) > 0):
                    index = self.sourceModel().index(sourceRow, column, sourceParent)
                    if(index.data() not in column_filter_in_set):
                        show_row = False
                        break
        return show_row
    
    def setFilterOutList(self, filter_out_list):
        self.filter_out_list = filter_out_list
        self.is_filter_out = True
        
    def setFilterInList(self, filter_in_list):
        self.filter_in_list = filter_in_list
        self.is_filter_out = False
        
