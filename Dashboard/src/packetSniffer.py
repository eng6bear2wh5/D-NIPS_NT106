import os
import sys
from Custom_Widgets import *
from src.ui_interface import *
import random
from datetime import datetime, timedelta

class AddPacketsToTable:
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.ui = MainWindow.ui
        self.addPacketsToTable()

    def addPacketsToTable(self):
        table = self.ui.packets 
        protocols = ["TCP", "UDP", "ICMP"]
        statuses = ["OK", "Error", "Timeout"]
        base_time = datetime.strptime("12:30:00", "%H:%M:%S")

        data = []
        for i in range(1, 101):
            time = (base_time + timedelta(seconds=i * 30)).strftime("%H:%M:%S")
            source_ip = f"192.168.1.{i}"
            dest_ip_1 = f"10.0.0.{i * 2 - 1}"
            protocol = random.choice(protocols)
            length = str(random.choice([64, 128, 256, 512, 1024, 2048]))
            status = random.choice(statuses)
            data.append([str(i), time, source_ip, dest_ip_1, protocol, length, status])

        table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the cell read-only
                item.setForeground(Qt.white)  # Set the text color to white
                table.setItem(row_idx, col_idx, item)