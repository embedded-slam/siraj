*Siraj* is a cross-platform textual log parser that was built using Python3 and Qt  
![Siraj UI](https://raw.githubusercontent.com/embedded-slam/siraj/release/siraj_screenshot.png)


# Problem
Text-based logs can sometimes be huge. And going through them with standard text 
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
8.	Adding/removing **bookmarks** on desired log traces (i.e. table rows).
9.  **Cross-platform**, Works on Linux, Windows, and Mac (not tested on Mac yet but it should work).
10. **Light-weight**, It relies on the Qt (which is written in C++) to do the heavy-lifting.
11. Generatig **Graphs** out of the existing data using **Regular Expressions**.


------------------------------------------------------------

# Running Siraj
## From Source (Preferred)

Before you use *Siraj* you'll need to install and configure the following based
on your target system:

1.  [Python3](https://www.python.org/downloads/). 
2.  [SIP](http://www.riverbankcomputing.com/software/sip/download).
3.  [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download).
4.	[Pygments](http://pygments.org/download/). For the syntax highlighting functionality.
5.	[PyQtGraph](http://www.pyqtgraph.org/). For the graphing functionality.
6.  [CxFreeze](http://cx-freeze.sourceforge.net/). Optional, for packaging.

Once you have the prerequisites you can run the tool using it's main module as
follows:

`python siraj.py` 

## From Binaries
If you only need to use the tool and don't have/need python or Qt, you can 
download one of the following archives based on your system. 
                 
1.	[Linux.]  	(https://github.com/embedded-slam/siraj/releases/download/v1.2.0/siraj_linux.tar.gz)
2. 	[Windows.]	(https://github.com/embedded-slam/siraj/releases/download/v1.2.0/siraj_windows.zip) 
3.	[Mac.]      (https://github.com/embedded-slam/siraj/releases/download/v1.2.0/siraj_mac.zip) 

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
        "log_row_pattern" : "^(?P<LEVEL>.+)\\|\\|(?P<FUNCTION>.+)\\|\\|(?P<MESSAGE>.+)\\|\\|(?P<TIME>.+)\\|\\|(?P<FILE_AND_LINE>[^:]+:\\d+)\\s*$",
        "time_stamp_column_number_zero_based": 3,
        "user_data_column_zero_based" : 2,
        "source_cross_reference_configs" :
        {
            "root_source_path_prefix" : "",
            "pygments_syntax_highlighting_style":"vs",
            "file_column_number_zero_based": 4,
            "file_column_pattern" : "(?P<FILE>[^:]+):",
            "line_column_number_zero_based": 4,
            "line_column_pattern" : ":(?P<LINE>\\d+)"
        },
        "external_editor_configs" :
        {
            "editor" : "gedit",
            "editor_command_format" : "{editor_executable} +{line_number} {file_name}"
        },
        "table_conditional_formatting_configs" :
        {
            "foreground_key_column" : 0,
            "foreground_color_dict" :
            {
                "DEBUG"     : "green",
                "INFO"      : "blue",
                "WARNING"   : "white"
            },
            "background_key_column" : 0,
            "background_color_dict" :
            {
                "WARNING"   : "orange"
    
            },
            "special_formatting_key_column" : 1,
            "special_formatting_style_dict":
            {
                "style1" :
                {
                    "foreground" : "white",
                    "background" : "purple"
                },
                "style2" :
                {
                    "foreground" : "white",
                    "background" : "blue"
                },
                "style3" :
                {
                    "foreground" : "white",
                    "background" : "darkCyan"
                }
            },
            "special_formatting_color_dict":
            {
                "cell_left_clicked" : "style1",
                "hide_filtered_out_entries" : "style2",
                "get_config_item" : "style3"
            },
            "bookmark_color_dict":
            {
                "foreground" : "black",
                "background" : "yellow"
            }
        },
    
        "graph_configs": {
            "window_dict": {
                "window #1": {
                    "plot_dict": {
                        "plot #1": {
                    "row" : 1,
    
                            "series_dict": {
                                "series #1": {
                                    "symbol": "t",
                                    "color": "red",
                                    "pattern"   : "Value = (\\d+)"
                                }
                            }
                        },
                        "plot #2": {
                    "row" : 2,
    
                            "series_dict": {
                                "series #2": {
                                    "symbol": "+",
                                    "color": "green",
                                    "pattern"   : "The number of items is (\\d+) item\\(s\\)"
                                }
                            }
                        }
                    }
                },
                "window #2": {
                    "plot_dict": {
                        "plot #3": {
                    "row" : 1,
    
                            "series_dict": {
                                "series #3": {
                                    "symbol": "o",
                                    "color": "blue",
                                    "pattern"   : "The number of items is (\\d+) item\\(s\\)"
                                }
                            }
                        }
                    }            
                }
            }
        }
    }
------------------------------------------------------------

`log_file_full_path`  
The log file to load initially on startup. Other log files can be opened from the GUI through File > Open menu. If `log_file_full_path` is empty then nothing is loaded when the tool opens.

`log_row_pattern`  
This is the most important configuration. This tells Siraj how to identify fields in the log lines. Matched log line is placed in the table. This uses RegEx named group to achieve two goals:

1.	Extract the different fields from each log line.
2.	Name the columns after the group names (compare the configuration to the screenshot).

`time_stamp_column_number_zero_based`  
Determines the column index that contains the timing information (if any). This is mainly used to calculate the elapsed time between any two selected logs.

`non_matching_line_target_column_zero_based`
Sometimes, there are log entries that doesn't match the regex pattern specified by _log_row_pattern_, but still it needs to be displayed. This parameter specifies
which column will hold these non matching data when encountered. The values of the remaining columns will be copied as is from the previous row.

`source_cross_reference_configs`  
Holds configurations related to source code cross-referencing. This is used when selecting a table cell to display the corresponding source code that generated the currently selected row (if applicable).

`root_source_path_prefix`  
For logs that contains file:line information. This field contains the path prefix that if appended to the file mentioned in the log it produce the full file path. This is used to load the corresponding file if the file:line field was clicked.

`pygments_syntax_highlighting_style`  
This is the pygment syntax highlighting style to use when (if) showing the source code corresponding to the selected log in the source view. At the time of writing this document, Pygments support the following styles:

['paraiso-light', 'xcode', 'fruity', 'paraiso-dark', 'manni', 'colorful', 'perldoc', 'borland', 'friendly', 'murphy', 'vim', 'autumn', 'trac', 'default', 'rrt', 'pastie', 'monokai', 'igor', 'bw', 'emacs', 'tango', 'native', 'vs']

`file_column_number_zero_based`  
The column number that contains the source file information.

`file_column_pattern`  
The Regex pattern to extract the file name from the `file_column_number_zero_based` column at the selected row.

`line_column_number_zero_based`  
The column number that contains the line number information.

`line_column_pattern`  
The Regex pattern to extract the line number from the `line_column_number_zero_based` column at the selected row.

`external_editor_configs`  
This determine which external editor to use when double clicking a cell to open the corresponding source code in an external text editor.

`editor`  
This is the name of the external editor executable file (ex. gedit, kate, notepad++).

`editor_command_format`  
This is the command format to use when invoking the external editor. For example:

`gedit +30 my_file.c`

This command open my_file.c and highlight line number 30.

`table_conditional_formatting_configs`  
Contains the conditional formatting dictionary for foreground and background colors. Color supported currently are the [Qt predefined colors] (http://pyqt.sourceforge.net/Docs/PyQt4/qcolor.html#predefined-colors) as well as the [SVG colors] (http://www.w3.org/TR/SVG/types.html#ColorKeywords)

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

`bookmark_color_dict`  
Holds the background/foreground colors to use with bookmakrs.

`graph_configs`  
The graph can be specified heirarchical manner as follows
- `window`      This is the top level item. It can hold one or more plots.
- `plot`        This represents one plot. Which is the container of one or more data series.
- `series`      This represents the a single variable to be plotted.

In case of multiple plots in a window, the `row` variable specify the order of the plot within the window.

For each series, the user can specify the following
`symbol`    : The symbol to use to mark the points of that series.
`color`     : Color used to draw the series.
`pattern`   : The pattern used to match the series variable. This use regular expression groups to match a single group to be plotted. In the given config
above, the integer value following the "The number of items is" string will be plotted

If the graph_configs is empty, graphing functionality is disabled automatically. This can be achieved as follows

	"graph_configs" :
	{
	}
	
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

`Ctrl+Up`  
Jumps to the previous matching cell (if one exists) from the same column. Works only when a single cell is selected.  

`Ctrl+Down`  
Jumps to the next matching cell (if one exists) from the same column. Works only when a single cell is selected.  

`Ctrl+C`  
Copies the selected cell text into the clipboard. If a single cell is selected when the copy is performed, the text of that cell is copied into clipboard. If multiple cells are selected at the time of copy, then the whole rows representing the selected cells are copied into the clipboard.

`Ctrl+B` 
Toggles the _bookmarked_ state of the current row. 

`Ctrl+PageUp`  
Jumps to the previous bookmark (if any).

`Ctrl+PageDown`  
Jumps to the next bookmark (if any).

`Ctrl+LeftArrow`  
Jumps to the previous search match (if any).

`Ctrl+RightArrow`  
Jumps to the next search match (if any).

`Ctrl+Shift+B`  
Clears all bookmarks.

`Ctrl+Home`  
Jumps to the first row in the table.

`Ctrl+End`  
Jumps to the last row in the table.

`F5`  
Reload the currently loaded file from the desk. Useful if the file contents can change while opening it.



`Selecting two cells from different columns`  
will show the elapsed time between the two logs. This is only applicable if the log fields contains a time field and it is specified in the configuration via `time_stamp_column_number_zero_based`.  

`Selecting a cell with source view open`  
This will display the code that generated the current log in the `SourceView` at the bottom. Assuming `file_column_number_zero_based`, `file_column_pattern`, `line_column_number_zero_based`, and `line_column_pattern` are set properly.   

`Double-clicking a cell`  
This will open the file that generated the current log in an external text editor and highlight the current line. It can be useful if the user want more facilities (eg. source code cross-reference). 

`Drag and Drop`  
Drag log file from your file explorer and drop them into the table to load them. The log file shall follow the same format as that defined in the currently loaded configuration file. It currently support dropping a single log file at a time, when dropping more than one file, the first one is loaded and the rest are ignored.



