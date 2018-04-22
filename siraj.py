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

#from PyQt5.QtCore import (Qt, QModelIndex, QSortFilterProxyModel)
#from PyQt5.QtGui import (QCursor)
#from PyQt5.QtWidgets import (QMainWindow,QFileDialog, QApplication, QMenu, QAction, QMessageBox, QAbstractItemView, QLineEdit)

from subprocess import call
from sj_configs import LogSParserConfigs
from sj_table_model import MyTableModel
from sj_filter_proxy import MySortFilterProxyModel
from ui_siraj import Ui_Siraj
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

class LogSParserMain(QMainWindow):
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
        self.user_interface = Ui_Siraj()  
        self.user_interface.setupUi(self) 
        
        self.user_interface.mnuActionOpen.triggered.connect(self.menu_open_file)
        self.user_interface.mnuActionLoadConfigs.triggered.connect(self.menu_load_configs)
        self.user_interface.mnuActionExit.triggered.connect(self.menu_exit)
        self.user_interface.mnuActionAbout.triggered.connect(self.menu_about)
        self.user_interface.centralwidget.setLayout(self.user_interface.verticalLayout)
        self.user_interface.dckSourceContents.setLayout(self.user_interface.lytSource)
        self.user_interface.tblLogData.doubleClicked.connect(self.cell_double_clicked)
        self.user_interface.tblLogData.clicked.connect(self.cell_left_clicked)
        self.user_interface.tblLogData.keyPressEvent = self.cell_key_pressed
        self.user_interface.tblLogData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.user_interface.tblLogData.customContextMenuRequested.connect(self.cell_right_clicked)
        self.user_interface.txtSourceFile.setReadOnly(True)

        self.is_table_visible = True
        self.is_source_visible = True
        
        self.user_interface.tblLogData.resizeColumnsToContents() 
        self.user_interface.tblLogData.resizeRowsToContents() 
        
        self.setup_context_menu()
        self.setup_toolbars()
        
        self.clipboard = QApplication.clipboard()
        self.is_filtering_mode_out = True
        
        self.matched_row_list = []
        self.search_criteria_updated = True
        
        self.case_sensitive_search_type = Qt.CaseInsensitive
        self.is_wrap_search = True  
        self.is_match_whole_word = False

        self.graph_marker_list = []

        self.user_interface.tblLogData.setAcceptDrops(False)
        self.setAcceptDrops(True)

        self.load_configuration_file()

        self.toggle_source_view()

        self.select_cell_by_row_and_column(0, self.user_data_column_zero_based)
        
    def setup_toolbars(self):
        source_toolbar = self.addToolBar('SourceToolbar')
        
        self.user_interface.tbrActionToggleSourceView = QAction('C/C++', self)
        self.user_interface.tbrActionToggleSourceView.triggered.connect(self.toggle_source_view)
        self.user_interface.tbrActionToggleSourceView.setToolTip("Toggle source code view")
        self.user_interface.tbrActionToggleSourceView.setCheckable(True)
        self.user_interface.tbrActionToggleSourceView.setChecked(True)
        
        source_toolbar.addAction(self.user_interface.tbrActionToggleSourceView)
        
        search_toolbar = self.addToolBar("SearchToolbar")
        search_toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.ledSearchBox = QLineEdit()
        self.ledSearchBox.textChanged.connect(self.invalidate_search_criteria)
        self.ledSearchBox.keyPressEvent = self.search_box_key_pressed

        search_toolbar.addWidget(self.ledSearchBox)
        
        tbrActionPrevSearchMatch = QAction('<<', self)                               
        tbrActionPrevSearchMatch.triggered.connect(functools.partial(self.select_search_match, False))
        tbrActionPrevSearchMatch.setToolTip("Go to previous search match")                  

        tbrActionNextSearchMatch = QAction('>>', self)                               
        tbrActionNextSearchMatch.triggered.connect(functools.partial(self.select_search_match, True))             
        tbrActionNextSearchMatch.setToolTip("Go to next search match")                  

        tbrActionIgnoreCase = QAction('Ignore Case', self)                               
        tbrActionIgnoreCase.setCheckable(True)
        tbrActionIgnoreCase.setChecked(True)
        tbrActionIgnoreCase.triggered.connect(self.set_search_case_sensitivity, tbrActionIgnoreCase.isChecked())            
        tbrActionIgnoreCase.setToolTip("Ignore case") 
        
        tbrActionWrapSearch = QAction('Wrap Search', self)                               
        tbrActionWrapSearch.setCheckable(True)
        tbrActionWrapSearch.setChecked(True)
        tbrActionWrapSearch.triggered.connect(self.set_search_wrap, tbrActionWrapSearch.isChecked())             
        tbrActionWrapSearch.setToolTip("Wrap Search") 
        
        tbrActionMatchWholeWord = QAction('Match Whole Word', self)                               
        tbrActionMatchWholeWord.setCheckable(True)
        tbrActionMatchWholeWord.setChecked(False)
        tbrActionMatchWholeWord.triggered.connect(self.set_match_whole_word, tbrActionMatchWholeWord.isChecked())             
        tbrActionMatchWholeWord.setToolTip("Match Whole Word") 
                                               
        search_toolbar.addAction(tbrActionPrevSearchMatch)
        search_toolbar.addAction(tbrActionNextSearchMatch)
        search_toolbar.addAction(tbrActionIgnoreCase)
        search_toolbar.addAction(tbrActionMatchWholeWord)
        search_toolbar.addAction(tbrActionWrapSearch)

    def set_search_case_sensitivity(self, ignore_case):
        self.invalidate_search_criteria()
        if(ignore_case):
            self.case_sensitive_search_type = Qt.CaseInsensitive
        else:
            self.case_sensitive_search_type = Qt.CaseSensitive

    def set_search_wrap(self, wrap_search):
        self.invalidate_search_criteria()
        self.is_wrap_search = wrap_search
        
    def set_match_whole_word(self, match_whole_word):
        self.invalidate_search_criteria()
        self.is_match_whole_word = match_whole_word
  
    def invalidate_search_criteria(self):
        self.search_criteria_updated = True;
        self.matched_row_list.clear()
        
    def get_matched_row_list(self, key_column, search_criteria, case_sensitivity):
        search_proxy = QSortFilterProxyModel()
        search_proxy.setSourceModel(self.user_interface.tblLogData.model())
        search_proxy.setFilterCaseSensitivity(case_sensitivity)
        search_proxy.setFilterKeyColumn(key_column)
        if(self.is_match_whole_word):
            search_criteria = r"\b{}\b".format(search_criteria)
            
        search_proxy.setFilterRegExp(search_criteria)
        matched_row_list = []
        for proxy_row in range(search_proxy.rowCount()):
            match_index = search_proxy.mapToSource(search_proxy.index(proxy_row, key_column))
            matched_row_list.append(match_index.row())
        self.search_criteria_updated = False    
        return matched_row_list

    def select_search_match(self, is_forward):
        selected_indexes = self.get_selected_indexes()
        
        if(len(selected_indexes) == 0):
            self.display_message_box(
                "No selection", 
                "Please select a cell from the column you want to search", 
                QMessageBox.Warning)
        else:
            index = self.get_selected_indexes()[0]
            row = index.row()
            column = index.column()
            search_criteria = self.ledSearchBox.text()
            if(self.search_criteria_updated):
                self.matched_row_list = self.get_matched_row_list(column, search_criteria, self.case_sensitive_search_type)
            if(len(self.matched_row_list) > 0):    
                is_match_found = False
                if(is_forward):
                    matched_row_index = bisect_left(self.matched_row_list, row)
                    if((matched_row_index < len(self.matched_row_list) - 1)):
                        if(self.matched_row_list[matched_row_index] == row):
                            matched_row_index += 1
                        is_match_found = True
                    elif(self.is_wrap_search):
                        matched_row_index = 0
                        is_match_found = True
                else:
                    matched_row_index = bisect_right(self.matched_row_list, row)
                    if(matched_row_index > 0):
                        matched_row_index -= 1
                    if((matched_row_index > 0)):
                        if((self.matched_row_list[matched_row_index] == row)):
                            matched_row_index -= 1
                        is_match_found = True
                    elif(self.is_wrap_search):
                        matched_row_index = len(self.matched_row_list) - 1
                        is_match_found = True
                if(is_match_found):
                    self.select_cell_by_row_and_column(self.matched_row_list[matched_row_index], column)
            else:
                self.display_message_box(
                     "No match found", 
                     'Search pattern "{}" was not found in column "{}"'.format(search_criteria, self.header[column]), 
                     QMessageBox.Warning)

    def reset_per_config_file_data(self):
        self.graph_dict.clear()
        self.reset_per_log_file_data()
        self.table_data = None
        self.table_model = None
        self.proxy_model = None
        
    def load_configuration_file(self, config_file_path="siraj_configs.json"):
        self.reset_per_config_file_data()
        self.config = LogSParserConfigs(config_file_path)
        self.log_file_full_path = self.config.get_config_item("log_file_full_path")
        self.log_trace_regex_pattern = self.config.get_config_item("log_row_pattern")
        self.time_stamp_column = self.config.get_config_item("time_stamp_column_number_zero_based")
        self.user_data_column_zero_based = self.config.get_config_item("user_data_column_zero_based")

        self.external_editor_configs = self.config.get_config_item("external_editor_configs")
        
        cross_reference_configs = self.config.get_config_item("source_cross_reference_configs")
        
        self.file_column = cross_reference_configs["file_column_number_zero_based"]
        self.file_column_pattern = cross_reference_configs["file_column_pattern"]
        self.line_column = cross_reference_configs["line_column_number_zero_based"]
        self.line_column_pattern = cross_reference_configs["line_column_pattern"]
        
        self.graph_configs = self.config.get_config_item("graph_configs")

        self.root_source_path_prefix = cross_reference_configs["root_source_path_prefix"]
        self.syntax_highlighting_style = cross_reference_configs["pygments_syntax_highlighting_style"]
        
        self.table_conditional_formatting_config = self.config.get_config_item("table_conditional_formatting_configs")
        self.load_log_file(self.log_file_full_path)

        
    def load_graphs(self, graph_configs, table_data):
        
        pg.setConfigOption('background', QColor("white"))
        pg.setConfigOption('foreground', QColor("black"))
        pg.setConfigOptions(antialias=True)
        graphs = list(sorted(graph_configs.keys(), key=lambda k: graph_configs[k]["index"]))
        graph_data = [([],[],) for _ in graphs]

        self.graph_marker_list = []

        for row_number, row_data in enumerate(table_data):
            for graph_number, graph_name in enumerate(graphs):
                cell_to_match = row_data[graph_configs[graph_name]["column"]]
                m = re.search(graph_configs[graph_name]["pattern"], cell_to_match)
                if(m is not None):
                    graph_data[graph_number][0].append(row_number)          # X-Axis value
                    graph_data[graph_number][1].append(int(m.group(1)))     # Y-Axis value
            

        for graph in graphs:
            window = None
            wnd = graph_configs[graph]["window"]
            if (wnd in self.graph_dict):
                window = self.graph_dict[wnd]
                window.clear()

        is_new_window = False
        first_plot_name = None
        for graph_number, graph in enumerate(graphs):
            window = None
            wnd = graph_configs[graph]["window"]
            if (wnd in self.graph_dict):
                window = self.graph_dict[wnd]
                is_new_window = False
            else:
                is_new_window = True
                window = pg.GraphicsWindow(title=wnd)

                self.graph_dict[wnd] = window


            p = window.addPlot(name=graph, title=graph)

            p.plot(graph_data[graph_number][0],
                   graph_data[graph_number][1],
                   pen=pg.mkPen(width=1, color=QColor(graph_configs[graph]["color"])), symbol='d', symbolPen='w', symbolBrush=(0,0,0), name=graph)
            p.showGrid(x=True, y=True)
            if first_plot_name == None:
                first_plot_name = graph
            p.setXLink(first_plot_name)
            marker = pg.InfiniteLine(angle=90, movable=False)
            p.addItem(marker, ignoreBounds=True)
            self.graph_marker_list.append(marker)

            window.nextRow()

    def setup_context_menu(self):
        self.menuFilter = QMenu(self)
        
        self.hide_action                 = QAction('Hide selected values', self)
        self.show_only_action            = QAction('Show only selected values', self)
        self.clear_all_filters_action    = QAction('Clear all filters', self)
        self.copy_selection_action       = QAction('Copy selection', self)
       
        self.unhide_menu = QMenu('Unhide item from selected column', self.menuFilter)

        self.hide_action.triggered.connect(self.hide_rows_based_on_selected_cells)
        self.show_only_action.triggered.connect(self.show_rows_based_on_selected_cells)
        self.clear_all_filters_action.triggered.connect(self.clear_all_filters)
        self.copy_selection_action.triggered.connect(self.prepare_clipboard_text)
        
        self.menuFilter.addAction(self.hide_action)
        self.menuFilter.addMenu(self.unhide_menu)
        self.menuFilter.addAction(self.show_only_action)
        self.menuFilter.addAction(self.clear_all_filters_action)
        self.menuFilter.addSeparator()
        self.menuFilter.addAction(self.copy_selection_action)

        self.hide_action.setShortcut('Ctrl+H')
        self.show_only_action.setShortcut('Ctrl+O')
        self.clear_all_filters_action.setShortcut('Ctrl+Del')
        self.copy_selection_action.setShortcut("Ctrl+C")
        
    def toggle_source_view(self):
        self.is_source_visible = not self.is_source_visible
        self.user_interface.tbrActionToggleSourceView.setChecked(self.is_source_visible)

        self.user_interface.dckSource.setVisible(self.is_source_visible)
        logging.info("Source view is now {}".format("Visible" if self.is_source_visible else "Invisible"))

    def display_message_box(self, title, message, icon):
        """
        Show the about box.
        """   
        message_box = QMessageBox(self);
        message_box.setWindowTitle(title);
        message_box.setTextFormat(Qt.RichText);   
        message_box.setText(message)
        message_box.setIcon(icon)
        message_box.exec_()
                
    def menu_about(self):
        """
        Show the about box.
        """

        about_text = """
        
Copyright 2015 Mohamed Galal El-Din Ebrahim (<a href="mailto:mohamed.g.ebrahim@gmail.com">mohamed.g.ebrahim@gmail.com</a>)
<br>
<br>
siraj is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License.
<br>
<br>
siraj is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  See the GNU General Public License for more details.
<br>
<br>
You should have received a copy of the GNU General Public License along with 
siraj.  If not, see 
<a href="http://www.gnu.org/licenses">http://www.gnu.org/licenses</a>.
        
"""        
        self.display_message_box("About", about_text, QMessageBox.Information)
    
    def menu_exit(self):
        """
        Handles the exit menu clicked event.
        """
        exit(0)
        
    def menu_open_file(self):
        """
        Handles the open menu clicked event.
        """
        self.log_file_full_path = QFileDialog.getOpenFileName(
            self,
            'Open Log File',
            os.getcwd())
        if(self.log_file_full_path != ''):
            self.load_log_file(self.log_file_full_path)
        
    def menu_load_configs(self):
        """
        Loads a new configuration file.
        """
        self.config_file_full_path = QFileDialog.getOpenFileName(
            self,
            'Open Config File',
            os.getcwd())
        if(self.config_file_full_path != ''):
            self.load_configuration_file(self.config_file_full_path)
            
        
    def reset_per_log_file_data(self):
        self.invalidate_search_criteria()
        
    def load_log_file(self, log_file_full_path):
        """
        Loads the given log file into the table.
        """
        self.reset_per_log_file_data()
        if (log_file_full_path == ""):
            pass
        elif (os.path.isfile(log_file_full_path)):
            with open(log_file_full_path, "r") as log_file_handle:
                log_file_content_lines = log_file_handle.read().splitlines()
            
            pattern = re.compile(self.log_trace_regex_pattern)        
            
            self.table_data = []
            most_recent_valid_table_entry = []
            for line in log_file_content_lines:
                m = pattern.match(line)
                if(m is not None):
                    most_recent_valid_table_entry = [group.strip() for group in m.groups()]
                    self.table_data.append(list(most_recent_valid_table_entry))
                else:
                    if(self.user_data_column_zero_based != -1):
                        temp_list = list(most_recent_valid_table_entry)
                        temp_list[self.user_data_column_zero_based] = line
                        self.table_data.append(temp_list)                    
            
            m = re.search(self.log_trace_regex_pattern, log_file_content_lines[1])
            self.header = [group_name for group_name in sorted(m.groupdict().keys(), key=lambda k: m.start(k))]
            self.table_model = MyTableModel(self.table_data, self.header, self.table_conditional_formatting_config, self)
            logging.info("Headers: %s", self.header)
            logging.info("%s has %d lines", self.log_file_full_path, len(self.table_data))
            self.proxy_model = MySortFilterProxyModel(self)
            self.proxy_model.setSourceModel(self.table_model)
            self.user_interface.tblLogData.setModel(self.proxy_model)
            if(len(self.per_column_filter_out_set_list) == 0):
                self.per_column_filter_out_set_list = [set() for column in range(len(self.table_data[0]))]
            if(len(self.per_column_filter_in_set_list) == 0):
                self.per_column_filter_in_set_list = [set() for column in range(len(self.table_data[0]))]
            
            self.extract_column_dictionaries(self.header, self.table_data)
            self.load_graphs(self.graph_configs, self.table_data) 
            self.setWindowTitle("Siraj | {}".format(log_file_full_path))   
        else:
            self.display_message_box(
                "File not Found!", 
                "File <b>`{}`</b> was not found. You can either: <br><br>1. Open a log file via the File menu. Or<br>2. Drag a log file from the system and drop it into the application".format(log_file_full_path), 
                QMessageBox.Critical)

            
    def extract_column_dictionaries(self, header_vector_list, data_matrix_list):
        """
        This function extracts a dictionary of dictionaries
        
        The extracted is a dictionary of columns where key is the column name, 
        and the data is another dictionary.
        
        The inner dictionary has a key equal to a specific cell value of the 
        current column, and the value is a list of row number where this value
        appeared in.
        
        This will be used to provide quick navigation through the log.        
        """
        column_count = len(header_vector_list)
        self.columns_dict = {}
        for column, column_name in enumerate(header_vector_list):
            self.columns_dict[column] = {}
            
        for row, log in enumerate(data_matrix_list):
            for column, field in enumerate(log):
                if(log[column] not in self.columns_dict[column]):
                    self.columns_dict[column][log[column]] = []
                self.columns_dict[column][log[column]].append(row)
    
    def cell_left_clicked(self, index):
        """
        Handles the event of clicking on a table cell.
        
        If the clicked column was the the column that contain the source file:line
        information from the log, the function also populate the the EditView
        with the source file contents with a marker highlighting the line.
        
        This is only done if the source view is visible.
        """
        index = self.proxy_model.mapToSource(index)

        if(self.is_source_visible):
            logging.info("cell[%d][%d] = %s", index.row(), index.column(), index.data())
            row = index.row()
            
            file_matcher = re.search(self.file_column_pattern, self.table_data[row][self.file_column])
            line_matcher = re.search(self.line_column_pattern, self.table_data[row][self.line_column])
            
            if((file_matcher is not None) and (line_matcher is not None)):
                file = file_matcher.group(1)
                line = line_matcher.group(1)
                full_path = "{}{}".format(self.root_source_path_prefix, file.strip())
                self.load_source_file(full_path, line)
                self.user_interface.tblLogData.setFocus() 
        self.update_status_bar()
        self.update_graph_markers()


    def load_source_file(self, file, line):    
        code = open(file).read()
        lexer = get_lexer_for_filename(file)
        formatter = HtmlFormatter(
                                  linenos = True,
                                  full = True,
                                  style = self.syntax_highlighting_style,
                                  hl_lines = [line])
        result = highlight(code, lexer, formatter)
        self.user_interface.txtSourceFile.setHtml(result)
        
        text_block = self.user_interface.txtSourceFile.document().findBlockByLineNumber(int(line))      
        text_cursor = self.user_interface.txtSourceFile.textCursor()
        text_cursor.setPosition(text_block.position())        
        self.user_interface.txtSourceFile.setTextCursor(text_cursor)
        self.user_interface.txtSourceFile.ensureCursorVisible()

    def get_selected_indexes(self):
        """
        Returns a list of the currently selected indexes mapped to the source numbering.
        
        mapToSource is needed to retrive the actual row number regardless of whether filtering is applied or not.
        """
        return [self.proxy_model.mapToSource(index) for index in self.user_interface.tblLogData.selectedIndexes()]
                    
    def update_status_bar(self):
        """
        Updates the status bar with relevant information
        """
        selected_indexes = self.get_selected_indexes()
        
        if(len(selected_indexes) == 1):
            selected_cell_index = selected_indexes[0]
            number_of_occurances = len(self.columns_dict[selected_cell_index.column()][selected_cell_index.data()])
            self.user_interface.statusbar.showMessage(
                '["{}"] occurred {} time(s) ~ {}%'.format(
                selected_cell_index.data(), 
                number_of_occurances,
                number_of_occurances * 100 // len(self.table_data)))
        elif(len(selected_indexes) == 2):
            row_1 = selected_indexes[0].row()
            row_2 = selected_indexes[1].row()
            time_stamp1 = float(self.table_data[row_1][self.time_stamp_column])
            time_stamp2 = float(self.table_data[row_2][self.time_stamp_column])
            self.user_interface.statusbar.showMessage("Time difference = {}".format(abs(time_stamp2 - time_stamp1)))
        else:
            self.user_interface.statusbar.showMessage("")

    def cell_right_clicked(self, point):
        """
        Handle the event of right-clicking on a table cell.

        This function is responsible for showing the context menu for the user
        to choose from.
        """
        index = self.proxy_model.mapToSource(
            self.user_interface.tblLogData.indexAt(point))
        logging.debug("Cell[%d, %d] was right-clicked. Contents = %s", index.row(), index.column(), index.data())

        self.right_clicked_cell_index = index
        self.populate_unhide_context_menu(index.column())

        self.prepare_clipboard_text()
        
        self.menuFilter.popup(QCursor.pos())
        
    def populate_unhide_context_menu(self, column):    
        self.unhide_menu.clear()
        if(self.is_filtering_mode_out):
            filtered_out_set = self.per_column_filter_out_set_list[column]
        else:
            filtered_out_set = set(self.columns_dict[column].keys()) - self.per_column_filter_in_set_list[column]
        
        if(len(filtered_out_set) > 0):
            self.unhide_menu.setEnabled(True)
            for filtered_string in filtered_out_set:
                temp_action = QAction(filtered_string, self.unhide_menu)
                temp_action.triggered.connect(functools.partial(self.unhide_selected_rows_only_based_on_column, self.right_clicked_cell_index.column(), filtered_string))
                self.unhide_menu.addAction(temp_action)
        else:
            self.unhide_menu.setEnabled(False)
            

    def cell_double_clicked(self, index):
        """
        Handles the event of double-clicking on a table cell.
        
        If the double clicked cell was at the column of file:line, the function
        triggers external text editor (currently this is gedit on Linux) and make 
        it point on the corresponding line.
        """
        
        index = self.proxy_model.mapToSource(index)

        logging.info("cell[%d][%d] = %s", index.row(), index.column(), index.data())
        row = index.row()
        
        file_matcher = re.search(self.file_column_pattern, self.table_data[row][self.file_column])
        line_matcher = re.search(self.line_column_pattern, self.table_data[row][self.line_column])
        
        if((file_matcher is not None) and (line_matcher is not None)):
            file = file_matcher.group(1)
            line = line_matcher.group(1)
            full_path = "{}{}".format(self.root_source_path_prefix, file.strip())
            logging.info("Using external editor (gedit) to open %s at line %s", file, line)
            
            editor = self.external_editor_configs["editor"]
            editor_command_format = self.external_editor_configs["editor_command_format"]
            
            editor_command = editor_command_format.format(
                editor_executable=editor,
                line_number=line,
                file_name=full_path)
            
            call(editor_command,
                shell=True)
            self.user_interface.tblLogData.setFocus() 
        self.update_status_bar()

    def search_box_key_pressed(self, q_key_event):
        key = q_key_event.key()
        if (key in [Qt.Key_Enter, Qt.Key_Return]):
            if(Qt.ShiftModifier == (int(q_key_event.modifiers()) & (Qt.ShiftModifier))):
                self.select_search_match(False)
            else:
                self.select_search_match(True)
        else:
            QLineEdit.keyPressEvent(self.ledSearchBox, q_key_event)
                                        

    def cell_key_pressed(self, q_key_event):
        """
        Handles the event of pressing a keyboard key while on the table.
        """
        logging.warning("A key was pressed!!!")
        key = q_key_event.key()
        logging.info("Key = {}".format(key))

        if(Qt.ControlModifier == (int(q_key_event.modifiers()) & (Qt.ControlModifier))):
            if key == Qt.Key_Delete:
                logging.info("Delete key pressed while in the table. Clear all filters")
                self.clear_all_filters()
            elif key == Qt.Key_H:
                self.hide_rows_based_on_selected_cells()
            elif key == Qt.Key_O:
                self.show_rows_based_on_selected_cells()
            elif key == Qt.Key_Up: # Jump to previous match
                selected_indexes = self.get_selected_indexes()
                if(len(selected_indexes) == 1):
                    self.go_to_prev_match(selected_indexes[0])
            elif key == Qt.Key_Down: # Jump to next match
                selected_indexes = self.get_selected_indexes()
                if(len(selected_indexes) == 1):
                    self.go_to_next_match(selected_indexes[0])           
            elif key == Qt.Key_PageUp:
                selected_indexes = self.get_selected_indexes()
                if(len(selected_indexes) == 1):
                    prev_bookmark_index = self.table_model.getPrevBookmarkIndex(selected_indexes[0])
                    if(prev_bookmark_index is not None):
                        self.select_cell_by_index(prev_bookmark_index)
            elif key == Qt.Key_PageDown:
                selected_indexes = self.get_selected_indexes()
                if(len(selected_indexes) == 1):
                    next_bookmark_index = self.table_model.getNextBookmarkIndex(selected_indexes[0])
                    if(next_bookmark_index is not None):
                        self.select_cell_by_index(next_bookmark_index)
            elif key == Qt.Key_C:
                selected_indexes = self.get_selected_indexes()
                self.prepare_clipboard_text()
            elif key == Qt.Key_B:
                if(Qt.ShiftModifier == (int(q_key_event.modifiers()) & (Qt.ShiftModifier))):
                    self.table_model.clearAllBookmarks()
                else:
                    selected_indexes = self.get_selected_indexes()
                    self.table_model.toggleBookmarks(selected_indexes)
            elif key == Qt.Key_Left:
                self.select_search_match(is_forward=False)
            elif key == Qt.Key_Right:
                self.select_search_match(is_forward=True)
            elif key == Qt.Key_Home:
                self.select_cell_by_row_and_column(0, 0);
            elif key == Qt.Key_End:
                self.select_cell_by_row_and_column(self.table_model.rowCount(None) - 1, 0);               
        elif key == Qt.Key_F5:
            self.load_log_file(self.log_file_full_path)
        
        else:
            QTableView.keyPressEvent(self.user_interface.tblLogData, q_key_event)
        self.update_graph_markers()

    def update_graph_markers(self):
        selected_indexes = self.get_selected_indexes()
        if (len(selected_indexes) == 1):
            for marker in self.graph_marker_list:
                marker.setPos(selected_indexes[0].row())

    def prepare_clipboard_text(self):
        """
        Copy the cell content to the clipboard if a single cell is selected. Or
        Copy the whole rows if cells from multiple rows are selected.
        """
        selected_indexes = self.get_selected_indexes()
        if(len(selected_indexes) == 0):
            clipboard_text = ""
        elif(len(selected_indexes) == 1):
            clipboard_text = self.user_interface.tblLogData.currentIndex().data()
        else:
            unique_rows_set = set([index.row() for index in sorted(selected_indexes)])
            row_text_list = [str(row) + "," + ",".join([self.proxy_model.index(row, column, QModelIndex()).data() for column in range(self.proxy_model.columnCount())]) for row in sorted(unique_rows_set)]
            clipboard_text = "\n".join(row_text_list)
        self.clipboard.setText(clipboard_text)

    
    def get_index_by_row_and_column(self, row, column):
        """
        Get the table index value by the given row and column
        """
        index = self.table_model.createIndex(row, column)
        index = self.proxy_model.mapFromSource(index)
        return index
           
    def select_cell_by_row_and_column(self, row, column):
        """
        Select the cell identified by the given row and column and scroll the 
        table view to make that cell in the middle of the visible part of the
        table.
        """
        self.user_interface.tblLogData.clearSelection()
        index = self.get_index_by_row_and_column(row, column)
        self.user_interface.tblLogData.setCurrentIndex(index)  
        self.user_interface.tblLogData.scrollTo(index, hint = QAbstractItemView.PositionAtCenter)
        self.user_interface.tblLogData.setFocus()
        self.update_status_bar()
        
    def select_cell_by_index(self, index):        
        """
        Select a cell at the given index.
        """
        self.user_interface.tblLogData.clearSelection()
        index = self.proxy_model.mapFromSource(index)
        self.user_interface.tblLogData.setCurrentIndex(index)  
        self.user_interface.tblLogData.scrollTo(index, hint = QAbstractItemView.PositionAtCenter)
        self.user_interface.tblLogData.setFocus()
        self.update_status_bar()
        
    def go_to_prev_match(self, selected_cell):
        """
        Go to the prev cell that matches the currently selected cell in the 
        same column
        """
        matches_list = self.columns_dict[selected_cell.column()][selected_cell.data()]
        index = matches_list.index(selected_cell.row())
        if(index > 0):
            new_row = matches_list[index - 1]
            self.select_cell_by_row_and_column(new_row, selected_cell.column())
            
    def go_to_next_match(self, selected_cell):
        """
        Go to the prev cell that matches the currently selected cell in the 
        same column
        """
        matches_list = self.columns_dict[selected_cell.column()][selected_cell.data()]
        index = matches_list.index(selected_cell.row())
        if(index < (len(matches_list) - 1)):
            new_row = matches_list[index + 1]
            self.select_cell_by_row_and_column(new_row, selected_cell.column())
    
    
    def get_top_left_selected_row_index(self):
        """
        This function return the top-left selected index from the selected list.
        It's used for example to anchor the table view around the top-left 
        selected cell following any change in the visible cells due to filtering
        """
        top_left_index = None
        
        selected_indexes = self.get_selected_indexes()
        if(len(selected_indexes) > 0):
            selected_indexes = self.get_selected_indexes()
            
            top_left_index  = selected_indexes[0]
            row             = top_left_index.row()
            column          = top_left_index.column()
            for index in selected_indexes[1:]:
                if((index.row() < row) and (index.column() < column)):
                    row     = index.row()
                    column  = index.column()
                    top_left_index = index
        return top_left_index            
            
    def clear_all_filters(self):
        """
        Clears all the current filter and return the table to its initial view.
        """
        top_selected_index = self.get_top_left_selected_row_index()
        
        self.per_column_filter_out_set_list = [set() for column in range(len(self.table_data[0]))]
        self.per_column_filter_in_set_list = [set() for column in range(len(self.table_data[0]))]
        self.apply_filter(is_filtering_mode_out = True)
        
        if(top_selected_index != None):
            self.select_cell_by_index(top_selected_index)
      
        self.update_status_bar()   

        
    def hide_rows_based_on_selected_cells(self):
        """
        Hides the selected rows and any other rows with matching data.
        """
        selected_indexes = self.get_selected_indexes()
        for index in selected_indexes:
            column = index.column()
            self.per_column_filter_out_set_list[column].add(index.data())
        
        new_selected_row = None
        min_selected_row = selected_indexes[0].row()    
        max_selected_row = selected_indexes[-1].row()    
        if(min_selected_row != 0):
            new_selected_row = min_selected_row - 1
        elif(max_selected_row != self.table_model.columnCount(None)):
            new_selected_row = max_selected_row + 1
            
        self.apply_filter(is_filtering_mode_out=True)    
        
        self.select_cell_by_row_and_column(new_selected_row, selected_indexes[0].column())
        self.update_status_bar()   
            
    def show_rows_based_on_selected_cells(self):
        """
        Shows the selected rows and any other rows with matching data only.
        """
        
        selected_indexes = self.get_selected_indexes()
        self.per_column_filter_in_set_list = [set() for column in range(len(self.table_data[0]))]
        for index in selected_indexes:
            column = index.column()
            self.per_column_filter_in_set_list[column].add(index.data())
        self.apply_filter(is_filtering_mode_out=False)   
        self.update_status_bar()   

    def unhide_selected_rows_only_based_on_column(self, filter_column, filtered_out_string):
        """
        Unhides the selected rows and any other rows with matching data.
        
        The filtering works on one column only.
        """
        top_selected_index = self.get_top_left_selected_row_index()

        if(self.is_filtering_mode_out):
            self.per_column_filter_out_set_list[filter_column].remove(filtered_out_string)
        else:
            self.per_column_filter_in_set_list[filter_column].add(filtered_out_string)
            
        logging.debug("Unhiding: %s", filtered_out_string)
        self.apply_filter(self.is_filtering_mode_out)
        
        if(top_selected_index != None):
            self.select_cell_by_index(top_selected_index)
        
        self.update_status_bar()   
        
    def apply_filter(self, is_filtering_mode_out):    
        """
        Applies the filter based on the given mode. 
        """
        self.is_filtering_mode_out = is_filtering_mode_out
        if(is_filtering_mode_out):
            self.proxy_model.setFilterOutList(self.per_column_filter_out_set_list)
        else:
            self.proxy_model.setFilterInList(self.per_column_filter_in_set_list)
        
        # This is just to trigger the proxy model to apply the filter    
        self.proxy_model.setFilterKeyColumn(0)
    
    def dragEnterEvent(self, q_drag_enter_event):
        if(q_drag_enter_event.mimeData().hasFormat("text/uri-list")):
            q_drag_enter_event.acceptProposedAction();
    
    def dropEvent(self, q_drop_event):
        url_list = q_drop_event.mimeData().urls()
        if(len(url_list) == 0):
            return
        log_file_list = [url.toLocalFile() for url in url_list]
        self.log_file_full_path = log_file_list[0]
        self.load_log_file(self.log_file_full_path)
    
    def closeEvent(self, event):
        app = QApplication([])
#         app.closeAllWindows() 
        app.deleteLater()
        app.closeAllWindows()
                          
def main():
    logging.basicConfig(
        format='%(levelname)s||%(funcName)s||%(message)s||%(created)f||%(filename)s:%(lineno)s', 
        filename='siraj.log',
        filemode="w",
        level=logging.DEBUG,  
        datefmt='%d/%m/%y|%H:%M:%S')
#     logging.disable(CRITICAL)
    logging.debug('Entering...')
    APP = QApplication(sys.argv)
    MAIN = LogSParserMain()
    MAIN.showMaximized()
    logging.debug('Exiting...')
    sys.exit(APP.exec_())

if __name__ == "__main__":
    main()
