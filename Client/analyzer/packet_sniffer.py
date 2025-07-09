import time
import pcap
import sys
import threading
from collections import defaultdict
from utils.packet_parser import PacketParser
from utils.pcap_handler import PCAPHandler
from models.anomaly_detector import EnhancedAnomalyDetection
from analyzer.visualizer import PacketVisualizer
from utils.anomaly_reporter import AnomalyReporter
from analyzer.data_sender import DataSender
from config import *
import platform

class PacketSniffer:
    def __init__(self, interface=DEFAULT_INTERFACE, output_dir=DEFAULT_OUTPUT_DIR, model_path=DEFAULT_MODEL_PATH, filter_exp=None, analyze_only=False, agent_id=None, agent_hostname=None, agent_os=None, agent_ip_addr=None):
        # Khởi tạo các thành phần
        self.agent_id = agent_id
        self.agent_hostname = agent_hostname
        self.agent_os = agent_os
        self.agent_ip_addr = agent_ip_addr
        self.interface = interface
        self.packet_id = 0
        self.filter_exp = filter_exp  # Thêm thuộc tính lưu filter
        self.analyze_only = analyze_only  # Thêm flag để xác định chế độ chỉ phân tích

        # Khởi tạo đối tượng xử lý file pcap
        self.pcap_handler = PCAPHandler(output_dir=output_dir)
        
        # Khởi tạo đối tượng parser
        self.packet_parser = PacketParser()

        # Khởi tạo DataSender
        self.data_sender = DataSender()
        
        # Chỉ khởi tạo đối tượng pcap nếu không phải chế độ chỉ phân tích
        if not analyze_only:
            try:
                self.pcap_object = pcap.pcap(name=interface, promisc=True, immediate=True)
                
                # Thiết lập filter nếu có
                if self.filter_exp:
                    try:
                        self.pcap_object.setfilter(self.filter_exp)
                        print(f"[+] Đã áp dụng filter: {self.filter_exp}")
                    except Exception as e:
                        print(f"[!] Lỗi khi áp dụng filter: {e}")
                
                print(f"[+] Đã khởi tạo pcap trên interface: {interface}")
            except Exception as e:
                print(f"[!] Lỗi khi khởi tạo pcap: {e}")
                sys.exit(1)
        else:
            self.pcap_object = None
            print(f"[+] Đã khởi tạo trong chế độ chỉ phân tích file")

        # Khởi tạo visualizer
        self.visualizer = PacketVisualizer()

        # Khởi tạo mô hình phát hiện bất thường
        self.anomaly_detector = EnhancedAnomalyDetection(model_path=model_path)    

        # Lưu trữ dữ liệu gói tin để huấn luyện
        self.feature_vectors = []
        self.flow_anomalies = defaultdict(int)
        
        # Khởi tạo reporter để gửi thông tin bất thường tới server
        if ANOMALY_REPORT_ENABLED:
            self.anomaly_reporter = AnomalyReporter(
                server_host=ANOMALY_REPORT_SERVER,
                server_port=ANOMALY_REPORT_PORT,
                reconnect_interval=ANOMALY_REPORT_RETRY,
                queue_size=ANOMALY_REPORT_QUEUE_SIZE
            )
            print(f"[+] Đã khởi tạo reporter kết nối tới {ANOMALY_REPORT_SERVER}:{ANOMALY_REPORT_PORT}")
        else:
            self.anomaly_reporter = None
            print("[!] Báo cáo bất thường qua socket đã bị tắt trong cấu hình")
            
    def detect_anomaly(self, packet_info, timestamp):
        """Phát hiện bất thường trong gói tin"""
        # Trích xuất đặc trưng từ gói tin
        features, flow_key = self.anomaly_detector.extract_features(packet_info, timestamp)
        self.feature_vectors.append(features)

        # Dự đoán bất thường
        is_anomaly, score = self.anomaly_detector.predict(features)

        # Cập nhật thống kê bất thường theo luồng
        if is_anomaly == -1:
            self.flow_anomalies[flow_key] += 1

        # Xác định mức độ nguy hiểm của luồng
        flow_score = 0
        if flow_key in self.flow_anomalies:
            flow_score = self.flow_anomalies[flow_key]
        
        return is_anomaly, score, flow_score

    def parse_packet(self, packet):
        """Phân tích gói tin và trả về thông tin"""
        return self.packet_parser.parse_packet(packet)
    
    def report_anomaly(self, packet_info, anomaly_info, raw_packet=None, agent_id=None, agent_hostname=None, agent_os=None, agent_ip_addr=None):
        """Báo cáo gói tin bất thường tới server nếu đã bật tính năng"""
        if not self.anomaly_reporter or not ANOMALY_REPORT_ENABLED:
            return
            
        is_anomaly, score, flow_score = anomaly_info
        # Kiểm tra ngưỡng báo cáo
        if (is_anomaly == -1 and score < ANOMALY_THRESHOLD) or flow_score >= FLOW_SCORE_THRESHOLD:
            self.anomaly_reporter.report_anomaly(packet_info, anomaly_info, raw_packet, agent_id, agent_hostname, agent_os, agent_ip_addr)

    def start_sniffing(self, max_packets=None):
        # Kiểm tra xem có đang ở chế độ chỉ phân tích không
        if self.analyze_only or self.pcap_object is None:
            print("[!] Không thể bắt gói tin trong chế độ chỉ phân tích")
            return

        # Khởi động reporter nếu có
        if self.anomaly_reporter and ANOMALY_REPORT_ENABLED:
            self.anomaly_reporter.start()

        # Tạo luồng gửi dữ liệu định kỳ
        def periodic_send():
            while True:
                time.sleep(1)  # Gửi dữ liệu mỗi giây
                self.data_sender.send_data()

        sender_thread = threading.Thread(target=periodic_send, daemon=True)
        sender_thread.start()
            
        # Bắt đầu bắt và phân tích gói tin
        self.visualizer.update_display()
        print(f"[+] Bắt đầu bắt gói tin... Nhấn Ctrl+C để dừng")
            
        try:
            for timestamp, packet in self.pcap_object:
                self.packet_id += 1
                
                # Lưu gói tin vào file PCAP
                self.pcap_handler.save_packet_to_pcap(timestamp, packet)
                
                # Phân tích gói tin
                packet_info = self.packet_parser.parse_packet(packet)
                
                # Phát hiện bất thường
                is_anomaly, anomaly_score, flow_score = self.detect_anomaly(packet_info, timestamp)

                # Thêm dữ liệu vào hàng đợi gửi
                self.data_sender.add_data(packet_info, is_anomaly, anomaly_score, flow_score)

                # Thêm gói tin vào visualizer
                self.visualizer.add_packet(packet_info, (is_anomaly, anomaly_score, flow_score))
                
                # Báo cáo bất thường nếu cần
                self.report_anomaly(packet_info, (is_anomaly, anomaly_score, flow_score), packet, self.agent_id, self.agent_hostname, self.agent_os, self.agent_ip_addr)
                
                # Hiển thị bảng
                if self.packet_id % 5 == 0:  # Cập nhật bảng sau mỗi 5 gói tin để giảm nhấp nháy
                    self.visualizer.update_display()
                
                # Hiển thị cảnh báo cho luồng nguy hiểm
                if flow_score >= 5:
                    alert_msg = (f"Phát hiện luồng bất thường kéo dài! "
                            f"({packet_info['src_ip']}:{packet_info['src_port']} -> "
                            f"{packet_info['dst_ip']}:{packet_info['dst_port']} "
                            f"[{packet_info['protocol']}])")
                    self.visualizer.print_alert(alert_msg)
                
                # Cập nhật mô hình định kỳ
                if self.packet_id % 100 == 0 and len(self.feature_vectors) >= 100:
                    if self.anomaly_detector.fit(self.feature_vectors[-1000:]):
                        print(f"[+] Đã cập nhật mô hình phát hiện bất thường với {len(self.feature_vectors[-1000:])} mẫu")
                        # Lưu mô hình
                        self.anomaly_detector.save_model()
                
                # Kiểm tra số lượng gói tin tối đa
                if max_packets and self.packet_id >= max_packets:
                    print(f"[+] Đã đạt số lượng gói tin tối đa ({max_packets}). Dừng bắt gói tin.")
                    break
                
                # Tạm dừng ngắn để giảm tải CPU
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n[!] Đã dừng bắt gói tin do người dùng ngắt")
        except Exception as e:
            print(f"\n[!] Lỗi: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Dừng reporter
            if self.anomaly_reporter and ANOMALY_REPORT_ENABLED:
                self.anomaly_reporter.stop()
                
            # Lưu mô hình trước khi thoát
            if self.feature_vectors and len(self.feature_vectors) > 100:
                self.anomaly_detector.save_model()
            
            # Đóng file PCAP
            pcap_file = self.pcap_handler.close()
            if pcap_file:
                print(f"[+] Đã lưu gói tin vào: {pcap_file}")
            
            # Hiển thị tóm tắt
            self.visualizer.show_summary()
            
            print(f"[+] Tổng số gói tin đã bắt: {self.packet_id}")