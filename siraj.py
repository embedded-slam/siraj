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
from PyQt4.QtGui import (QMainWindow, QFileDialog, QApplication, 
QSortFilterProxyModel, QTextCursor, QTextCharFormat, QBrush, QColor, QMenu, 
QAction, QCursor, QMessageBox, QItemSelectionModel, QAbstractItemView, QTableView, QLineEdit)
from subprocess import call
from sj_configs import LogSParserConfigs
from sj_table_model import MyTableModel
from sj_filter_proxy import MySortFilterProxyModel
from ui_siraj import Ui_Siraj  # import generated interface
import logging
from logging import CRITICAL
from functools import partial
import functools
import json
# from sj_syntax_highlight import PythonHighlighter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pip.util import file_contents
from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename)
from bisect import (bisect_left, bisect_right)

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
        self.load_configuration_file()

        
        self.is_table_visible = True
        self.is_source_visible = True
        
        self.user_interface.tblLogData.resizeColumnsToContents() 
        self.user_interface.tblLogData.resizeRowsToContents() 
        
        self.setup_context_menu()
        self.setup_toolbar()
        
        self.clipboard = QApplication.clipboard()
        self.is_filtering_mode_out = True
        
        self.matched_row_list = None
        self.search_criteria_updated = True

    def setup_toolbar(self):
        source_toolbar = self.addToolBar('SourceToolbar')
        
        tbrActionToggleSourceView = QAction('C/C++', self)
        tbrActionToggleSourceView.triggered.connect(self.toggle_source_view)
        tbrActionToggleSourceView.setToolTip("Toggle source code view")
        tbrActionToggleSourceView.setCheckable(True)
        tbrActionToggleSourceView.setChecked(True)
        
        source_toolbar.addAction(tbrActionToggleSourceView)
        
        search_toolbar = self.addToolBar("SearchToolbar")
        search_toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.ledSearchBox = QLineEdit()
        self.ledSearchBox.textChanged.connect(self.invalidate_search_criteria)
        self.user_interface.mnuActionOpen.triggered.connect(self.menu_open_file)
        search_toolbar.addWidget(self.ledSearchBox)
        
        tbrActionPrevSearchMatch = QAction('<<', self)                               
        tbrActionPrevSearchMatch.triggered.connect(functools.partial(self.select_search_match, self.ledSearchBox.text, False))
        tbrActionPrevSearchMatch.setToolTip("Go to previous search match")                  

        tbrActionNextSearchMatch = QAction('>>', self)                               
        tbrActionNextSearchMatch.triggered.connect(functools.partial(self.select_search_match, self.ledSearchBox.text, True))             
        tbrActionNextSearchMatch.setToolTip("Go to next search match")                  
                                       
        search_toolbar.addAction(tbrActionPrevSearchMatch)
        search_toolbar.addAction(tbrActionNextSearchMatch)

    def invalidate_search_criteria(self):
        self.search_criteria_updated = True;
        
    def get_matched_row_list(self, key_column, search_criteria):
        search_proxy = QSortFilterProxyModel()
        search_proxy.setSourceModel(self.user_interface.tblLogData.model())
        search_proxy.setFilterKeyColumn(key_column)
        search_proxy.setFilterRegExp(search_criteria)
        matched_row_list = []
        for proxy_row in range(search_proxy.rowCount()):
            match_index = search_proxy.mapToSource(search_proxy.index(proxy_row, key_column))
            matched_row_list.append(match_index.row())
        return matched_row_list

    def select_search_match(self, get_search_criteria_callback, is_forward):
        index = self.get_selected_indexes()[0]
        row = index.row()
        column = index.column()
        if(self.search_criteria_updated):
            self.matched_row_list = self.get_matched_row_list(column, get_search_criteria_callback())
            self.search_criteria_updated = False
            
        if(is_forward):
            matched_row_index = bisect_left(self.matched_row_list, row)
            if((self.matched_row_list[matched_row_index] == row) and (matched_row_index < len(self.matched_row_list) - 1)):
                matched_row_index += 1
        else:
            matched_row_index = bisect_right(self.matched_row_list, row)
            if(matched_row_index > 0):
                matched_row_index -= 1
            if((self.matched_row_list[matched_row_index] == row) and (matched_row_index > 0)):
                matched_row_index -= 1
                    
        self.select_cell_by_row_and_column(self.matched_row_list[matched_row_index], column)
        
    def load_configuration_file(self, config_file_path="siraj_configs.json"):
        self.config = LogSParserConfigs(config_file_path)
        self.log_trace_regex_pattern = self.config.get_config_item("log_row_pattern")
        self.log_file_full_path = self.config.get_config_item("log_file_full_path")
        self.file_line_column = self.config.get_config_item("file_line_column_number_zero_based")
        self.root_prefix = self.config.get_config_item("root_source_path_prefix")
        self.time_stamp_column = self.config.get_config_item("time_stamp_column_number_zero_based")
        self.table_conditional_formatting_config = self.config.get_config_item("table_conditional_formatting_config")
        self.syntax_highlighting_style = self.config.get_config_item("pygments_syntax_highlighting_style")
        self.load_log_file(self.log_file_full_path)
        
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
        self.user_interface.dckSource.setVisible(self.is_source_visible)
        logging.info("Source view is now {}".format("Visible" if self.is_source_visible else "Invisible"))

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
        message_box = QMessageBox(self);
        message_box.setWindowTitle("About");
        message_box.setTextFormat(Qt.RichText);   
        message_box.setText(about_text)
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()
    
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
            
        
    def load_log_file(self, log_file_full_path):
        """
        Loads the given log file into the table.
        """

        with open(log_file_full_path, "r") as log_file_handle:
            log_file_content_lines = log_file_handle.read().splitlines()
        
        pattern = re.compile(self.log_trace_regex_pattern)        
#         self.table_data = [list(re.match(self.log_trace_regex_pattern, line).groups()) for line in log_file_content_lines if(pattern.match(line) is not None)]
        
        self.table_data = []
        for line in log_file_content_lines:
            m = pattern.match(line)
            if(m is not None):
                self.table_data.append([group.strip() for group in m.groups()])
        
        m = re.match(self.log_trace_regex_pattern, log_file_content_lines[1])
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
#             self.user_interface.txtSourceFile.setTextCursor(QTextCursor())
            logging.info("cell[%d][%d] = %s", index.row(), index.column(), index.data())
            self.left_clicked_cell_index = index
    
            if(index.column() == self.file_line_column):
#                 highlight = PythonHighlighter(self.user_interface.txtSourceFile.document())
                [file, line] = index.data().split(":")
                full_path = "{}{}".format(self.root_prefix, file.strip())
                self.load_source_file(full_path, line)
                self.user_interface.tblLogData.setFocus() 
        self.update_status_bar()
        
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
        Updates the status bar with relevant informations
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
                temp_action = QAction(filtered_string, self.unhide_menu);
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
        if(index.column() == self.file_line_column):
            [file, line] = index.data().split(":")
            logging.info("Using external editor (gedit) to open %s at line %s", file, line)
            call("gedit +{} {}{}".format(
                line,
                self.root_prefix,
                file.strip()),
                shell=True)

    def cell_key_pressed(self, q_key_event):
        """
        Handles the event of pressing a keyboard key while on the table.
        """
        logging.warning("A key was pressed!!!")
        key = q_key_event.key()
        logging.info("Key = {}".format(key))

        if(int(q_key_event.modifiers()) == (Qt.ControlModifier)):
            if key == Qt.Key_Delete:
                logging.info("Delete key pressed while in the table. Clear all filters")
                self.clear_all_filters()
            elif key == Qt.Key_H:
                self.hide_rows_based_on_selected_cells()
            elif key == Qt.Key_O:
                self.show_rows_based_on_selected_cells()
            elif key == Qt.Key_N:
                selected_indexes = self.get_selected_indexes()
                if(len(selected_indexes) == 1):
                    self.go_to_next_match(selected_indexes[0])        
            elif key == Qt.Key_P:
                selected_indexes = self.get_selected_indexes()
                if(len(selected_indexes) == 1):
                    self.go_to_prev_match(selected_indexes[0])
            elif key == Qt.Key_C:
                    selected_indexes = self.get_selected_indexes()
                    self.prepare_clipboard_text()
        else:
            QTableView.keyPressEvent(self.user_interface.tblLogData, q_key_event)
            
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
        index = self.get_index_by_row_and_column(row, column)
        self.user_interface.tblLogData.setCurrentIndex(index)  
        self.user_interface.tblLogData.scrollTo(index, hint = QAbstractItemView.PositionAtCenter)
        self.update_status_bar()
        
    def select_cell_by_index(self, index):        
        """
        Select a cell at the given index.
        """
        index = self.proxy_model.mapFromSource(index)
        self.user_interface.tblLogData.setCurrentIndex(index)  
        self.user_interface.tblLogData.scrollTo(index, hint = QAbstractItemView.PositionAtCenter)
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
            self.user_interface.tblLogData.clearSelection()
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
            self.user_interface.tblLogData.clearSelection()
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
#         top_selected_index = self.get_top_left_selected_row_index()

        selected_indexes = self.get_selected_indexes()
        for index in selected_indexes:
            column = index.column()
            self.per_column_filter_out_set_list[column].add(index.data())
        self.apply_filter(is_filtering_mode_out=True)    
        
#         if(top_selected_index != None):
#             self.select_cell_by_row_and_column(max(0, top_selected_index.row() - 1), top_selected_index.column())

        self.update_status_bar()   
            
    def show_rows_based_on_selected_cells(self):
        """
        Shows the selected rows and any other rows with matching data only.
        """
        
#         top_selected_index = self.get_top_left_selected_row_index()

        selected_indexes = self.get_selected_indexes()
        self.per_column_filter_in_set_list = [set() for column in range(len(self.table_data[0]))]
        for index in selected_indexes:
            column = index.column()
            self.per_column_filter_in_set_list[column].add(index.data())
        self.apply_filter(is_filtering_mode_out=False)   
        
#         if(top_selected_index != None):
#             self.select_cell_by_index(top_selected_index) 
            
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
