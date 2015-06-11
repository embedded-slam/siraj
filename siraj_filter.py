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
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.graph_dict = {}
        self.menuFilter = None
        self.proxy_model = None
        self.table_data = None
        self.ui_filter = Ui_SirajFilter()  
        self.ui_filter.setupUi(self) 
        
    
        
        self.ui_filter.centralwidget.setLayout(self.ui_filter.verticalLayout)
        
        self.ui_filter.tblLogFilter.resizeColumnsToContents() 
        self.ui_filter.tblLogFilter.resizeRowsToContents() 
        
        self.clipboard = QApplication.clipboard()
        self.ui_filter.tblLogFilter.setAcceptDrops(True)
    
        