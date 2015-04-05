*Siraj* is a cross-platform textual log parser that was built using Python3 and QT
![Siraj GUI](siraj_screenshot.png "Siraj") 

# The Problem

Textual logs can sometimes be huge. And going through them with standard text 
editor without color coding or filtering can be really frustrating job.


# The Solution [as offered by *Siraj*]

*Siraj*  aims to facilitate textual logs analysis by presenting the textual
log in a user-friendly tabular format, it also allows the user to show/hide rows 
based on their contents.

# Quick Feature List:

1.  Parsing any textual log and present matched fields as a **tabular format**.
2.  Matching logs is based on **Regular Expressions** for maximum flexibility.
2.  **Conditionally formatting** the table cells foreground/background colors based on the contents.
3.	**Hiding** one or more rows based on the contents.
4.	**Showing** only specific rows and hiding everything else.
5.  **Cross-referencing the source code** file/line that generated the log if applicable.
6.	Calculating the **time difference** between any two rows in the table if applicable.

# Prerequisites

Before you use *Siraj*  you'll need to install and configure the following:

1.  [Python3](https://www.python.org/downloads/). 
2.  [SIP](http://www.riverbankcomputing.com/software/sip/download).
3.  [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download).

