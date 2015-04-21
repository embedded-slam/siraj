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
import json
import logging

class LogSParserConfigs(object):
    """
    This class is responsible for saving and loading the application 
    configurations.
    
    Application configuration are stored in JSON format.
    """
    
    config_items = {}
    def __init__(self, config_file_path):
        self.load_configs(config_file_path)
        logging.info(config_file_path)
            
    def load_configs(self, config_file_path):
        """
        Loads the data from the given JSON file.
        
        Configuration items are stored in a dictionary to simplify 
        reading and writing.
        """
        logging.info("Loading configuration file...")
        self.config_items = json.load(open(config_file_path))
        
    def save_configs(self, config_file_path):
        """
        Saves the configuration currently sotred in the dictionary to a file.
        """
        logging.info("Saving configuration file...")
        json.dump(self.config_items, open(config_file_path, 'w'), indent=4, sort_keys=True)
        
    def set_config_item(self, item_name, item_value):
        """
        Writes the given value into the given configuration item key.
        """
        logging.info("Setting item ['{}'] value...".format(item_name))
        self.config_items[item_name] = item_value
        
    def get_config_item(self, item_name):
        """
        Reads the value of the given configuration key.
        """
        logging.info("Getting item ['{}'] value...".format(item_name))
        return self.config_items[item_name]
