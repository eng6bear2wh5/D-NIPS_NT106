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
                if not self.report_queue.empty():
                    report = self.report_queue.get(block=False)
                    self._send_report(report)
                    self.report_queue.task_done()
                else:
                    time.sleep(0.1)  # Ngủ một chút nếu không có báo cáo
            except queue.Empty:
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Lỗi trong reporter loop: {e}")
                self.connected = False
                time.sleep(self.reconnect_interval)
    
    def _send_report(self, report):
        """Gửi báo cáo tới server"""
        try:
            # Chuyển đổi báo cáo thành JSON và gửi đi
            json_data = json.dumps(report)
            message = json_data.encode('utf-8') + b'\n'  # Thêm ký tự xuống dòng để phân biệt các báo cáo
            self.socket.sendall(message)
            self.logger.debug(f"Đã gửi báo cáo: {report['flow']['id']}")
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi gửi báo cáo: {e}")
            self.connected = False
            # Đưa báo cáo lại vào hàng đợi để thử lại sau
            try:
                self.report_queue.put(report, block=False)
            except queue.Full:
                self.logger.warning("Hàng đợi báo cáo đầy, bỏ qua báo cáo này")
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
        if packet_info["protocol"] in ["TCP", "UDP"]:
            flow_id = f"{packet_info['src_ip']}:{packet_info['src_port']}-{packet_info['dst_ip']}:{packet_info['dst_port']}-{packet_info['protocol']}"
        else:
            flow_id = f"{packet_info['src_ip']}-{packet_info['dst_ip']}-{packet_info['protocol']}"
        
        # Xác định loại giao thức IP
        ip_proto = 0
        if packet_info["protocol"] == "TCP":
            ip_proto = 6
        elif packet_info["protocol"] == "UDP":
            ip_proto = 17
        elif packet_info["protocol"] == "ICMP":
            ip_proto = 1
        
        # Chuẩn bị thông tin về layer giao thức ứng dụng
        proto_layer = {"type": "unknown"}
        if packet_info["app_proto"]:
            proto_layer["type"] = packet_info["app_proto"].lower()
            # Thông tin chi tiết có thể được bổ sung tùy thuộc vào kiểu giao thức
        
        # Tạo thông tin TCP/UDP (nếu có)
        transport_layer = {}
        if packet_info["protocol"] == "TCP":
            # Phân tích các cờ TCP từ details
            flags = {"syn": 0, "ack": 0, "fin": 0, "rst": 0, "psh": 0, "urg": 0}
            if "Flags:" in packet_info["details"]:
                flags_str = packet_info["details"].split("Flags:")[1].strip()
                for flag in ["SYN", "ACK", "FIN", "RST", "PSH", "URG"]:
                    if flag in flags_str:
                        flags[flag.lower()] = 1
            
            transport_layer = {
                "sport": int(packet_info["src_port"]) if packet_info["src_port"] != "N/A" else 0,
                "dport": int(packet_info["dst_port"]) if packet_info["dst_port"] != "N/A" else 0,
                "seq": 0,  # Giá trị mặc định vì không có thông tin
                "ack": 0,  # Giá trị mặc định vì không có thông tin
                "flags": flags,
                "window": 0,  # Giá trị mặc định vì không có thông tin
                "header_len": 20,  # Giá trị TCP header tiêu chuẩn
                "options": []
            }
        elif packet_info["protocol"] == "UDP":
            transport_layer = {
                "sport": int(packet_info["src_port"]) if packet_info["src_port"] != "N/A" else 0,
                "dport": int(packet_info["dst_port"]) if packet_info["dst_port"] != "N/A" else 0,
                "length": packet_info["size"] - 28  # UDP payload length (gói tin size - IP header - UDP header)
            }
        
        # Tạo báo cáo theo định dạng yêu cầu
        current_time = datetime.now().isoformat()
        report = {
            "packet": {
                "ip": {
                    "src": packet_info["src_ip"],
                    "dst": packet_info["dst_ip"],
                    "proto": ip_proto,
                    "ttl": 64,  # Giá trị mặc định vì không có thông tin
                    "id": 0,    # Giá trị mặc định vì không có thông tin
                    "flags": {
                        "df": 0,  # Giá trị mặc định vì không có thông tin
                        "mf": 0   # Giá trị mặc định vì không có thông tin
                    },
                    "frag_offset": 0,
                    "tos": 0,
                    "options": []
                }
            },
            "flow": {
                "id": flow_id,
                "packet_count": 1,  # Có thể cập nhật nếu có thông tin
                "byte_count": packet_info["size"],
                "start_time": current_time,
                "last_time": current_time,
                "inter_packet_time": 0  # Có thể cập nhật nếu có thông tin
            },
            "proto_layer": proto_layer,
            "anomaly": {
                "score": float(anomaly_score),
                "flow_score": flow_score,
                "detection_method": "isolation_forest"
            }
        }
        
        # Thêm thông tin transport layer (TCP/UDP) nếu có
        if transport_layer:
            protocol_key = packet_info["protocol"].lower()
            report["packet"][protocol_key] = transport_layer
        
        # Gửi báo cáo
        try:
            self.report_queue.put(report, block=False)
            self.logger.info(f"Đã thêm báo cáo vào hàng đợi: {flow_id}")
            
            # Bắt đầu thread gửi báo cáo nếu chưa chạy
            if not self.running:
                self.start()
                
            return True
        except queue.Full:
            self.logger.warning(f"Hàng đợi báo cáo đầy, bỏ qua báo cáo: {flow_id}")
            return False