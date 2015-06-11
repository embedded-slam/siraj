# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'siraj.ui'
#
# Created: Thu Jun 11 08:45:04 2015
#      by: PyQt4 UI code generator 4.11.3
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Siraj.sizePolicy().hasHeightForWidth())
        Siraj.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(Siraj)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(360, 60, 160, 80))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblLogData = QtGui.QTableView(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setBold(True)
        font.setWeight(75)
        self.tblLogData.setFont(font)
        self.tblLogData.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblLogData.setProperty("showDropIndicator", False)
        self.tblLogData.setDragDropOverwriteMode(False)
        self.tblLogData.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tblLogData.setShowGrid(False)
        self.tblLogData.setObjectName(_fromUtf8("tblLogData"))
        self.tblLogData.horizontalHeader().setCascadingSectionResizes(False)
        self.tblLogData.horizontalHeader().setStretchLastSection(True)
        self.tblLogData.verticalHeader().setCascadingSectionResizes(False)
        self.tblLogData.verticalHeader().setMinimumSectionSize(18)
        self.verticalLayout.addWidget(self.tblLogData)
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
        self.dckSource = QtGui.QDockWidget(Siraj)
        self.dckSource.setMinimumSize(QtCore.QSize(56, 41))
        self.dckSource.setAutoFillBackground(True)
        self.dckSource.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dckSource.setObjectName(_fromUtf8("dckSource"))
        self.dckSourceContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dckSourceContents.sizePolicy().hasHeightForWidth())
        self.dckSourceContents.setSizePolicy(sizePolicy)
        self.dckSourceContents.setObjectName(_fromUtf8("dckSourceContents"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.dckSourceContents)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(150, 210, 160, 80))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.lytSource = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.lytSource.setMargin(0)
        self.lytSource.setObjectName(_fromUtf8("lytSource"))
        self.txtSourceFile = QtGui.QTextEdit(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        self.txtSourceFile.setFont(font)
        self.txtSourceFile.setObjectName(_fromUtf8("txtSourceFile"))
        self.lytSource.addWidget(self.txtSourceFile)
        self.dckSource.setWidget(self.dckSourceContents)
        Siraj.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dckSource)
        self.mnuActionOpen = QtGui.QAction(Siraj)
        self.mnuActionOpen.setObjectName(_fromUtf8("mnuActionOpen"))
        self.mnuActionExit = QtGui.QAction(Siraj)
        self.mnuActionExit.setObjectName(_fromUtf8("mnuActionExit"))
        self.mnuActionAbout = QtGui.QAction(Siraj)
        self.mnuActionAbout.setObjectName(_fromUtf8("mnuActionAbout"))
        self.mnuActionLoadConfigs = QtGui.QAction(Siraj)
        self.mnuActionLoadConfigs.setObjectName(_fromUtf8("mnuActionLoadConfigs"))
        self.mnuActionNewFilterView = QtGui.QAction(Siraj)
        self.mnuActionNewFilterView.setObjectName(_fromUtf8("mnuActionNewFilterView"))
        self.menuFile.addAction(self.mnuActionOpen)
        self.menuFile.addAction(self.mnuActionLoadConfigs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.mnuActionNewFilterView)
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
        self.mnuActionOpen.setText(_translate("Siraj", "Open log file...", None))
        self.mnuActionExit.setText(_translate("Siraj", "Exit", None))
        self.mnuActionAbout.setText(_translate("Siraj", "About", None))
        self.mnuActionLoadConfigs.setText(_translate("Siraj", "Load configuration...", None))
        self.mnuActionNewFilterView.setText(_translate("Siraj", "New Filter View...", None))

