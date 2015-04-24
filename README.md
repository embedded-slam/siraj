*Siraj* is a cross-platform textual log parser that was built using Python3 and Qt  
![](https://raw.githubusercontent.com/embedded-slam/siraj/master/siraj_screenshot.png)


# Problem
Textual logs can sometimes be huge. And going through them with standard text 
editor without color coding or filtering can be really frustrating job.

# Solution
*Siraj*  aims to facilitate textual logs analysis by presenting the textual
log in a user-friendly tabular format, it also allows the user to show/hide rows 
based on their contents. As well as linking each log trace with the source line
that generated it to give context while analyzing the log.

------------------------------------------------------------

# Quick Feature List
1.  Parsing any textual log and present matched fields as a **tabular format**.
2.  Matching logs is based on **Regular Expressions** for maximum flexibility.
3.  **Conditionally formatting** the table cells foreground/background colors based on the contents.
4.	**Hiding** one or more rows based on the contents.
5.	**Showing** only specific rows and hiding everything else.
6.  **Cross-referencing the source code** file/line that generated the log if applicable.
7.	Calculating the **time difference** between any two rows in the table if applicable.
8.  **Cross-platform**, Works on Linux, Windows, and Mac (not tested on Mac yet but it should work).
9.  **Light-weight**, It relies on the Qt (written in C++) to do the heavy-lifting.


------------------------------------------------------------

# Running Siraj
## From Source (Preferred)

Before you use *Siraj* you'll need to install and configure the following based
on your target system:

1.  [Python3](https://www.python.org/downloads/). 
2.  [SIP](http://www.riverbankcomputing.com/software/sip/download).
3.  [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download).

Once you have the prerequisites you can run the tool using it's main module as
follows:

`python siraj.py` 

## From Binaries
If you only need to use the tool and don't have/need python or Qt, you can 
download one of the following archives based on your system. 
                 
1.	[Linux.]  	(https://github.com/embedded-slam/siraj/raw/release/release/linux/siraj_linux.tar.gz)
2. 	[Windows.]	(https://github.com/embedded-slam/siraj/raw/release/release/windows/siraj_windows.zip) 
3.	Mac.  _Comming soon!_  

Once downloaded, you'll need to extract it and run *sirag*. This will run with 
the provided sample log `sample.log` and the provided sample configuration 
`siraj_configs.json`. You can then fine tune the configuration and load the 
log of your choice.

Note:
Linux and Windows binaries were created using [cx_freeze](http://cx-freeze.sourceforge.net/ "cx_freeze") 

------------------------------------------------------------

# Using Siraj
## Configuration
Siraj relies on a configuration file called siraj_configs.json which looks as shown below, You'll need to modify this file to suite your needs.

Since JSON doesn't allow inline comments, the different configuration items are described below:

------------------------------------------------------------
	{
		"log_file_full_path": "sample.log", 
		"file_line_column_number_zero_based": 4,
		"log_row_pattern" : "^(?P<LEVEL>[^|]+)\\|(?P<FUNCTION>[^|]+)\\|(?P<MESSAGE>[^|]+)\\|(?P<TIME>[^|]+)\\|(?P<FILE_AND_LINE>[^|]+)$",
		"root_source_path_prefix" : "",
		"time_stamp_column_number_zero_based": 3,
		"table_conditional_formatting_config" : 
		{
			"foreground_key_column" : 0,
			"foreground_color_dict" : 
			{
				"DEBUG" 	: "green",
				"INFO" 		: "blue",
				"WARNING" 	: "white"
			},
			"background_key_column" : 0,
			"background_color_dict" : 
			{
			    "WARNING" 	: "red"
			},		
			"special_formatting_key_column" : 1,
			"special_formatting_color_dict":
			{
				"cell_left_clicked" : 
				{
					"foreground" : "white",
					"background" : "purple"
				},
				"hide_filtered_out_entries" : 
				{
					"foreground" : "white",
					"background" : "blue"
				},
				"get_config_item" : 
				{
					"foreground" : "white",
					"background" : "darkCyan"
				}			
			}
		},
		"pygments_syntax_highlighting_style":"vs"
	}
------------------------------------------------------------

`log_file_full_path`  
The log file to load initially on startup. Other log files can be opened from the GUI through File > Open menu. Currently the configuration file name is hard-coded. Later it can be loaded from the GUI.

`file_line_column_number_zero_based`  
The column number that contains the file and line information, assumption here that
file and line will be separated by a colon (file:line). This also can be changed in the future to make it more flexible.

This is the column based on the log___row___pattern regex criteria. First column is index 0.

`log_row_pattern`  
This is the most important configuration. This tells Siraj how to identify fields in the log lines. Matched log line is placed in the table. This uses RegEx named group to achieve two goals:

1.	Extract the different fields from each log line.
2.	Name the columns after the group names (compare the configuration to the screenshot).

`root_source_path_prefix`  
For logs that contains file:line information. This field contains the path prefix that if appended to the file mentioned in the log it produce the full file path. This is used to load the corresponding file if the file:line field was clicked.

`time_stamp_column_number_zero_based`  
Determines the column index that contains the timing information (if any). This is mainly used to calculate the elapsed time between any two selected logs.

`table_conditional_formatting_config`  
Contains the conditional formatting dictionary for foreground and background colors

`foreground_key_column and background_key_column`  
Determines which columns will be used to determine the foreground and background colors of each rows based on the row contents intersecting with that column.

`foreground_color_dict and background_color_dict`     
Dictionaries that hold pairs for key/values. Where the key is a match to perform against each row at cell of intersection with the respective column (foreground/background key), and the value is the color to use for Foreground/background.

Cells that doesn't match any value in this dictionary will be displayed using the default colors. Black foreground on white background.

`special_formatting_key_column`  
This column can have formatting rules that overrides the default rule applied on the row. When a cell in that column match the search criteria it can have a different Foreground/Background than the rest of cells on the same row.

`special_formatting_color_dict`  
A dictionary for the special formatting of cells falling under the `special_formatting_key_column`. The key is the text to match, and the value is a dictionary for the foreground and background colors to use with matching cells.

Example for this can be seen in the _FUNCTION_  column in the screenshot above.

`pygments_syntax_highlighting_style`  
This is the pygment syntax highlighting style to use when (if) showing the source code corresponding to the selected log in the source view. At the time of writing this document, Pygments support the following styles:

['paraiso-light', 'xcode', 'fruity', 'paraiso-dark', 'manni', 'colorful', 'perldoc', 'borland', 'friendly', 'murphy', 'vim', 'autumn', 'trac', 'default', 'rrt', 'pastie', 'monokai', 'igor', 'bw', 'emacs', 'tango', 'native', 'vs']


## Functions

`Search`  
You can select any cell and start typing your search criteria, the selection will jump to the first cell that matches the letter(s) you wrote. More advanced search should be coming when fixing Issue #19.

`Ctrl+H`  
Hides all the rows with fields that matches the selected cells(s).  

`Ctrl+O`  
Shows Only selected. Hides everything except rows with fields that matches the selected cell(s).  

`Ctrl+Del`  
Clears all current filter.  

The three options are also accessible via context menu. To unhide a previously hidden row, you can select the unhide option from the context menu for a list of hidden value of the current column, then select the value to unhide.  

When multiple cells are selected which belong to one or more column(s) and the hide option is triggered, then a row will be hidden if any of its fields(columns) matches any filtered-out value in the corresponding column.

When multiple cells are selected which belong to one or more column(s) and the show-only option is triggered, then a row will be shown only if all of its fields(columns) matches the corresponding filtered-in column.

`Ctrl+P`  
Jumps to the previous matching cell (if one exists) from the same column. Works only when a single cell is selected.  

`Ctrl+N`  
Jumps to the next matching cell (if one exists) from the same column. Works only when a single cell is selected.  

`Ctrl+C`  
Copies the selected cell text into the clipboard. If a single cell is selected when the copy is performed, the text of that cell is copied into clipboard. If multiple cells are selected at the time of copy, then the whole rows representing the selected cells are copied into the clipboard.

`Selecting two cells from different columns`  
will show the elapsed time between the two logs. This is only applicable if the log fields contains a time field and it is specified in the configuration via `time_stamp_column_number_zero_based`.  

`Selecting a cell from the file/line column`  
This will display the code that generated the current log in the `TextView` at the bottom.  

`Double-clicking a cell from the file/line column`  
This will open the file that generated the current log and highlight the current line in an external text editor for more additional facilities (eg. source code cross-reference). Currently this text editor is hard-coded to gedit which only works on Linux AFAIK.


