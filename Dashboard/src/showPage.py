from Custom_Widgets import *

class ShowPageMixin:
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.ui = MainWindow.ui

        #initialize app themes
        #Dashboard Functions
        self.ui.pushButton_2.clicked.connect(self.showDashboardPage)

        #Settings Functions
        self.ui.pushButton_11.clicked.connect(self.showSettingsPage)

        #Packet Analyzer Functions
        self.ui.pushButton_3.clicked.connect(self.showPacketAnalyzerPage)

        #Blacklist Functions
        self.ui.pushButton_6.clicked.connect(self.showBlacklistPage)

        #Activity Functions
        self.ui.pushButton_5.clicked.connect(self.showActivityPage)

        #Notification Functions
        self.ui.pushButton_4.clicked.connect(self.showNotificationPage)

    def showDashboardPage(self):
        """Chuyển sang trang dashboardPage."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.dashboardPage)

    def showSettingsPage(self):
        """Chuyển sang trang settingsPage."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.settingPage)

    def showPacketAnalyzerPage(self):
        """Chuyển sang trang packetAnalyzerPage."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.packetAnalyzerPage)

    def showBlacklistPage(self):
        """Chuyển sang trang blacklistPage."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.blackListPage)

    def showActivityPage(self):
        """Chuyển sang trang activityPage."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.activityPage)

    def showNotificationPage(self):
        """Chuyển sang trang notificationPage."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.notificationPage)