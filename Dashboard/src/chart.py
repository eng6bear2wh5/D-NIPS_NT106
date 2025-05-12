from Custom_Widgets import *
# IMPORT PyQtGraph
import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QColor
from datetime import datetime

class InitializeChart:
    def __init__(self, chart_container):
        self.chart_container = chart_container
        self._setup_chart()

    def _setup_chart(self):
        # Tạo PlotWidget nếu chưa có
        if hasattr(self.chart_container, '_plot_widget') and self.chart_container._plot_widget:
            self.plot_widget = self.chart_container._plot_widget
        else:
            self.plot_widget = pg.PlotWidget()
            self.chart_container._plot_widget = self.plot_widget
            layout = self.chart_container.layout()
            if layout is None:
                layout = QVBoxLayout(self.chart_container)
                self.chart_container.setLayout(layout)
            layout.addWidget(self.plot_widget)
            self.plot_widget.setBackground('#0F121A')
            self.plot_widget.setTitle("Packets per Second", color="#FFFFFF", size="10pt")
        # Thiết lập trục
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('left', 'Packets', color='w', size='8pt')
        self.plot_widget.setLabel('bottom', 'Time', color='w', size='8pt')
        # Dữ liệu
        self.x_data = []
        self.y_total = []
        self.y_anomalous = []
        self.max_points = None  # Không giới hạn số điểm
        # Đường cho gói tin bất thường (bên trái)
        self.curve_anomalous = self.plot_widget.plot(pen=pg.mkPen(color="#E91E63", width=2), name="Anomalous Packets")
        # Đường cho tổng số gói tin (bên phải)
        self.curve_total = self.plot_widget.plot(pen=pg.mkPen(color="#2196F3", width=2), name="Total Packets")

    def update(self, anomalous_count, total_count):
        current_time_str = datetime.now().strftime("%H:%M:%S")
        self.x_data.append(current_time_str)
        self.y_anomalous.append(anomalous_count)
        self.y_total.append(total_count)
        # Không pop dữ liệu cũ, giữ toàn bộ lịch sử
        # Vẽ đường: anomalous nằm bên trái, total nằm bên phải
        x_idx = list(range(len(self.x_data)))
        self.curve_anomalous.setData(x_idx, self.y_anomalous)
        self.curve_total.setData(x_idx, self.y_total)
        # Cập nhật nhãn trục X
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([[(i, t) for i, t in enumerate(self.x_data)]])
        self.plot_widget.getPlotItem().setAxisItems({'bottom': stringaxis})

