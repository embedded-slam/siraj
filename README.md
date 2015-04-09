*Siraj* is a cross-platform textual log parser that was built using Python3 and Qt
![Siraj GUI](siraj_screenshot.png "Siraj") 

# Problem
Textual logs can sometimes be huge. And going through them with standard text 
editor without color coding or filtering can be really frustrating job.

# Solution [as offered by *Siraj*]
*Siraj*  aims to facilitate textual logs analysis by presenting the textual
log in a user-friendly tabular format, it also allows the user to show/hide rows 
based on their contents. As well as linking each log trace with the source line
that generated it to give context while analyzing the log.

------------------------------------------------------------

# Quick feature list
1.  Parsing any textual log and present matched fields as a **tabular format**.
2.  Matching logs is based on **Regular Expressions** for maximum flexibility.
2.  **Conditionally formatting** the table cells foreground/background colors based on the contents.
3.	**Hiding** one or more rows based on the contents.
4.	**Showing** only specific rows and hiding everything else.
5.  **Cross-referencing the source code** file/line that generated the log if applicable.
6.	Calculating the **time difference** between any two rows in the table if applicable.
7.  **Cross-platform**, Works on Linux, Windows, and Mac (not tested on Mac yet but it should work).
8.  **Light-weight**, It relies on the Qt (written in C++) to do the heavy-lifting.


------------------------------------------------------------

# Running Siraj
## From the source (Preferred method)

Before you use *Siraj* you'll need to install and configure the following based
on your target system:

1.  [Python3](https://www.python.org/downloads/). 
2.  [SIP](http://www.riverbankcomputing.com/software/sip/download).
3.  [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download).

Once you have the prerequisites you can run the tool using it's main module as
follows:

`python siraj.py` 

## From the binaries
If you only need to use the tool and don't have/need python or Qt, you can 
download one of the following archives based on your system. 
                 
1.	[Linux.]  	(https://github.com/embedded-slam/siraj/raw/release/release/linux/siraj_linux.tar.gz)
2. 	[Windows.]	(https://github.com/embedded-slam/siraj/raw/release/release/windows/siraj_windows.zip) 
3.	Mac.  _Comming soon!_  

Once downloaded, you'll need to extract it and run *sirag*. This will run with 
the provided sample log `sample.log` and the provided sample configuration 
`siraj_configs.json`. You can then fine tune the configuration and load the 
log of your choice.

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
			}		
		}
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

Contains the conditional formatting dictionary for forground and background colors

`foreground_key_column and background_key_column`

Determines which columns will be used to determine the foreground and background colors respectively.

`foreground_color_dict and background_color_dict`
Dictionaries that hold pairs for key/values. Where the key is a match to perform against each row at cell of intersection with the respective column, and the value is the color to use for Foreground/background.

## Functions


`H` 	
Hide all the rows with fields that matches the selected cells(s).  
`O`		
Hides everything except rows with fields that matches the selected cell(s).  
`Del` 	
Clear all current filter.

The three options are also accessible via context menu. To unhide a previously hidden row, you can select the unhide option from the context menu for a list of hidden value of the current column, then select the value to unhide.

NOTE: Filtering works on a single column for now. [Issue #3](https://github.com/embedded-slam/siraj/issues/3 "Issue #3") is there to fix that and extend the filtering to be multi-columns.

`Selecting two cells from different columns`
will show the elapsed time between the two logs. This is only applicable if the log fields contains a time field and it is specified in the configuration via `time_stamp_column_number_zero_based`.

`Selecting a cell from the file/line column`
This will display the code that generated the current log in the `TextView` at the bottom.

`Double-clicking a cell from the file/line column`
This will open the file that generated the current log and highlight the current line in an external text editor for more appealing code view (eg. syntax highlighting). Currently this text editor is hard-coded to gedit which only works on Linux AFAIK. [Issue #15](https://github.com/embedded-slam/siraj/issues/15 "Issue #15") is there to fix that. 
