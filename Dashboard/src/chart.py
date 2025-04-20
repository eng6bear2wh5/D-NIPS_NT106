from Custom_Widgets import *
# IMPORT PyQtGraph
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from PySide6.QtWidgets import QVBoxLayout
from pyqtgraph import AxisItem
from PySide6.QtCore import QTimer
import random
from datetime import datetime
from pyqtgraph import AxisItem

class InitializeChart:
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.ui = MainWindow.ui
        self.addChartToDashboard()

    class TimeAxisItem(AxisItem):
        """Trục X tùy chỉnh để hiển thị thời gian."""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.time_labels = []

        def update_labels(self, labels):
            """Cập nhật nhãn trục X."""
            self.time_labels = labels

        def tickStrings(self, values, scale, spacing):
            """Hiển thị nhãn trục X."""
            return [self.time_labels[int(v)] if 0 <= int(v) < len(self.time_labels) else "" for v in values]

    def addChartToDashboard(self):
        """Thêm biểu đồ thời gian thực vào widget graph trong dashboardPage."""
        # Kiểm tra widget graph
        if not hasattr(self.ui, "graph"):
            print("Widget 'graph' không tồn tại trong giao diện!")
            return

        # Đặt chiều cao cố định cho widget graph
        self.ui.graph.setMinimumHeight(300)
        self.ui.graph.setMaximumHeight(300)  # Giới hạn chiều cao

        # Tạo trục X tùy chỉnh
        self.time_axis = self.TimeAxisItem(orientation='bottom')
        self.chart = pg.PlotWidget(axisItems={'bottom': self.time_axis})
        self.chart.setBackground('k')  # Đặt nền đen cho biểu đồ
        self.chart.setTitle("Real-Time Packet Anomalies", color="w", size="12pt")  # Tiêu đề màu trắng
        self.chart.setLabel("left", "Packets", color="w", size="10pt")  # Nhãn trục Y màu trắng
        self.chart.addLegend(labelTextColor="w")  # Chú thích màu trắng
        self.chart.showGrid(x=True, y=True, alpha=0.3)  # Lưới mờ
        self.chart.setLabel("bottom", "Time", color="w", size="10pt")  # Nhãn trục X màu trắng
        self.chart.setLabel("left", "Anomalous Packets", color="w", size="10pt")  # Nhãn trục Y màu trắng

        # Kiểm tra layout hiện tại
        layout = self.ui.graph.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.graph)
            self.ui.graph.setLayout(layout)

        # Xóa các widget cũ trong layout (nếu có)
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Thêm widget biểu đồ vào layout
        layout.addWidget(self.chart)

        # Khởi tạo dữ liệu và vẽ biểu đồ
        self.initRealTimeChart()

    def initRealTimeChart(self):
        """Khởi tạo dữ liệu và cập nhật biểu đồ thời gian thực."""
        self.x_data = []  # Dữ liệu trục X (thời gian)
        self.y_data = []  # Dữ liệu trục Y (số gói tin bất thường)
        self.max_points = 50  # Số điểm tối đa hiển thị trên biểu đồ

        # Tạo đường biểu đồ
        self.curve = self.chart.plot(
            self.x_data, self.y_data,
            pen=pg.mkPen(color="w", width=2),  # Đường biểu đồ màu trắng
            name="Anomalous Packets"
        )

        # Thiết lập Timer để cập nhật dữ liệu
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateRealTimeChart)
        self.timer.start(1000)  # Cập nhật mỗi giây

    def updateRealTimeChart(self):
        """Cập nhật dữ liệu thời gian thực cho biểu đồ."""
        # Lấy thời gian hiện tại
        current_time = datetime.now().strftime("%H:%M:%S")

        # Sinh dữ liệu ngẫu nhiên (thay bằng dữ liệu thực tế nếu có)
        new_packet_count = random.randint(0, 100)  # Giá trị luôn >= 0

        # Thêm dữ liệu mới
        self.x_data.append(current_time)
        self.y_data.append(new_packet_count)

        # Giới hạn số điểm hiển thị
        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.y_data.pop(0)

        # Cập nhật nhãn trục X
        self.time_axis.update_labels(self.x_data)

        # Cập nhật đường biểu đồ
        self.curve.setData(range(len(self.x_data)), self.y_data)
