This document explains installtion on Ubuntu. Other system should have similar steps.

# Python3
* Install python3 and development packages:
    sudo apt-get install python3 python3-dev python3-pip

# Qt4 and supporting libraries

* Install Qt4
    sudo apt-get install qt4-designer qt4-dev-tools qt4-default qt4-bin-dbg 

* Download SIB from from the following link and extract the downloaded archive to a local directory:
    https://riverbankcomputing.com/software/sip/download
  
* Change directory to the extracted directory, and run the following list of commands to build it
    python3 configure.py
    make -j
    sudo make install

* Download PyQt4 from the following link and extract the downloaded archive to a local directory:
    https://riverbankcomputing.com/software/pyqt/download

* Change directory to the extracted directory, and run the following list of commands to build it
    python3 configure-ng.py      # Accept the license when prompted by typing 'yes' and hitting enter
    make -j
    sudo make install

# PyQtGraph

* Download the source package from here and extract the downloaded archieve to a local directory
    http://www.pyqtgraph.org/
  
* Install it using the following command
    sudo python3 setup.py install

# Pygments

* Install using the following command:
    sudo pip3 install pygments
