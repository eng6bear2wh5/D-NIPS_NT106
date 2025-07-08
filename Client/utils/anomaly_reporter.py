import socket
import json
import time
import threading
import queue
import logging
from datetime import datetime

class AnomalyReporter:
    """
    Class để báo cáo các gói tin bất thường tới server qua socket
    """
    def __init__(self, server_host="127.0.0.1", server_port=9999, reconnect_interval=5, queue_size=1000):
        self.server_host = server_host
        self.server_port = server_port
        self.reconnect_interval = reconnect_interval
        self.socket = None
        self.connected = False
        self.running = False
        
        # Hàng đợi để lưu các báo cáo khi không thể gửi ngay
        self.report_queue = queue.Queue(maxsize=queue_size)
        
        # Biến để lưu trạng thái các luồng
        self.flow_states = {}
        
        # Thiết lập logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("AnomalyReporter")
    
    def connect(self):
        """Kết nối tới server"""
        try:
            if self.socket:
                self.socket.close()
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            self.logger.info(f"Đã kết nối tới server {self.server_host}:{self.server_port}")
            return True
        except Exception as e:
            self.connected = False
            self.logger.error(f"Lỗi khi kết nối tới server: {e}")
            return False
    
    def start(self):
        """Bắt đầu thread gửi báo cáo"""
        if self.running:
            return
        
        self.running = True
        self.reporter_thread = threading.Thread(target=self._reporter_loop)
        self.reporter_thread.daemon = True
        self.reporter_thread.start()
        self.logger.info("Đã khởi động reporter thread")
    
    def stop(self):
        """Dừng thread gửi báo cáo"""
        self.running = False
        if self.socket:
            self.socket.close()
        self.logger.info("Đã dừng reporter thread")
    
    def _should_send_report(self, flow_id):
        """Kiểm tra xem có nên gửi báo cáo cho luồng không"""
        flow = self.flow_states[flow_id]
        current_time = datetime.now().timestamp()
        last_time = datetime.fromisoformat(flow["last_time"]).timestamp()
        # Gửi báo cáo nếu luồng không có gói tin mới trong 5 giây
        return (current_time - last_time) > 5

    def _create_report(self, flow_id):
        """Tạo báo cáo từ trạng thái luồng"""
        flow = self.flow_states[flow_id]
        
        # Tính toán điểm bất thường dựa trên dữ liệu thực tế
        packet_count = flow["packet_count"]
        byte_count = flow["byte_count"]
        duration = (datetime.fromisoformat(flow["last_time"]) - datetime.fromisoformat(flow["start_time"])).total_seconds()
        avg_packet_rate = packet_count / duration if duration > 0 else 0
        
        # Giả sử tính điểm bất thường dựa trên tốc độ gói tin
        score = min(1.0, avg_packet_rate / 100)  # Ví dụ: tốc độ > 100 gói/giây là bất thường
        flow_score = score * 5  # Quy đổi sang thang điểm 5
        
        report = {
            "flow": {
                "id": flow_id,
                "packet_count": packet_count,
                "byte_count": byte_count,
                "start_time": flow["start_time"],
                "last_time": flow["last_time"]
            },
            "anomaly": {
                "score": score,
                "flow_score": flow_score,
                "detection_method": "isolation_forest"
            },
            "packets": flow["packets"]  # Thêm danh sách các gói tin
        }
        return report

    def _reporter_loop(self):
        """Loop chính để gửi các báo cáo trong hàng đợi"""
        while self.running:
            # Kiểm tra kết nối
            if not self.connected:
                if not self.connect():
                    time.sleep(self.reconnect_interval)
                    continue

            # Xử lý các báo cáo trong hàng đợi
            try:
                batch = []
                while not self.report_queue.empty() and len(batch) < 10:  # Gửi tối đa 10 báo cáo mỗi lần
                    report = self.report_queue.get(block=False)
                    batch.append(report)
                    self.report_queue.task_done()

                if batch:
                    json_data = json.dumps(batch)
                    message = json_data.encode('utf-8') + b'\n'
                    self.socket.sendall(message)
                    self.logger.debug(f"Đã gửi batch {len(batch)} báo cáo")
                else:
                    time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Lỗi trong reporter loop: {e}")
                self.connected = False
                time.sleep(self.reconnect_interval)
    
    def _send_report(self, report):
        """Gửi báo cáo tới server"""
        try:
            report["sent_time"] = datetime.now().isoformat()  # Thêm timestamp
            json_data = json.dumps(report)
            message = json_data.encode('utf-8') + b'\n'
            self.socket.sendall(message)
            self.logger.debug(f"Đã gửi báo cáo: {report['flow']['id']}")
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi gửi báo cáo: {e}")
            self.connected = False
            # Đưa báo cáo lại vào hàng đợi hoặc lưu vào file tạm
            try:
                self.report_queue.put(report, block=False)
            except queue.Full:
                self.logger.warning("Hàng đợi báo cáo đầy, lưu báo cáo vào file tạm")
                with open("failed_reports.json", "a") as f:
                    f.write(json.dumps(report) + "\n")
            return False
    
    def report_anomaly(self, packet_info, anomaly_info, raw_packet=None):
        """
        Tạo báo cáo bất thường và gửi tới server
        
        Args:
            packet_info: Thông tin gói tin đã phân tích
            anomaly_info: Tuple (is_anomaly, score, flow_score)
            raw_packet: Dữ liệu gói tin thô (nếu có)
        """
        is_anomaly, anomaly_score, flow_score = anomaly_info
        
        # Chỉ báo cáo các gói bất thường
        if is_anomaly != -1 or flow_score < 3:
            return
        
        # Tạo ID cho luồng
        try:
            flow_id = f"{packet_info['src_ip']}:{packet_info['src_port']}-{packet_info['dst_ip']}:{packet_info['dst_port']}-{packet_info['protocol']}"
        except KeyError as e:
            self.logger.error(f"Thiếu thông tin trong packet_info: {e}")
            return
        
        # Cập nhật trạng thái luồng
        current_time = datetime.now().isoformat()
        if flow_id not in self.flow_states:
            self.flow_states[flow_id] = {
                "packet_count": 0,
                "byte_count": 0,
                "start_time": current_time,
                "last_time": current_time,
                "packets": []  # Danh sách các gói tin
            }
        
        # Khi cập nhật trạng thái luồng
        flow = self.flow_states[flow_id]
        flow["packet_count"] += 1
        flow["byte_count"] += packet_info["size"]
        flow["last_time"] = current_time

        # Thêm thông tin gói tin vào danh sách packets
        flow["packets"].append({
            "timestamp": current_time,
            "src_ip": packet_info["src_ip"],
            "dst_ip": packet_info["dst_ip"],
            "src_port": packet_info["src_port"],
            "dst_port": packet_info["dst_port"],
            "protocol": packet_info["protocol"],
            "payload": raw_packet.hex() if raw_packet else ""  # Payload dạng hex
        })
        
        # Kiểm tra và gửi báo cáo nếu cần thiết
        if self._should_send_report(flow_id):
            report = self._create_report(flow_id)
            self._send_report(report)
        
        # Gửi báo cáo tức thì nếu có lỗi xảy ra
        if anomaly_score > 0.8:
            # Cập nhật trạng thái luồng
            flow["packet_count"] += 1
            flow["byte_count"] += packet_info["size"]
            flow["last_time"] = current_time

            # Tạo và gửi báo cáo tức thì
            report = self._create_report(flow_id)
            self._send_report(report)
        
        # Gửi báo cáo định kỳ cho các luồng còn lại
        for flow_id in list(self.flow_states.keys()):
            if self._should_send_report(flow_id):
                report = self._create_report(flow_id)
                self._send_report(report)
                # Xóa luồng nếu không còn hoạt động
                if (datetime.now().timestamp() - datetime.fromisoformat(self.flow_states[flow_id]["last_time"]).timestamp()) > 60:
                    del self.flow_states[flow_id]
        
        self.logger.debug(f"Trạng thái flow_states: {json.dumps(self.flow_states, indent=2)}")
        self.logger.info(f"Số lượng báo cáo trong hàng đợi: {self.report_queue.qsize()}")