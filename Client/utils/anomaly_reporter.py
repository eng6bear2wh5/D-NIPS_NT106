import socket
import json
import time
import threading
import queue
import logging
from datetime import datetime
from utils.dh_utils import (
    deserialize_dh_parameters,
    generate_dh_private_key,
    serialize_dh_public_key,
    deserialize_dh_public_key,
    derive_aes_key_from_shared,
    send_message_dh,      
    recv_message_dh  
)
from utils.crypto_util import CryptoUtil 

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
    

        self.crypto_util = None # Sẽ được khởi tạo sau khi trao đổi DH thành công
        self.aes_key: bytes = None # Khóa AES được dẫn xuất
        
    def _perform_dh_key_exchange(self) -> bool:
            if not self.socket:
                self.logger.error("Socket không khả dụng cho trao đổi DH.")
                return False
            
            try:
                self.logger.info("Bắt đầu trao đổi khóa Diffie-Hellman...")
                self.socket.settimeout(30) # Timeout cho các thao tác socket trong DH

                self.logger.info("Đang nhận tham số DH từ server...")
                dh_params_pem = recv_message_dh(self.socket) # <--- SỬ DỤNG HÀM MỚI
                # self.logger.debug(f"Client received DH params PEM (len {len(dh_params_pem)}):\n{dh_params_pem.decode(errors='ignore')}")
                dh_parameters = deserialize_dh_parameters(dh_params_pem)
                self.logger.info("Đã nhận và tải tham số DH.")

                self.logger.info("Đang nhận khóa công khai DH của server...")
                server_public_key_pem = recv_message_dh(self.socket) # <--- SỬ DỤNG HÀM MỚI
                # self.logger.debug(f"Client received Server Public Key PEM (len {len(server_public_key_pem)}):\n{server_public_key_pem.decode(errors='ignore')}")
                server_dh_public_key = deserialize_dh_public_key(server_public_key_pem)
                self.logger.info("Đã nhận khóa công khai DH của server.")

                client_dh_private_key = generate_dh_private_key(dh_parameters)
                client_dh_public_key = client_dh_private_key.public_key()
                client_dh_public_key_pem = serialize_dh_public_key(client_dh_public_key)

                self.logger.info("Đang gửi khóa công khai DH của client cho server...")
                send_message_dh(self.socket, client_dh_public_key_pem) # <--- SỬ DỤNG HÀM MỚI
                
                shared_secret_bytes = client_dh_private_key.exchange(server_dh_public_key)
                
                self.aes_key = derive_aes_key_from_shared(shared_secret_bytes, key_length_bytes=32)
                self.crypto_util = CryptoUtil(self.aes_key)
                
                self.logger.info(f"Trao đổi khóa Diffie-Hellman thành công. Khóa AES đã được dẫn xuất (4 byte đầu hex: {self.aes_key[:4].hex()}).")
                self.socket.settimeout(None) 
                return True

            except (socket.timeout, ConnectionAbortedError, ValueError) as e_dh:
                self.logger.error(f"Trao đổi khóa DH thất bại: {e_dh}")
            except Exception as e: 
                self.logger.error(f"Lỗi trong quá trình xử lý DH: {e}", exc_info=True)
            
            if self.socket:
                try: self.socket.close()
                except: pass
            self.socket = None
            self.crypto_util = None
            self.aes_key = None
            return False


    def connect(self):
        """Kết nối tới server"""
        try:
            if self.socket:
                self.socket.close()
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            self.logger.info(f"Đã kết nối tới server {self.server_host}:{self.server_port}")

            if not self._perform_dh_key_exchange():
                self.logger.error("Không thể thiết lập phiên bảo mật qua trao đổi khóa DH.")
                self.connected = False
                # _perform_dh_key_exchange đã đóng socket nếu lỗi
                return False
            return True
        
        except Exception as e:
            self.connected = False
            self.logger.error(f"Lỗi khi kết nối tới server: {e}")
            return False
    
    def start(self):
        """Bắt đầu thread gửi báo cáo"""
        if self.running:
            return
        print("start")
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


    def _requeue_report(self, report): # Hàm helper để đưa báo cáo lại vào queue
        if report is None: return # Không đưa tín hiệu dừng vào lại queue
        try:
            self.report_queue.put(report, block=False)
            self.logger.info(f"Đã đưa báo cáo (ID: {report.get('flow', {}).get('id', 'N/A')}) trở lại hàng đợi.")
        except queue.Full:
            self.logger.warning(f"Hàng đợi báo cáo đầy, bỏ qua báo cáo (ID: {report.get('flow', {}).get('id', 'N/A')}) sau khi gửi thất bại.")


    def _send_report(self, report):
        """Gửi báo cáo tới server"""

        if not self.crypto_util: # Kiểm tra crypto_util đã được khởi tạo chưa
            self.logger.error("CryptoUtil chưa được khởi tạo. Không thể gửi báo cáo mã hóa.")
            self.connected = False # Đánh dấu mất kết nối vì không thể mã hóa
            return False
        
        if self.socket is None or self.socket.fileno() == -1:
            self.logger.error("Socket không hợp lệ hoặc đã đóng trước khi gửi báo cáo.")
            self.connected = False # Đảm bảo trạng thái connected đúng
            # Không raise ConnectionError ở đây ngay, để _reporter_loop xử lý việc kết nối lại
            # Thay vào đó, có thể đưa báo cáo lại vào queue và return False
            self._requeue_report(report) # Đưa lại báo cáo vào queue
            return False # Báo hiệu gửi thất bại để _reporter_loop thử kết nối lại
        
        try:
            # Chuyển đổi báo cáo thành JSON và gửi đi
            json_data = json.dumps(report)
            payload_to_send = self.crypto_util.encrypt(json_data)
            message = payload_to_send.encode('utf-8') + b'\n'  # Thêm ký tự xuống dòng để phân biệt các báo cáo
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
    
    def report_anomaly(self, packet_info, anomaly_info, raw_packet=None, agent_id=None, agent_hostname=None, agent_os=None):
        """
        Tạo báo cáo bất thường và gửi tới server
        
        Args:
            packet_info: Thông tin gói tin đã phân tích
            anomaly_info: Tuple (is_anomaly, score, flow_score)
            raw_packet: Dữ liệu gói tin thô (nếu có)
        """
        is_anomaly, anomaly_score, flow_score = anomaly_info
        
        # Chỉ báo cáo các gói bất thường
        # if is_anomaly != -1 or flow_score < 3:
        #     return
        
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
            "agent": {
            "id": str(agent_id),
            "hostname": agent_hostname,
            "os": agent_os
            },

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