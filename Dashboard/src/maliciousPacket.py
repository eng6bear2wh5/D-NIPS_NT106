import os
import sys
from Custom_Widgets import *
from src.ui_interface import *
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QColor # Changed from PySide6.QtCore import Qt, as QColor is more specific

class AddTableInfo:  # This class will manage the 'anomalous_packets_table'
    def __init__(self, table_widget):
        self.table = table_widget
        if self.table is None:
            print("Error: AddTableInfo initialized with a None table_widget.")
            return
        self._setup_headers()

    def _setup_headers(self):
        headers = [
            "No.", "Time", "Src IP", "Dst IP", "Protocol",
            "Src Port", "Dst Port", "App Proto", "Size",
            "Status", "Anomaly Score", "Flow Score", "Details"
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)
        self.table.horizontalHeader().setVisible(True)

    def add_packet_row(self, packet_row_data):
        if self.table is None:
            print("Error: Cannot add row, table_widget is None in AddTableInfo.")
            return
            
        if not isinstance(packet_row_data, list) or len(packet_row_data) != self.table.columnCount():
            # print(f"Skipping malformed packet data for malicious table: {packet_row_data}, expected {self.table.columnCount()} columns")
            return
        
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for col_idx, cell_data in enumerate(packet_row_data):
            item = QTableWidgetItem(str(cell_data))
            # Ensure item flags allow it to be displayed and are not editable
            item.setFlags(item.flags() & ~Qt.ItemIsEditable if hasattr(Qt, 'ItemIsEditable') else item.flags()) # Check if Qt is imported
            item.setForeground(QColor("white")) # Set text color to white
            self.table.setItem(row_position, col_idx, item)
        self.table.scrollToBottom()

# Minimal Qt import for flags if not already available through other imports
try:
    from PySide6.QtCore import Qt
except ImportError:
    # Fallback or error handling if Qt is absolutely needed and not found
    # For now, the hasattr check handles it if Qt.ItemIsEditable is not defined
    pass