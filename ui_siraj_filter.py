# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'siraj_filter.ui'
#
# Created: Thu Jun 11 09:21:02 2015
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

class Ui_SirajFilter(object):
    def setupUi(self, SirajFilter):
        SirajFilter.setObjectName(_fromUtf8("SirajFilter"))
        SirajFilter.resize(976, 771)
        self.centralwidget = QtGui.QWidget(SirajFilter)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(260, 210, 160, 80))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblLogFilter = QtGui.QTableView(self.verticalLayoutWidget)
        self.tblLogFilter.setObjectName(_fromUtf8("tblLogFilter"))
        self.verticalLayout.addWidget(self.tblLogFilter)
        SirajFilter.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SirajFilter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 976, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        SirajFilter.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SirajFilter)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SirajFilter.setStatusBar(self.statusbar)

        self.retranslateUi(SirajFilter)
        QtCore.QMetaObject.connectSlotsByName(SirajFilter)

    def retranslateUi(self, SirajFilter):
        SirajFilter.setWindowTitle(_translate("SirajFilter", "Siraj Filter", None))

