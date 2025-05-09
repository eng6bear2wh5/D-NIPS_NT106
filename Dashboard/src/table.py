import os
import sys
from Custom_Widgets import *
from src.ui_interface import *

class AddTableInfo:
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.ui = MainWindow.ui
        self.addInfoToTable()

    def addInfoToTable(self):
        table = self.ui.table  # Assuming you have a QTableWidget named tableWidget in your UI
        data = [
            ["1", "192.168.1.1", "10.0.0.1", "10.0.0.2", "TCP", "512", "12:30:45", "Active"],
            ["2", "192.168.1.2", "10.0.0.3", "10.0.0.4", "UDP", "1024", "12:31:10", "Inactive"],
            ["3", "192.168.1.3", "10.0.0.5", "10.0.0.6", "TCP", "256", "12:32:00", "Active"],
            ["4", "192.168.1.4", "10.0.0.7", "10.0.0.8", "ICMP", "128", "12:33:15", "Active"],
            ["5", "192.168.1.5", "10.0.0.9", "10.0.0.10", "TCP", "64", "12:34:20", "Inactive"],
            ["6", "192.168.1.6", "10.0.0.11", "10.0.0.12", "UDP", "2048", "12:35:00", "Active"],
            ["7", "192.168.1.7", "10.0.0.13", "10.0.0.14", "TCP", "512", "12:36:10", "Inactive"],
            ["8", "192.168.1.8", "10.0.0.15", "10.0.0.16", "ICMP", "128", "12:37:25", "Active"],
            ["9", "192.168.1.9", "10.0.0.17", "10.0.0.18", "UDP", "1024", "12:38:40", "Inactive"],
            ["10", "192.168.1.10", "10.0.0.19", "10.0.0.20", "TCP", "256", "12:39:55", "Active"],
            ["11", "192.168.1.11", "10.0.0.21", "10.0.0.22", "ICMP", "64", "12:40:30", "Inactive"],
            ["12", "192.168.1.12", "10.0.0.23", "10.0.0.24", "TCP", "512", "12:41:15", "Active"],
            ["13", "192.168.1.13", "10.0.0.25", "10.0.0.26", "UDP", "2048", "12:42:50", "Inactive"],
            ["14", "192.168.1.14", "10.0.0.27", "10.0.0.28", "ICMP", "128", "12:43:35", "Active"],
            ["15", "192.168.1.15", "10.0.0.29", "10.0.0.30", "TCP", "1024", "12:44:20", "Inactive"],
        ]

        table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the cell read-only
                item.setForeground(Qt.white)  # Set the text color to white
                table.setItem(row_idx, col_idx, item)