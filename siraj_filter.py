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

import logging

from PyQt4.QtCore import (Qt)

from siraj_base import SirajBase


class SirajFilter(SirajBase):
    """
    This is the main class in the application. It's responsible for displaying
    the log data in a tabular format as well as allowing the user to filter the
    logs displayed.
    """
    per_column_filter_out_set_list = list()
    per_column_filter_in_set_list = list()
    header = list()
    # table_conditional_formatting_config = None
    def __init__(self, table_model, columns_dict):
        SirajBase.__init__(self)
        SirajBase.set_table_model(self, table_model)
        SirajBase.set_columns_dict(self, columns_dict)
        
        # self.graph_dict = {}
        # self.menuFilter = None
        # self.table_proxy = None
        # self.table_data = None
        # self.user_interface = Ui_SirajFilter()  
        # self.user_interface.setupUi(self) 
        # self.table_model = table_model
        # 
        # self.table_proxy = MySortFilterProxyModel(self)
        # self.table_proxy.setSourceModel(self.table_model)
        # self.user_interface.tblLogData.setModel(self.table_proxy)
        # 
        # # Initially the filter in list is empty
        # self.per_column_filter_in_set_list = [set() for column in range(self.table_model.columnCount(None))]
        # 
#         [self.per_column_filter_in_set_list[column].add("Impossible to exist value!") for column in range(self.table_model.columnCount(None))]
        
        self.table_proxy.setFilterInList(self.per_column_filter_in_set_list)
        self.table_proxy.invalidate()

        self.user_interface.centralwidget.setLayout(self.user_interface.verticalLayout)
        
        # self.user_interface.tblLogData.resizeColumnsToContents()
        # self.user_interface.tblLogData.resizeRowsToContents()
        #
        # self.clipboard = QApplication.clipboard()
        # self.user_interface.tblLogData.setAcceptDrops(True)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.user_interface.tblLogData.keyPressEvent = self.cell_key_pressed
        """
        @todo This is a hack to disable the menu bar in the filter menu. The proper way is to remove the menu bar from
        the SirajBase Class altogether and add it where it belongs (in Siraj class which has the main window).
        """

        self.setMenuBar(None)

    
    def add_to_filter_view(self, column, data):
        """
        Add the given cell index to the filtered view.
        """

        self.per_column_filter_in_set_list[column].add(data)
        self.table_proxy.setFilterInList(self.per_column_filter_in_set_list)
        self.table_proxy.invalidate()    
        
    def remove_from_filter_view(self, column, data):
        """
        Add the given cell index to the filtered view.
        """

        self.per_column_filter_in_set_list[column].remove(data)
        self.table_proxy.setFilterInList(self.per_column_filter_in_set_list)
        self.table_proxy.invalidate()

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
                SirajBase.cell_key_pressed(self, q_key_event)
        else:
            SirajBase.cell_key_pressed(self, q_key_event)