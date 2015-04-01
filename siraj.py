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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QMainWindow, QFileDialog, QApplication, 
QSortFilterProxyModel, QTextCursor, QTextCharFormat, QBrush, QColor, QMenu, 
QAction, QCursor, QMessageBox)
from subprocess import call
from sj_configs import LogSParserConfigs
from sj_table_model import MyTableModel
from ui_siraj import Ui_Siraj  # import generated interface
import logging
from logging import CRITICAL


class LogSParserMain(QMainWindow):
    """
    This is the main class in the application. It's responsible for displaying
    the log data in a tabular format as well as allowing the user to filter the
    logs displayed.
    """
    items_to_hide_per_column = list()
    header = list()
    def __init__(self):
        QMainWindow.__init__(self)
        self.context_menu = None
        self.proxy_model = None
        self.table_data = None
        self.user_interface = Ui_Siraj()  
        self.user_interface.setupUi(self) 
        self.user_interface.mnuActionOpen.activated.connect(self.menu_open_file)
        self.user_interface.mnuActionExit.activated.connect(self.menu_exit)
        self.user_interface.mnuActionAbout.activated.connect(self.menu_about)
        self.user_interface.centralwidget.setLayout(self.user_interface.verticalLayout)
        self.user_interface.tblLogData.doubleClicked.connect(self.cell_double_clicked)
        self.user_interface.tblLogData.clicked.connect(self.cell_left_clicked)
        self.user_interface.tblLogData.keyPressEvent = self.cell_key_pressed
        self.user_interface.tblLogData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.user_interface.tblLogData.customContextMenuRequested.connect(self.cell_right_clicked)
        self.user_interface.txtSourceFile.setReadOnly(True)
        self.config = LogSParserConfigs("siraj_configs.json")
        self.log_trace_regex_pattern = self.config.get_config_item("log_row_pattern")
        self.full_path = self.config.get_config_item("log_file_full_path")
        self.load_log_file()
        self.file_line_column = self.config.get_config_item("file_line_column_number_zero_based")
        self.root_prefix = self.config.get_config_item("root_source_path_prefix")

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
        message_box.exec()
    
    def menu_exit(self):
        """
        Handles the exit menu clicked event.
        """
        exit(0)
        
    def menu_open_file(self):
        """
        Handles the open menu clicked event.
        """
        self.full_path = ""
        self.load_log_file()
        
    def load_log_file(self):
        """
        Loads the given log file into the table.
        
        If no file was specified, the function triggers the open file dialog, so
        that the user can select a log file to load.
        """
        if self.full_path == "":
            self.full_path = QFileDialog.getOpenFileName(
                self,
                'Open file',
                os.getcwd())
        with open(self.full_path, "r") as log_file_handle:
            log_file_content_lines = log_file_handle.read().splitlines()
        self.table_data = [list(re.match(self.log_trace_regex_pattern, line).groups()) for line in log_file_content_lines if(re.match(self.log_trace_regex_pattern, line) is not None)]
        m = re.match(self.log_trace_regex_pattern, log_file_content_lines[1])
        self.header = [group_name for group_name in sorted(m.groupdict().keys(), key=m.span)]
        table_model = MyTableModel(self.table_data, self.header, self)
        logging.info("Headers: %s", self.header)
        logging.info("%s has %d lines", self.full_path, len(self.table_data))
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(table_model)
        self.user_interface.tblLogData.setModel(self.proxy_model)
        if(len(self.items_to_hide_per_column) == 0):
            self.items_to_hide_per_column = [[] for column in range(len(self.table_data[0]))]
            
    def cell_left_clicked(self, index):
        """
        Handles the event of clicking on a table cell.
        
        If the clicked column was the the column that contain the source file:line
        information from the log, the function also populate the the EditView
        with the source file contents with a marker highlighting the line.
        """
        self.user_interface.txtSourceFile.setTextCursor(QTextCursor())
        logging.info("cell[%d][%d] = %s", index.row(), index.column(), index.data())
        self.left_clicked_cell_index = index

        if(index.column() == self.file_line_column):
            [file, line] = index.data().split(":")
            full_path = "{}{}".format(self.root_prefix, file.strip())
            self.user_interface.lblSourceFileName.setText(full_path)
            file_contents = "\n".join(["{0:4d}: {1:s}".format(i + 1, line) for(i, line) in enumerate(open(full_path).read().splitlines())])
            self.user_interface.txtSourceFile.setText(file_contents)
            line_number = int(line) - 1
            logging.debug("file:line is %s:%s", file, line)
            text_block = self.user_interface.txtSourceFile.document().findBlockByLineNumber(line_number)
            text_cursor = self.user_interface.txtSourceFile.textCursor()
            text_cursor.setPosition(text_block.position())
            self.user_interface.txtSourceFile.setFocus()
            text_format = QTextCharFormat()
            text_format.setBackground(QBrush(QColor("yellow")))
            text_cursor.movePosition(QTextCursor.EndOfLine, 1)
            text_cursor.mergeCharFormat(text_format)
            self.user_interface.txtSourceFile.setTextCursor(text_cursor)
                        
    def cell_right_clicked(self, point):
        """
        Handle the event of right-clicking on a table cell.
        
        This function is responsible for showing the context menu for the user
        to choose from.
        """
        index = self.proxy_model.mapToSource(
            self.user_interface.tblLogData.indexAt(point))
        row = index.row()
        column = index.column()
        cell_text = self.table_data[row][column].strip()
        logging.debug("Cell[%d, %d] was right-clicked. Contents = %s", row, column, index.data())
        self.context_menu = QMenu(self)
        
        hide_action = QAction('Hide selected values from column "{}"'.format(self.header[column]), self)
        show_only_action = QAction('Show only selected values from column "{}"'.format(self.header[column]), self)
        clear_all_filters_action = QAction('Clear all filters'.format(self.header[column]), self)
        
        hide_action.triggered.connect(self.context_menu_hide_selected_rows)
        show_only_action.triggered.connect(self.context_menu_show_selected_rows_only)
        clear_all_filters_action.triggered.connect(self.clear_all_filters)
        
        self.context_menu.addAction(hide_action)
        self.context_menu.addAction(show_only_action)
        self.context_menu.addAction(clear_all_filters_action)
        self.context_menu.popup(QCursor.pos())
        
        self.right_clicked_cell_index = index

    def cell_double_clicked(self, index):
        """
        Handles the event of double-clicking on a table cell.
        
        If the double clicked cell was at the column of file:line, the function
        triggers external text editor (currently this is gedit on linux) and make 
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
        key = q_key_event.key()

        if key == Qt.Key_Delete:
            logging.info("Delete key pressed while in the table. Clear all filters")
            self.clear_all_filters()
        elif key == Qt.Key_H:
            self.hide_selected_rows_based_on_column(self.left_clicked_cell_index.column())
        elif key == Qt.Key_O:
            self.show_selected_rows_only_based_on_column(self.left_clicked_cell_index.column())

    def clear_all_filters(self):
        """
        Clears all the current filter and return the table to its initial view.
        """
        self.proxy_model.setFilterFixedString("")
        self.items_to_hide_per_column = [[] for column in range(len(self.table_data[0]))]
        
    def context_menu_hide_selected_rows(self):
        """
        Handles the context menu clicked event to hide selected rows.
        
        The filtering works on one column only. That column is the one which
        was right-clicked to show the context menu.
        """
        self.hide_selected_rows_based_on_column(self.right_clicked_cell_index.column())
            
    def context_menu_show_selected_rows_only(self):
        """
        Handles the context menu clicked event to show only selected rows. 
                
        The filtering works on one column only. That column is the one which
        was right-clicked to show the context menu.
        """
        self.show_selected_rows_only_based_on_column(self.right_clicked_cell_index.column())
    
    def hide_selected_rows_based_on_column(self, column):
        """
        Hides the selected rows and any other rows with matching data.
        
        The filtering works on one column only. That column is the one which
        was right-clicked to show the context menu.
        """
        selected_indexes = [self.proxy_model.mapToSource(index) for index in self.user_interface.tblLogData.selectedIndexes()]
        filter_column = column
        unique_items_to_hide_list = list(set([index.data() for index in selected_indexes if index.column() == column]))
        self.items_to_hide_per_column[column].extend(unique_items_to_hide_list)
        logging.debug("filtering: %s", self.items_to_hide_per_column[filter_column])
        regex_pattern_to_hide =  r"|".join([r"({})".format(re.escape(item)) for item in self.items_to_hide_per_column[filter_column]])    
        regex_pattern_to_hide = r"^(?!{})".format(regex_pattern_to_hide)
        logging.debug("Regex pattern to hide: %s", regex_pattern_to_hide)
        self.proxy_model.setFilterKeyColumn(filter_column)
        self.proxy_model.setFilterRegExp(regex_pattern_to_hide)        
            
    def show_selected_rows_only_based_on_column(self, column):
        """
        Shows the selected rows and any other rows with matching data only.
        
        The filtering works on one column only. That column is the one which
        was right-clicked to show the context menu.
        """
        selected_indexes = [self.proxy_model.mapToSource(index) for index in self.user_interface.tblLogData.selectedIndexes()]
        filter_column = column
        unique_items_to_show_list = list(set([index.data() for index in selected_indexes if index.column() == filter_column]))
        logging.debug("Showing the following from column %s: %s", self.header[filter_column], unique_items_to_show_list)
        regex_pattern_to_show = r"|".join([r"({})".format(re.escape(item)) for item in unique_items_to_show_list])    
        logging.debug("Regex pattern to show: '%s'", regex_pattern_to_show)
        self.proxy_model.setFilterKeyColumn(filter_column)
        self.proxy_model.setFilterRegExp(regex_pattern_to_show)


def main():
    logging.basicConfig(
        format='%(levelname)s|%(funcName)s|%(message)s|%(created)f|%(filename)s:%(lineno)s', 
        filename='siraj.log',
        mode="w",
        level=logging.DEBUG,  
        datefmt='%d/%m/%y|%H:%M:%S')
#     logging.disable(CRITICAL)
    logging.debug('Entering...')
    APP = QApplication(sys.argv)
    MAIN = LogSParserMain()
    MAIN.show()
    logging.debug('Exiting...')
    sys.exit(APP.exec_())

if __name__ == "__main__":
    main()