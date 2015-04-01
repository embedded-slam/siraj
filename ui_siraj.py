# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'siraj.ui'
#
# Created: Wed Apr  1 08:05:09 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Siraj(object):
    def setupUi(self, Siraj):
        Siraj.setObjectName(_fromUtf8("Siraj"))
        Siraj.resize(994, 905)
        self.centralwidget = QtGui.QWidget(Siraj)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(260, 220, 160, 191))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.verticalLayoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblLogData = QtGui.QTableView(self.splitter)
        self.tblLogData.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblLogData.setProperty("showDropIndicator", False)
        self.tblLogData.setDragDropOverwriteMode(False)
        self.tblLogData.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tblLogData.setObjectName(_fromUtf8("tblLogData"))
        self.tblLogData.horizontalHeader().setStretchLastSection(False)
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lblSourceFileName = QtGui.QLabel(self.layoutWidget)
        self.lblSourceFileName.setFrameShape(QtGui.QFrame.Box)
        self.lblSourceFileName.setFrameShadow(QtGui.QFrame.Plain)
        self.lblSourceFileName.setText(_fromUtf8(""))
        self.lblSourceFileName.setAlignment(QtCore.Qt.AlignCenter)
        self.lblSourceFileName.setObjectName(_fromUtf8("lblSourceFileName"))
        self.verticalLayout_2.addWidget(self.lblSourceFileName)
        self.txtSourceFile = QtGui.QTextEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        self.txtSourceFile.setFont(font)
        self.txtSourceFile.setObjectName(_fromUtf8("txtSourceFile"))
        self.verticalLayout_2.addWidget(self.txtSourceFile)
        self.verticalLayout.addWidget(self.splitter)
        Siraj.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Siraj)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 994, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        Siraj.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Siraj)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Siraj.setStatusBar(self.statusbar)
        self.mnuActionOpen = QtGui.QAction(Siraj)
        self.mnuActionOpen.setObjectName(_fromUtf8("mnuActionOpen"))
        self.mnuActionExit = QtGui.QAction(Siraj)
        self.mnuActionExit.setObjectName(_fromUtf8("mnuActionExit"))
        self.mnuActionAbout = QtGui.QAction(Siraj)
        self.mnuActionAbout.setObjectName(_fromUtf8("mnuActionAbout"))
        self.menuFile.addAction(self.mnuActionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.mnuActionExit)
        self.menuAbout.addAction(self.mnuActionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(Siraj)
        QtCore.QMetaObject.connectSlotsByName(Siraj)

    def retranslateUi(self, Siraj):
        Siraj.setWindowTitle(_translate("Siraj", "Siraj", None))
        self.menuFile.setTitle(_translate("Siraj", "File", None))
        self.menuAbout.setTitle(_translate("Siraj", "Help", None))
        self.mnuActionOpen.setText(_translate("Siraj", "Open...", None))
        self.mnuActionExit.setText(_translate("Siraj", "Exit", None))
        self.mnuActionAbout.setText(_translate("Siraj", "About", None))

