# GUI functions

#IMPORTS NECESSARY FOR GUI
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay

from PySide6.QtCore import QSettings
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtWidgets import QGraphicsDropShadowEffect

class GuiFunctions:
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.parent = MainWindow.parent()

        #initialize app themes
        self.initAppThemes()

    #INITIALIZE APP THEMES
    def initAppThemes(self):
        """ Intialize the app themes from the settings"""
        settings = QSettings()
        curentTheme = settings.value("theme")
        print("Current Theme: ", curentTheme)

    def showDashboardPage(self):
        """Chuyển sang trang dashboardPage."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.dashboarPage)
