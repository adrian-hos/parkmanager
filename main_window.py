# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window14FlLHmO.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QGridLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1029, 597)
        self.actionNew_database = QAction(MainWindow)
        self.actionNew_database.setObjectName(u"actionNew_database")
        icon = QIcon(QIcon.fromTheme(u"document-new"))
        self.actionNew_database.setIcon(icon)
        self.actionOpen_database = QAction(MainWindow)
        self.actionOpen_database.setObjectName(u"actionOpen_database")
        icon1 = QIcon(QIcon.fromTheme(u"document-open"))
        self.actionOpen_database.setIcon(icon1)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon2 = QIcon(QIcon.fromTheme(u"document-save"))
        self.actionSave.setIcon(icon2)
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        icon3 = QIcon(QIcon.fromTheme(u"document-save-as"))
        self.actionSave_As.setIcon(icon3)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        icon4 = QIcon(QIcon.fromTheme(u"application-exit"))
        self.actionQuit.setIcon(icon4)
        self.actionAdd = QAction(MainWindow)
        self.actionAdd.setObjectName(u"actionAdd")
        icon5 = QIcon(QIcon.fromTheme(u"list-add"))
        self.actionAdd.setIcon(icon5)
        self.actionRemove = QAction(MainWindow)
        self.actionRemove.setObjectName(u"actionRemove")
        icon6 = QIcon(QIcon.fromTheme(u"list-remove"))
        self.actionRemove.setIcon(icon6)
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        icon7 = QIcon(QIcon.fromTheme(u"preferences-other"))
        self.actionPreferences.setIcon(icon7)
        self.actionParkManager_Handbook = QAction(MainWindow)
        self.actionParkManager_Handbook.setObjectName(u"actionParkManager_Handbook")
        icon8 = QIcon(QIcon.fromTheme(u"help-contents"))
        self.actionParkManager_Handbook.setIcon(icon8)
        self.actionAbout_ParkManager = QAction(MainWindow)
        self.actionAbout_ParkManager.setObjectName(u"actionAbout_ParkManager")
        icon9 = QIcon(QIcon.fromTheme(u"help-about"))
        self.actionAbout_ParkManager.setIcon(icon9)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacerCameraRight = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacerCameraRight, 0, 3, 3, 1)

        self.horizontalSpacerCameraLeft = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacerCameraLeft, 0, 0, 3, 1)

        self.labelCamera = QLabel(self.centralwidget)
        self.labelCamera.setObjectName(u"labelCamera")
        self.labelCamera.setMinimumSize(QSize(640, 480))

        self.gridLayout_2.addWidget(self.labelCamera, 1, 1, 1, 2)

        self.verticalSpacerCameraBottom = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacerCameraBottom, 2, 1, 1, 2)

        self.verticalSpacerCameraTop = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacerCameraTop, 0, 1, 1, 2)

        self.pushButtonClose = QPushButton(self.centralwidget)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.gridLayout_2.addWidget(self.pushButtonClose, 3, 2, 1, 2)

        self.pushButtonOpen = QPushButton(self.centralwidget)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")

        self.gridLayout_2.addWidget(self.pushButtonOpen, 3, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1029, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dWidgetPlateReader = QDockWidget(MainWindow)
        self.dWidgetPlateReader.setObjectName(u"dWidgetPlateReader")
        self.dWidgetPlateReader.setMinimumSize(QSize(364, 204))
        self.dWidgetPlateReader.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.dWidgetContentsPlateReader = QWidget()
        self.dWidgetContentsPlateReader.setObjectName(u"dWidgetContentsPlateReader")
        self.gridLayout_3 = QGridLayout(self.dWidgetContentsPlateReader)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.labelPlateText = QLabel(self.dWidgetContentsPlateReader)
        self.labelPlateText.setObjectName(u"labelPlateText")
        self.labelPlateText.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.labelPlateText, 3, 1, 1, 1)

        self.horizontalSpacerPlateLeft = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacerPlateLeft, 2, 0, 1, 1)

        self.verticalSpacerPlateMiddle1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacerPlateMiddle1, 2, 1, 1, 1)

        self.verticalSpacerPlateMiddle2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacerPlateMiddle2, 4, 1, 1, 1)

        self.horizontalSpacerPlateRight = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacerPlateRight, 2, 2, 1, 1)

        self.verticalSpacerPlateTop = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacerPlateTop, 0, 1, 1, 1)

        self.labelPlate = QLabel(self.dWidgetContentsPlateReader)
        self.labelPlate.setObjectName(u"labelPlate")
        self.labelPlate.setMinimumSize(QSize(300, 50))
        self.labelPlate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.labelPlate, 1, 1, 1, 1)

        self.labelBarrierStatus = QLabel(self.dWidgetContentsPlateReader)
        self.labelBarrierStatus.setObjectName(u"labelBarrierStatus")
        self.labelBarrierStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.labelBarrierStatus, 5, 1, 1, 1)

        self.verticalSpacerPlateBottom = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacerPlateBottom, 6, 1, 1, 1)

        self.dWidgetPlateReader.setWidget(self.dWidgetContentsPlateReader)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dWidgetPlateReader)
        self.dWidgetRecognisedPlates = QDockWidget(MainWindow)
        self.dWidgetRecognisedPlates.setObjectName(u"dWidgetRecognisedPlates")
        self.dWidgetRecognisedPlates.setMinimumSize(QSize(347, 129))
        self.dWidgetRecognisedPlates.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.dWidgetContentsRecognisedPlates = QWidget()
        self.dWidgetContentsRecognisedPlates.setObjectName(u"dWidgetContentsRecognisedPlates")
        self.gridLayout = QGridLayout(self.dWidgetContentsRecognisedPlates)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.dWidgetContentsRecognisedPlates)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        self.dWidgetRecognisedPlates.setWidget(self.dWidgetContentsRecognisedPlates)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dWidgetRecognisedPlates)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew_database)
        self.menuFile.addAction(self.actionOpen_database)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionAdd)
        self.menuEdit.addAction(self.actionRemove)
        self.menuSettings.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionParkManager_Handbook)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_ParkManager)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ParkManager", None))
        self.actionNew_database.setText(QCoreApplication.translate("MainWindow", u"&New database", None))
        self.actionOpen_database.setText(QCoreApplication.translate("MainWindow", u"&Open database...", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save &As...", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"&Add", None))
        self.actionRemove.setText(QCoreApplication.translate("MainWindow", u"&Remove", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"&Preferences...", None))
        self.actionParkManager_Handbook.setText(QCoreApplication.translate("MainWindow", u"&ParkManager Handbook", None))
        self.actionAbout_ParkManager.setText(QCoreApplication.translate("MainWindow", u"&About ParkManager", None))
        self.labelCamera.setText("")
        self.pushButtonClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.pushButtonOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"&Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.dWidgetPlateReader.setWindowTitle(QCoreApplication.translate("MainWindow", u"P&late Reader", None))
        self.labelPlateText.setText("")
        self.labelPlate.setText("")
        self.labelBarrierStatus.setText("")
        self.dWidgetRecognisedPlates.setWindowTitle(QCoreApplication.translate("MainWindow", u"Reco&gnised Plates", None))
    # retranslateUi

