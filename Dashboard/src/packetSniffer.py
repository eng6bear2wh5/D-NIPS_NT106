import os
import sys
import random
from datetime import datetime, timedelta
import requests
from PySide6.QtCore import QTimer, QDateTime, Qt
from PySide6.QtWidgets import QTableWidgetItem

# Import the refactored classes
from .chart import InitializeChart
from .maliciousPacket import AddTableInfo

class LivePacketUpdater:
    def __init__(self, 
                 all_packets_table_widget, 
                 anomalous_packets_table_widget, 
                 graph_widget):
        
        # Sử dụng chung một widget cho cả bảng và biểu đồ nếu cần
        self.all_packets_table = all_packets_table_widget
        if anomalous_packets_table_widget is None:
            print("CRITICAL: anomalous_packets_table_widget is None in LivePacketUpdater init.")
            self.anomalous_table_manager = None 
        else:
            self.anomalous_table_manager = AddTableInfo(anomalous_packets_table_widget)

        # Sử dụng self.ui.graph_list cho tất cả các biểu đồ
        self.chart_manager = InitializeChart(graph_widget)

        self.total_packets = 0
        self.total_anomalous_packets = 0
        self.malicious_protocol_counts = {} 

        # Setup the headers for the all packets table
        self._setup_all_packets_table_headers()

    def _setup_all_packets_table_headers(self):
        headers = [
            "No.", "Time", "Src IP", "Dst IP", "Protocol",
            "Src Port", "Dst Port", "App Proto", "Size",
            "Status", "Anomaly Score", "Flow Score", "Details"
        ]
        self.all_packets_table.setColumnCount(len(headers))
        self.all_packets_table.setHorizontalHeaderLabels(headers)
        self.all_packets_table.setRowCount(0)
        self.all_packets_table.horizontalHeader().setVisible(True)

    def _add_row_to_all_packets_table(self, packet_row_data):
        if self.all_packets_table is None:
            print("Error: all_packets_table is None in LivePacketUpdater.")
            return
        # Basic check for column count, assuming all_packets_table is configured with 13 columns
        if len(packet_row_data) != 13: 
            print(f"Skipping malformed packet data for all_packets_table: {packet_row_data}, expected 13 columns")
            return

        row_position = self.all_packets_table.rowCount()
        self.all_packets_table.insertRow(row_position)
        for col_idx, cell_data in enumerate(packet_row_data):
            item = QTableWidgetItem(str(cell_data))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            # Using QColor from Qt for white text, ensure Qt is imported or QColor is available
            try:
                from PySide6.QtGui import QColor
                item.setForeground(QColor("white")) 
            except ImportError:
                pass # Fallback if QColor is not available or handle error
            self.all_packets_table.setItem(row_position, col_idx, item)
        self.all_packets_table.scrollToBottom()

    def process_incoming_data(self, new_packets_data_list):
        current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        if not new_packets_data_list:
            if self.chart_manager:
                self.chart_manager.update(0, 0)
            return

        current_interval_anomalous_count = 0
        protocol_column_index = 4 
        status_column_index = 9   

        for packet_row_data in new_packets_data_list:
            self._add_row_to_all_packets_table(packet_row_data)

            is_anomaly_current_packet = False
            # Nếu status là "Anomaly" thì thêm vào bảng malicious
            if len(packet_row_data) > status_column_index and str(packet_row_data[status_column_index]) == "Anomaly":
                if self.anomalous_table_manager:
                    self.anomalous_table_manager.add_packet_row(packet_row_data)
                self.total_anomalous_packets += 1
                current_interval_anomalous_count += 1
                is_anomaly_current_packet = True
                if len(packet_row_data) > protocol_column_index:
                    protocol = packet_row_data[protocol_column_index]
                    self.malicious_protocol_counts[protocol] = self.malicious_protocol_counts.get(protocol, 0) + 1
        
        
        if self.chart_manager:
            self.chart_manager.update(
                current_interval_anomalous_count,
                len(new_packets_data_list)
            )
            print(f"Total Anomalous Packets: {self.total_anomalous_packets}")
            print(f"Total Packets: {len(new_packets_data_list)}")