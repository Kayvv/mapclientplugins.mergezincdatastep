# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mergezincdatawidget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_MergeZincDataWidget(object):
    def setupUi(self, MergeZincDataWidget):
        if not MergeZincDataWidget.objectName():
            MergeZincDataWidget.setObjectName(u"MergeZincDataWidget")
        MergeZincDataWidget.resize(715, 528)
        self.gridLayout = QGridLayout(MergeZincDataWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBoxInputOrder = QCheckBox(MergeZincDataWidget)
        self.checkBoxInputOrder.setObjectName(u"checkBoxInputOrder")

        self.gridLayout.addWidget(self.checkBoxInputOrder, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonDone = QPushButton(MergeZincDataWidget)
        self.pushButtonDone.setObjectName(u"pushButtonDone")

        self.horizontalLayout.addWidget(self.pushButtonDone)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.groupBoxMergeMarkersMap = QGroupBox(MergeZincDataWidget)
        self.groupBoxMergeMarkersMap.setObjectName(u"groupBoxMergeMarkersMap")
        self.verticalLayout = QVBoxLayout(self.groupBoxMergeMarkersMap)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableViewMarkerMap = QTableView(self.groupBoxMergeMarkersMap)
        self.tableViewMarkerMap.setObjectName(u"tableViewMarkerMap")

        self.verticalLayout.addWidget(self.tableViewMarkerMap)


        self.gridLayout.addWidget(self.groupBoxMergeMarkersMap, 0, 0, 1, 2)


        self.retranslateUi(MergeZincDataWidget)

        QMetaObject.connectSlotsByName(MergeZincDataWidget)
    # setupUi

    def retranslateUi(self, MergeZincDataWidget):
        MergeZincDataWidget.setWindowTitle(QCoreApplication.translate("MergeZincDataWidget", u"Merge Zinc Data", None))
        self.checkBoxInputOrder.setText(QCoreApplication.translate("MergeZincDataWidget", u"Switch order of input data", None))
        self.pushButtonDone.setText(QCoreApplication.translate("MergeZincDataWidget", u"Done", None))
        self.groupBoxMergeMarkersMap.setTitle(QCoreApplication.translate("MergeZincDataWidget", u"Merge markers", None))
    # retranslateUi

