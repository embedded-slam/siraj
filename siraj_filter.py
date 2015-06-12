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

import re
import os
import sys
from PyQt4.QtCore import (Qt, QModelIndex)
from PyQt4.QtGui import (qApp, QMainWindow, QFileDialog, QApplication, 
QSortFilterProxyModel, QTextCursor, QTextCharFormat, QBrush, QColor, QMenu, 
QAction, QCursor, QMessageBox, QItemSelectionModel, QAbstractItemView, QTableView, QLineEdit)
from subprocess import call
from sj_configs import LogSParserConfigs
from sj_table_model import MyTableModel
from sj_filter_proxy import MySortFilterProxyModel
from ui_siraj_filter import Ui_SirajFilter
import logging
from logging import CRITICAL
from functools import partial
import functools
import json
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename)
from bisect import (bisect_left, bisect_right)
import pyqtgraph as pg

class SirajFilter(QMainWindow):
    """
    This is the main class in the application. It's responsible for displaying
    the log data in a tabular format as well as allowing the user to filter the
    logs displayed.
    """
    per_column_filter_out_set_list = list()
    per_column_filter_in_set_list = list()
    header = list()
    table_conditional_formatting_config = None
    def __init__(self, table_model):
        QMainWindow.__init__(self)
        
        self.graph_dict = {}
        self.menuFilter = None
        self.proxy_model = None
        self.table_data = None
        self.ui_filter = Ui_SirajFilter()  
        self.ui_filter.setupUi(self) 
        self.table_model = table_model
        
        self.filter_proxy_model = MySortFilterProxyModel(self)
        self.filter_proxy_model.setSourceModel(self.table_model)
        self.ui_filter.tblLogFilter.setModel(self.filter_proxy_model)
        
        # Initially the filter in list is empty
        self.per_column_filter_in_set_list = [set() for column in range(self.table_model.columnCount(None))]
        
#         [self.per_column_filter_in_set_list[column].add("Impossible to exist value!") for column in range(self.table_model.columnCount(None))]
        
        self.filter_proxy_model.setFilterInList(self.per_column_filter_in_set_list)
        self.filter_proxy_model.invalidate()
    
        
        self.ui_filter.centralwidget.setLayout(self.ui_filter.verticalLayout)
        
        self.ui_filter.tblLogFilter.resizeColumnsToContents() 
        self.ui_filter.tblLogFilter.resizeRowsToContents() 
        
        self.clipboard = QApplication.clipboard()
        self.ui_filter.tblLogFilter.setAcceptDrops(True)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.ui_filter.tblLogFilter.keyPressEvent = self.cell_key_pressed

    
    def add_to_filter_view(self, column, data):
        """
        Add the given cell index to the filtered view.
        """

        self.per_column_filter_in_set_list[column].add(data)
        self.filter_proxy_model.setFilterInList(self.per_column_filter_in_set_list)
        self.filter_proxy_model.invalidate()    
        
    def remove_from_filter_view(self, column, data):
        """
        Add the given cell index to the filtered view.
        """

        self.per_column_filter_in_set_list[column].remove(data)
        self.filter_proxy_model.setFilterInList(self.per_column_filter_in_set_list)
        self.filter_proxy_model.invalidate()

    def on_close(self):
        """ 
        Send a signal so that main view can cleanup the reference. 
        """
        print("HHHHHHHHHHHH")
        self.close_signal.emit()
        
        
        
    def cell_key_pressed(self, q_key_event):
        """
        Handles the event of pressing a keyboard key while on the table.
        """
        logging.warning("A key was pressed!!!")
        key = q_key_event.key()
        logging.info("Key = {}".format(key))

        if(Qt.ControlModifier == (int(q_key_event.modifiers()) & (Qt.ControlModifier))):
            if key == Qt.Key_U: # Unfilter the selected cell
                selected_indexes = self.get_selected_indexes()
                if(len(selected_indexes) == 1):
                    self.remove_from_filter_view(selected_indexes[0].column(), selected_indexes[0].data())
        else:
            QTableView.keyPressEvent(self.ui_main.tblLogData, q_key_event)
            
            
    """
    @TODO: Extract all generic function form siraj.py into a common module. 
    """    
    def get_selected_indexes(self):
        """
        Returns a list of the currently selected indexes mapped to the source numbering.
        
        mapToSource is needed to retrive the actual row number regardless of whether filtering is applied or not.
        """
        return [self.filter_proxy_model.mapToSource(index) for index in self.ui_filter.tblLogFilter.selectedIndexes()]
                    