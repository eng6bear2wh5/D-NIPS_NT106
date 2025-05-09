# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_interface.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1194, 727)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"background-color: rgb(18, 20, 25);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(8)
        self.centralwidget.setFont(font1)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftMenu = QWidget(self.centralwidget)
        self.leftMenu.setObjectName(u"leftMenu")
        sizePolicy.setHeightForWidth(self.leftMenu.sizePolicy().hasHeightForWidth())
        self.leftMenu.setSizePolicy(sizePolicy)
        self.leftMenu.setMaximumSize(QSize(300, 16777215))
        self.leftMenu.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.verticalLayout = QVBoxLayout(self.leftMenu)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.leftMenu)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton.setMouseTracking(True)
        self.pushButton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/menu.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setCheckable(True)

        self.verticalLayout_2.addWidget(self.pushButton)


        self.verticalLayout.addWidget(self.widget, 0, Qt.AlignLeft|Qt.AlignTop)

        self.widget_2 = QWidget(self.leftMenu)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(12)
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon1 = QIcon()
        icon1.addFile(u":/material_design/icons/material_design/space_dashboard.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setCheckable(True)

        self.verticalLayout_3.addWidget(self.pushButton_2, 0, Qt.AlignHCenter)

        self.pushButton_3 = QPushButton(self.widget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)
        self.pushButton_3.setFont(font2)
        self.pushButton_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_3.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon2 = QIcon()
        icon2.addFile(u":/material_design/icons/material_design/manage_search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon2)

        self.verticalLayout_3.addWidget(self.pushButton_3, 0, Qt.AlignHCenter)

        self.pushButton_6 = QPushButton(self.widget_2)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy1.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy1)
        self.pushButton_6.setFont(font2)
        self.pushButton_6.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_6.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon3 = QIcon()
        icon3.addFile(u":/font_awesome_solid/icons/font_awesome/solid/ban.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_6.setIcon(icon3)

        self.verticalLayout_3.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(self.widget_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setFont(font2)
        self.pushButton_5.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_5.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        icon4 = QIcon()
        icon4.addFile(u":/material_design/icons/material_design/work_history.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_5.setIcon(icon4)

        self.verticalLayout_3.addWidget(self.pushButton_5, 0, Qt.AlignHCenter)

        self.pushButton_4 = QPushButton(self.widget_2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setFont(font2)
        self.pushButton_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_4.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon5 = QIcon()
        icon5.addFile(u":/material_design/icons/material_design/circle_notifications.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_4.setIcon(icon5)

        self.verticalLayout_3.addWidget(self.pushButton_4, 0, Qt.AlignHCenter)

        self.pushButton_7 = QPushButton(self.widget_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setFont(font2)
        self.pushButton_7.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_7.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon6 = QIcon()
        icon6.addFile(u":/feather/icons/feather/tool.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_7.setIcon(icon6)

        self.verticalLayout_3.addWidget(self.pushButton_7, 0, Qt.AlignHCenter)


        self.verticalLayout.addWidget(self.widget_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget_3 = QWidget(self.leftMenu)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_8 = QPushButton(self.widget_3)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setFont(font2)
        self.pushButton_8.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_8.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon7 = QIcon()
        icon7.addFile(u":/material_design/icons/material_design/admin_panel_settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_8.setIcon(icon7)

        self.verticalLayout_4.addWidget(self.pushButton_8, 0, Qt.AlignHCenter)

        self.pushButton_9 = QPushButton(self.widget_3)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setFont(font2)
        self.pushButton_9.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_9.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon8 = QIcon()
        icon8.addFile(u":/material_design/icons/material_design/support_agent.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_9.setIcon(icon8)

        self.verticalLayout_4.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.widget_3)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setFont(font2)
        self.pushButton_10.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_10.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon9 = QIcon()
        icon9.addFile(u":/material_design/icons/material_design/perm_contact_calendar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_10.setIcon(icon9)

        self.verticalLayout_4.addWidget(self.pushButton_10)

        self.pushButton_11 = QPushButton(self.widget_3)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setFont(font2)
        self.pushButton_11.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_11.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon10 = QIcon()
        icon10.addFile(u":/feather/icons/feather/settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_11.setIcon(icon10)
        self.pushButton_11.setCheckable(True)

        self.verticalLayout_4.addWidget(self.pushButton_11)

        self.pushButton_12 = QPushButton(self.widget_3)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setFont(font2)
        self.pushButton_12.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_12.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon11 = QIcon()
        icon11.addFile(u":/material_design/icons/material_design/logout.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_12.setIcon(icon11)

        self.verticalLayout_4.addWidget(self.pushButton_12)


        self.verticalLayout.addWidget(self.widget_3, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.horizontalLayout.addWidget(self.leftMenu)

        self.centerMenu = QWidget(self.centralwidget)
        self.centerMenu.setObjectName(u"centerMenu")
        sizePolicy.setHeightForWidth(self.centerMenu.sizePolicy().hasHeightForWidth())
        self.centerMenu.setSizePolicy(sizePolicy)
        self.centerMenu.setMaximumSize(QSize(1677215, 16777215))
        self.centerMenu.setSizeIncrement(QSize(200, 0))
        self.centerMenu.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.centerMenu)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centerMenu)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMaximumSize(QSize(16777215, 16777215))
        self.stackedWidget.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.settingPage = QWidget()
        self.settingPage.setObjectName(u"settingPage")
        self.verticalLayout_6 = QVBoxLayout(self.settingPage)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.widget_5 = QWidget(self.settingPage)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.verticalLayout_7 = QVBoxLayout(self.widget_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_2 = QLabel(self.widget_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_2)

        self.frame = QFrame(self.widget_5)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.comboBox = QComboBox(self.frame)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.comboBox)


        self.verticalLayout_7.addWidget(self.frame)


        self.verticalLayout_6.addWidget(self.widget_5, 0, Qt.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.settingPage)
        self.dashboardPage = QWidget()
        self.dashboardPage.setObjectName(u"dashboardPage")
        sizePolicy.setHeightForWidth(self.dashboardPage.sizePolicy().hasHeightForWidth())
        self.dashboardPage.setSizePolicy(sizePolicy)
        self.verticalLayout_22 = QVBoxLayout(self.dashboardPage)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.mainBody_2 = QWidget(self.dashboardPage)
        self.mainBody_2.setObjectName(u"mainBody_2")
        sizePolicy.setHeightForWidth(self.mainBody_2.sizePolicy().hasHeightForWidth())
        self.mainBody_2.setSizePolicy(sizePolicy)
        self.mainBody_2.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_18 = QVBoxLayout(self.mainBody_2)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.widget_18 = QWidget(self.mainBody_2)
        self.widget_18.setObjectName(u"widget_18")
        self.verticalLayout_19 = QVBoxLayout(self.widget_18)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.label_19 = QLabel(self.widget_18)
        self.label_19.setObjectName(u"label_19")
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.label_19.setFont(font3)
        self.label_19.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_19.setWordWrap(True)

        self.verticalLayout_19.addWidget(self.label_19)


        self.verticalLayout_18.addWidget(self.widget_18, 0, Qt.AlignLeft|Qt.AlignTop)

        self.widget_19 = QWidget(self.mainBody_2)
        self.widget_19.setObjectName(u"widget_19")
        sizePolicy.setHeightForWidth(self.widget_19.sizePolicy().hasHeightForWidth())
        self.widget_19.setSizePolicy(sizePolicy)
        self.widget_19.setMinimumSize(QSize(0, 0))
        self.verticalLayout_20 = QVBoxLayout(self.widget_19)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.widget_20 = QWidget(self.widget_19)
        self.widget_20.setObjectName(u"widget_20")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_20)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.comboBox_7 = QComboBox(self.widget_20)
        self.comboBox_7.setObjectName(u"comboBox_7")
        self.comboBox_7.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_7.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_6.addWidget(self.comboBox_7)

        self.comboBox_8 = QComboBox(self.widget_20)
        self.comboBox_8.setObjectName(u"comboBox_8")
        self.comboBox_8.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_8.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_6.addWidget(self.comboBox_8)

        self.comboBox_9 = QComboBox(self.widget_20)
        self.comboBox_9.setObjectName(u"comboBox_9")
        self.comboBox_9.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_9.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_6.addWidget(self.comboBox_9)

        self.comboBox_10 = QComboBox(self.widget_20)
        self.comboBox_10.setObjectName(u"comboBox_10")
        self.comboBox_10.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_10.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")

        self.horizontalLayout_6.addWidget(self.comboBox_10)

        self.comboBox_11 = QComboBox(self.widget_20)
        self.comboBox_11.setObjectName(u"comboBox_11")
        self.comboBox_11.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBox_11.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")

        self.horizontalLayout_6.addWidget(self.comboBox_11)


        self.verticalLayout_20.addWidget(self.widget_20, 0, Qt.AlignTop)

        self.widget_21 = QWidget(self.widget_19)
        self.widget_21.setObjectName(u"widget_21")
        sizePolicy.setHeightForWidth(self.widget_21.sizePolicy().hasHeightForWidth())
        self.widget_21.setSizePolicy(sizePolicy)
        self.widget_21.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_7 = QHBoxLayout(self.widget_21)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.widget_22 = QWidget(self.widget_21)
        self.widget_22.setObjectName(u"widget_22")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_22.sizePolicy().hasHeightForWidth())
        self.widget_22.setSizePolicy(sizePolicy2)
        self.widget_22.setMaximumSize(QSize(16777215, 16777215))
        self.widget_22.setFont(font1)
        self.widget_22.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"")
        self.gridLayout_5 = QGridLayout(self.widget_22)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pushButton_35 = QPushButton(self.widget_22)
        self.pushButton_35.setObjectName(u"pushButton_35")
        self.pushButton_35.setFont(font)
        self.pushButton_35.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon12 = QIcon()
        icon12.addFile(u":/feather/icons/feather/users.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_35.setIcon(icon12)
        self.pushButton_35.setIconSize(QSize(30, 30))

        self.gridLayout_5.addWidget(self.pushButton_35, 0, 3, 2, 1)

        self.label_21 = QLabel(self.widget_22)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font2)
        self.label_21.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_5.addWidget(self.label_21, 1, 0, 1, 1)

        self.label_20 = QLabel(self.widget_22)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font2)
        self.label_20.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_5.addWidget(self.label_20, 0, 0, 1, 3)

        self.pushButton_36 = QPushButton(self.widget_22)
        self.pushButton_36.setObjectName(u"pushButton_36")
        self.pushButton_36.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon13 = QIcon()
        icon13.addFile(u":/material_design/icons/material_design/arrow_circle_up.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_36.setIcon(icon13)
        self.pushButton_36.setIconSize(QSize(20, 20))

        self.gridLayout_5.addWidget(self.pushButton_36, 2, 0, 1, 1, Qt.AlignLeft)

        self.label_22 = QLabel(self.widget_22)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font)
        self.label_22.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_5.addWidget(self.label_22, 2, 1, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_22)

        self.widget_23 = QWidget(self.widget_21)
        self.widget_23.setObjectName(u"widget_23")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_23.sizePolicy().hasHeightForWidth())
        self.widget_23.setSizePolicy(sizePolicy3)
        self.widget_23.setMaximumSize(QSize(16777215, 16777215))
        self.widget_23.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.gridLayout_6 = QGridLayout(self.widget_23)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.pushButton_37 = QPushButton(self.widget_23)
        self.pushButton_37.setObjectName(u"pushButton_37")
        self.pushButton_37.setFont(font)
        self.pushButton_37.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon14 = QIcon()
        icon14.addFile(u":/font_awesome_regular/icons/font_awesome/regular/file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_37.setIcon(icon14)
        self.pushButton_37.setIconSize(QSize(30, 30))

        self.gridLayout_6.addWidget(self.pushButton_37, 0, 3, 2, 1)

        self.pushButton_38 = QPushButton(self.widget_23)
        self.pushButton_38.setObjectName(u"pushButton_38")
        self.pushButton_38.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_38.setIcon(icon13)
        self.pushButton_38.setIconSize(QSize(20, 20))

        self.gridLayout_6.addWidget(self.pushButton_38, 2, 0, 1, 1)

        self.label_23 = QLabel(self.widget_23)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font2)
        self.label_23.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_6.addWidget(self.label_23, 0, 0, 1, 3)

        self.label_24 = QLabel(self.widget_23)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font2)
        self.label_24.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_6.addWidget(self.label_24, 1, 0, 1, 1)

        self.label_25 = QLabel(self.widget_23)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font)
        self.label_25.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_6.addWidget(self.label_25, 2, 1, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_23)

        self.widget_24 = QWidget(self.widget_21)
        self.widget_24.setObjectName(u"widget_24")
        sizePolicy2.setHeightForWidth(self.widget_24.sizePolicy().hasHeightForWidth())
        self.widget_24.setSizePolicy(sizePolicy2)
        self.widget_24.setMaximumSize(QSize(16777215, 16777215))
        self.widget_24.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.gridLayout_7 = QGridLayout(self.widget_24)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.pushButton_39 = QPushButton(self.widget_24)
        self.pushButton_39.setObjectName(u"pushButton_39")
        self.pushButton_39.setFont(font)
        self.pushButton_39.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon15 = QIcon()
        icon15.addFile(u":/material_design/icons/material_design/warning_amber.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_39.setIcon(icon15)
        self.pushButton_39.setIconSize(QSize(30, 30))

        self.gridLayout_7.addWidget(self.pushButton_39, 0, 3, 2, 1)

        self.label_26 = QLabel(self.widget_24)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font2)
        self.label_26.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_7.addWidget(self.label_26, 0, 0, 1, 3)

        self.label_27 = QLabel(self.widget_24)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font2)
        self.label_27.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_7.addWidget(self.label_27, 1, 0, 1, 1)

        self.pushButton_40 = QPushButton(self.widget_24)
        self.pushButton_40.setObjectName(u"pushButton_40")
        self.pushButton_40.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_40.setIcon(icon13)
        self.pushButton_40.setIconSize(QSize(20, 20))

        self.gridLayout_7.addWidget(self.pushButton_40, 2, 0, 1, 1)

        self.label_28 = QLabel(self.widget_24)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font)
        self.label_28.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_7.addWidget(self.label_28, 2, 1, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_24)

        self.widget_25 = QWidget(self.widget_21)
        self.widget_25.setObjectName(u"widget_25")
        sizePolicy2.setHeightForWidth(self.widget_25.sizePolicy().hasHeightForWidth())
        self.widget_25.setSizePolicy(sizePolicy2)
        self.widget_25.setMaximumSize(QSize(16777215, 16777215))
        self.widget_25.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.gridLayout_8 = QGridLayout(self.widget_25)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.pushButton_42 = QPushButton(self.widget_25)
        self.pushButton_42.setObjectName(u"pushButton_42")
        self.pushButton_42.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_42.setIcon(icon13)
        self.pushButton_42.setIconSize(QSize(20, 20))

        self.gridLayout_8.addWidget(self.pushButton_42, 2, 0, 1, 1)

        self.label_29 = QLabel(self.widget_25)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font2)
        self.label_29.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_8.addWidget(self.label_29, 0, 0, 1, 3)

        self.pushButton_41 = QPushButton(self.widget_25)
        self.pushButton_41.setObjectName(u"pushButton_41")
        self.pushButton_41.setFont(font)
        self.pushButton_41.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.pushButton_41.setIcon(icon12)
        self.pushButton_41.setIconSize(QSize(30, 30))

        self.gridLayout_8.addWidget(self.pushButton_41, 0, 3, 2, 1)

        self.label_30 = QLabel(self.widget_25)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font2)
        self.label_30.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_8.addWidget(self.label_30, 1, 0, 1, 1)

        self.label_31 = QLabel(self.widget_25)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font)
        self.label_31.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_8.addWidget(self.label_31, 2, 1, 1, 1)


        self.horizontalLayout_7.addWidget(self.widget_25)


        self.verticalLayout_20.addWidget(self.widget_21, 0, Qt.AlignTop)

        self.graph_list = QWidget(self.widget_19)
        self.graph_list.setObjectName(u"graph_list")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.graph_list.sizePolicy().hasHeightForWidth())
        self.graph_list.setSizePolicy(sizePolicy4)
        self.graph_list.setMinimumSize(QSize(958, 350))
        self.graph_list.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.verticalLayout_13 = QVBoxLayout(self.graph_list)
        self.verticalLayout_13.setSpacing(6)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.graph_list)
        self.label.setObjectName(u"label")
        sizePolicy4.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy4)
        self.label.setFont(font2)

        self.verticalLayout_13.addWidget(self.label, 0, Qt.AlignTop)

        self.graph = QWidget(self.graph_list)
        self.graph.setObjectName(u"graph")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.graph.sizePolicy().hasHeightForWidth())
        self.graph.setSizePolicy(sizePolicy5)
        self.graph.setMinimumSize(QSize(0, 320))

        self.verticalLayout_13.addWidget(self.graph)


        self.verticalLayout_20.addWidget(self.graph_list, 0, Qt.AlignTop)

        self.widget_26 = QWidget(self.widget_19)
        self.widget_26.setObjectName(u"widget_26")
        sizePolicy.setHeightForWidth(self.widget_26.sizePolicy().hasHeightForWidth())
        self.widget_26.setSizePolicy(sizePolicy)
        self.widget_26.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.verticalLayout_21 = QVBoxLayout(self.widget_26)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.label_32 = QLabel(self.widget_26)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font2)
        self.label_32.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_21.addWidget(self.label_32)

        self.table = QTableWidget(self.widget_26)
        if (self.table.columnCount() < 8):
            self.table.setColumnCount(8)
        font4 = QFont()
        font4.setKerning(False)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem.setFont(font4);
        __qtablewidgetitem.setBackground(QColor(255, 255, 255));
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.table.setObjectName(u"table")
        self.table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setFrameShadow(QFrame.Sunken)
        self.table.setLineWidth(1)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.horizontalHeader().setVisible(False)
        self.table.horizontalHeader().setMinimumSectionSize(40)
        self.table.horizontalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_21.addWidget(self.table, 0, Qt.AlignTop)


        self.verticalLayout_20.addWidget(self.widget_26, 0, Qt.AlignBottom)


        self.verticalLayout_18.addWidget(self.widget_19, 0, Qt.AlignTop)


        self.verticalLayout_22.addWidget(self.mainBody_2, 0, Qt.AlignTop)

        self.stackedWidget.addWidget(self.dashboardPage)
        self.packetAnalyzerPage = QWidget()
        self.packetAnalyzerPage.setObjectName(u"packetAnalyzerPage")
        self.verticalLayout_9 = QVBoxLayout(self.packetAnalyzerPage)
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.widget_4 = QWidget(self.packetAnalyzerPage)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy6)
        font5 = QFont()
        font5.setPointSize(4)
        self.widget_4.setFont(font5)
        self.widget_4.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_13 = QPushButton(self.widget_4)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy6.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy6)
        self.pushButton_13.setMaximumSize(QSize(20, 15))
        self.pushButton_13.setFont(font1)
        self.pushButton_13.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_13.setIconSize(QSize(0, 0))
        self.pushButton_13.setCheckable(True)
        self.pushButton_13.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_13)

        self.pushButton_14 = QPushButton(self.widget_4)
        self.pushButton_14.setObjectName(u"pushButton_14")
        sizePolicy6.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy6)
        self.pushButton_14.setMaximumSize(QSize(45, 15))
        self.pushButton_14.setFont(font1)
        self.pushButton_14.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_14.setIconSize(QSize(0, 0))
        self.pushButton_14.setCheckable(True)
        self.pushButton_14.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_14)

        self.pushButton_16 = QPushButton(self.widget_4)
        self.pushButton_16.setObjectName(u"pushButton_16")
        sizePolicy6.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy6)
        self.pushButton_16.setMaximumSize(QSize(45, 15))
        self.pushButton_16.setFont(font1)
        self.pushButton_16.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_16.setIconSize(QSize(0, 0))
        self.pushButton_16.setCheckable(True)
        self.pushButton_16.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_16)

        self.pushButton_15 = QPushButton(self.widget_4)
        self.pushButton_15.setObjectName(u"pushButton_15")
        sizePolicy6.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy6)
        self.pushButton_15.setMaximumSize(QSize(45, 15))
        self.pushButton_15.setFont(font1)
        self.pushButton_15.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_15.setIconSize(QSize(0, 0))
        self.pushButton_15.setCheckable(True)
        self.pushButton_15.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_15)

        self.pushButton_17 = QPushButton(self.widget_4)
        self.pushButton_17.setObjectName(u"pushButton_17")
        sizePolicy6.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy6)
        self.pushButton_17.setMaximumSize(QSize(30, 15))
        self.pushButton_17.setFont(font1)
        self.pushButton_17.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_17.setIconSize(QSize(0, 0))
        self.pushButton_17.setCheckable(True)
        self.pushButton_17.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_17)

        self.pushButton_18 = QPushButton(self.widget_4)
        self.pushButton_18.setObjectName(u"pushButton_18")
        sizePolicy6.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy6)
        self.pushButton_18.setMaximumSize(QSize(30, 15))
        self.pushButton_18.setFont(font1)
        self.pushButton_18.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_18.setIconSize(QSize(0, 0))
        self.pushButton_18.setCheckable(True)
        self.pushButton_18.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_18, 0, Qt.AlignLeft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_9.addWidget(self.widget_4, 0, Qt.AlignTop)

        self.widget_6 = QWidget(self.packetAnalyzerPage)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton_22 = QPushButton(self.widget_6)
        self.pushButton_22.setObjectName(u"pushButton_22")
        sizePolicy6.setHeightForWidth(self.pushButton_22.sizePolicy().hasHeightForWidth())
        self.pushButton_22.setSizePolicy(sizePolicy6)
        self.pushButton_22.setMaximumSize(QSize(20, 20))
        font6 = QFont()
        font6.setPointSize(6)
        self.pushButton_22.setFont(font6)
        self.pushButton_22.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon16 = QIcon()
        icon16.addFile(u":/feather/icons/feather/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_22.setIcon(icon16)
        self.pushButton_22.setIconSize(QSize(16, 16))
        self.pushButton_22.setCheckable(True)
        self.pushButton_22.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_22)

        self.pushButton_21 = QPushButton(self.widget_6)
        self.pushButton_21.setObjectName(u"pushButton_21")
        sizePolicy6.setHeightForWidth(self.pushButton_21.sizePolicy().hasHeightForWidth())
        self.pushButton_21.setSizePolicy(sizePolicy6)
        self.pushButton_21.setMaximumSize(QSize(20, 20))
        self.pushButton_21.setFont(font6)
        self.pushButton_21.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon17 = QIcon()
        icon17.addFile(u":/feather/icons/feather/play.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_21.setIcon(icon17)
        self.pushButton_21.setIconSize(QSize(16, 16))
        self.pushButton_21.setCheckable(True)
        self.pushButton_21.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_21)

        self.pushButton_23 = QPushButton(self.widget_6)
        self.pushButton_23.setObjectName(u"pushButton_23")
        sizePolicy4.setHeightForWidth(self.pushButton_23.sizePolicy().hasHeightForWidth())
        self.pushButton_23.setSizePolicy(sizePolicy4)
        self.pushButton_23.setMaximumSize(QSize(20, 20))
        self.pushButton_23.setFont(font6)
        self.pushButton_23.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon18 = QIcon()
        icon18.addFile(u":/feather/icons/feather/pause.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_23.setIcon(icon18)
        self.pushButton_23.setIconSize(QSize(16, 16))
        self.pushButton_23.setCheckable(True)
        self.pushButton_23.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_23)

        self.pushButton_24 = QPushButton(self.widget_6)
        self.pushButton_24.setObjectName(u"pushButton_24")
        sizePolicy4.setHeightForWidth(self.pushButton_24.sizePolicy().hasHeightForWidth())
        self.pushButton_24.setSizePolicy(sizePolicy4)
        self.pushButton_24.setMaximumSize(QSize(20, 20))
        self.pushButton_24.setFont(font6)
        self.pushButton_24.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon19 = QIcon()
        icon19.addFile(u":/material_design/icons/material_design/replay.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_24.setIcon(icon19)
        self.pushButton_24.setIconSize(QSize(16, 16))
        self.pushButton_24.setCheckable(True)
        self.pushButton_24.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_24)

        self.line = QFrame(self.widget_6)
        self.line.setObjectName(u"line")
        sizePolicy6.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy6)
        self.line.setMaximumSize(QSize(1, 15))
        self.line.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 255, 255);")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_5.addWidget(self.line)

        self.pushButton_19 = QPushButton(self.widget_6)
        self.pushButton_19.setObjectName(u"pushButton_19")
        sizePolicy4.setHeightForWidth(self.pushButton_19.sizePolicy().hasHeightForWidth())
        self.pushButton_19.setSizePolicy(sizePolicy4)
        self.pushButton_19.setMaximumSize(QSize(20, 20))
        self.pushButton_19.setFont(font6)
        self.pushButton_19.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon20 = QIcon()
        icon20.addFile(u":/feather/icons/feather/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_19.setIcon(icon20)
        self.pushButton_19.setIconSize(QSize(16, 16))
        self.pushButton_19.setCheckable(True)
        self.pushButton_19.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_19)

        self.pushButton_20 = QPushButton(self.widget_6)
        self.pushButton_20.setObjectName(u"pushButton_20")
        sizePolicy4.setHeightForWidth(self.pushButton_20.sizePolicy().hasHeightForWidth())
        self.pushButton_20.setSizePolicy(sizePolicy4)
        self.pushButton_20.setMaximumSize(QSize(20, 20))
        self.pushButton_20.setFont(font6)
        self.pushButton_20.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon21 = QIcon()
        icon21.addFile(u":/feather/icons/feather/arrow-left.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_20.setIcon(icon21)
        self.pushButton_20.setIconSize(QSize(16, 16))
        self.pushButton_20.setCheckable(True)
        self.pushButton_20.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_20)

        self.pushButton_25 = QPushButton(self.widget_6)
        self.pushButton_25.setObjectName(u"pushButton_25")
        sizePolicy4.setHeightForWidth(self.pushButton_25.sizePolicy().hasHeightForWidth())
        self.pushButton_25.setSizePolicy(sizePolicy4)
        self.pushButton_25.setMaximumSize(QSize(20, 20))
        self.pushButton_25.setFont(font6)
        self.pushButton_25.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon22 = QIcon()
        icon22.addFile(u":/feather/icons/feather/arrow-right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_25.setIcon(icon22)
        self.pushButton_25.setIconSize(QSize(16, 16))
        self.pushButton_25.setCheckable(True)
        self.pushButton_25.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_25)

        self.pushButton_26 = QPushButton(self.widget_6)
        self.pushButton_26.setObjectName(u"pushButton_26")
        sizePolicy4.setHeightForWidth(self.pushButton_26.sizePolicy().hasHeightForWidth())
        self.pushButton_26.setSizePolicy(sizePolicy4)
        self.pushButton_26.setMaximumSize(QSize(20, 20))
        self.pushButton_26.setFont(font6)
        self.pushButton_26.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon23 = QIcon()
        icon23.addFile(u":/feather/icons/feather/arrow-up.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_26.setIcon(icon23)
        self.pushButton_26.setIconSize(QSize(16, 16))
        self.pushButton_26.setCheckable(True)
        self.pushButton_26.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_26)

        self.pushButton_27 = QPushButton(self.widget_6)
        self.pushButton_27.setObjectName(u"pushButton_27")
        sizePolicy4.setHeightForWidth(self.pushButton_27.sizePolicy().hasHeightForWidth())
        self.pushButton_27.setSizePolicy(sizePolicy4)
        self.pushButton_27.setMaximumSize(QSize(20, 20))
        self.pushButton_27.setFont(font6)
        self.pushButton_27.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon24 = QIcon()
        icon24.addFile(u":/feather/icons/feather/arrow-down.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_27.setIcon(icon24)
        self.pushButton_27.setIconSize(QSize(16, 16))
        self.pushButton_27.setCheckable(True)
        self.pushButton_27.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_27)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_9.addWidget(self.widget_6)

        self.packets = QTableWidget(self.packetAnalyzerPage)
        if (self.packets.columnCount() < 7):
            self.packets.setColumnCount(7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.packets.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.packets.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.packets.setHorizontalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.packets.setHorizontalHeaderItem(3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.packets.setHorizontalHeaderItem(4, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.packets.setHorizontalHeaderItem(5, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.packets.setHorizontalHeaderItem(6, __qtablewidgetitem14)
        self.packets.setObjectName(u"packets")
        self.packets.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.packets.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_9.addWidget(self.packets)

        self.stackedWidget.addWidget(self.packetAnalyzerPage)
        self.blackListPage = QWidget()
        self.blackListPage.setObjectName(u"blackListPage")
        self.verticalLayout_10 = QVBoxLayout(self.blackListPage)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_6 = QLabel(self.blackListPage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_6, 0, Qt.AlignVCenter)

        self.stackedWidget.addWidget(self.blackListPage)
        self.activityPage = QWidget()
        self.activityPage.setObjectName(u"activityPage")
        self.verticalLayout_11 = QVBoxLayout(self.activityPage)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_7 = QLabel(self.activityPage)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_7, 0, Qt.AlignVCenter)

        self.stackedWidget.addWidget(self.activityPage)
        self.notificationPage = QWidget()
        self.notificationPage.setObjectName(u"notificationPage")
        self.verticalLayout_12 = QVBoxLayout(self.notificationPage)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_8 = QLabel(self.notificationPage)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_8, 0, Qt.AlignVCenter)

        self.stackedWidget.addWidget(self.notificationPage)
        self.informationPage = QWidget()
        self.informationPage.setObjectName(u"informationPage")
        self.verticalLayout_8 = QVBoxLayout(self.informationPage)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_4 = QLabel(self.informationPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_4, 0, Qt.AlignVCenter)

        self.stackedWidget.addWidget(self.informationPage)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.centerMenu)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Packet Analyzer", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Black List", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Activity", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Notification", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Admin", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Support service", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Contact", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"RISK ANALYSIS", None))
        self.pushButton_35.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"1680", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Total Access", None))
        self.pushButton_36.setText("")
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"8.5% from yesterday", None))
        self.pushButton_37.setText("")
        self.pushButton_38.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Packet Received", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"1680", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"8.5% from yesterday", None))
        self.pushButton_39.setText("")
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Malicious Packet", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"1680", None))
        self.pushButton_40.setText("")
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"8.5% from yesterday", None))
        self.pushButton_42.setText("")
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Total Access", None))
        self.pushButton_41.setText("")
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"1680", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"8.5% from yesterday", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Graph", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Risk Score By Object", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Id", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Client IP", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Source Ip", None));
        ___qtablewidgetitem3 = self.table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Dest IP", None));
        ___qtablewidgetitem4 = self.table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Proto", None));
        ___qtablewidgetitem5 = self.table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Size", None));
        ___qtablewidgetitem6 = self.table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Time", None));
        ___qtablewidgetitem7 = self.table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"State", None));
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"Capture", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"Analyze", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"Statistic", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.pushButton_22.setText("")
        self.pushButton_21.setText("")
        self.pushButton_23.setText("")
        self.pushButton_24.setText("")
        self.pushButton_19.setText("")
        self.pushButton_20.setText("")
        self.pushButton_25.setText("")
        self.pushButton_26.setText("")
        self.pushButton_27.setText("")
        ___qtablewidgetitem8 = self.packets.horizontalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"No.", None));
        ___qtablewidgetitem9 = self.packets.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Time", None));
        ___qtablewidgetitem10 = self.packets.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Source Ip", None));
        ___qtablewidgetitem11 = self.packets.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Destination Ip", None));
        ___qtablewidgetitem12 = self.packets.horizontalHeaderItem(4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Protocol", None));
        ___qtablewidgetitem13 = self.packets.horizontalHeaderItem(5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Length", None));
        ___qtablewidgetitem14 = self.packets.horizontalHeaderItem(6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Info", None));
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"BlackList", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Activity", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Notification", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Information", None))
    # retranslateUi

