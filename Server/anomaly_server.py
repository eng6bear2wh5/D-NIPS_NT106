#!/usr/bin/env python3
"""
Server nhận báo cáo bất thường từ packet_sniffer
"""

import socket
import json
import threading
import logging
import argparse
import time
import os
from datetime import datetime

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AnomalyServer")

MAX_CLIENTS = 10

class AnomalyServer:
    def __init__(self, host="0.0.0.0", port=9999, save_dir="./anomaly_reports"):
        self.host = host
        self.port = port
        self.save_dir = save_dir
        self.server_socket = None
        self.running = False
        self.clients = []
        self.client_lock = threading.Lock()
        
        # Tạo thư mục lưu trữ báo cáo nếu chưa tồn tại
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logger.info(f"Đã tạo thư mục lưu trữ báo cáo: {save_dir}")
        
        # Thống kê
        self.stats = {
            "total_reports": 0,
            "total_clients": 0,
            "start_time": time.time()
        }
    
    def start(self):
        """Khởi động server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            logger.info(f"Server đang lắng nghe tại {self.host}:{self.port}")
            
            # Thread hiển thị thống kê
            stats_thread = threading.Thread(target=self._stats_display_loop)
            stats_thread.daemon = True
            stats_thread.start()
            
            while self.running:
                if len(self.clients) >= MAX_CLIENTS:
                    logger.warning("Số lượng client đã đạt giới hạn tối đa.")
                    time.sleep(1)
                    continue
                
                try:
                    client_socket, addr = self.server_socket.accept()
                    logger.info(f"Đã kết nối từ {addr[0]}:{addr[1]}")
                    
                    with self.client_lock:
                        self.clients.append(client_socket)
                        self.stats["total_clients"] += 1
                    
                    # Tạo thread xử lý client mới
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        logger.error(f"Lỗi khi chấp nhận kết nối: {e}")
                        
        except Exception as e:
            logger.error(f"Lỗi khi khởi động server: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Dừng server"""
        self.running = False
        
        # Đóng tất cả các kết nối client
        with self.client_lock:
            for client in self.clients:
                try:
                    client.close()
                except:
                    pass
            self.clients = []
        
        # Đóng server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        logger.info("Server đã dừng")
    
    def _handle_client(self, client_socket, address):
        """Xử lý kết nối từ client"""
        buffer = ""
        
        try:
            while self.running:
                # Nhận dữ liệu từ client
                data = client_socket.recv(4096)
                if not data:
                    logger.info(f"Client {address[0]}:{address[1]} đã ngắt kết nối")
                    break
                
                # Thêm dữ liệu vào buffer
                buffer += data.decode('utf-8')
                
                # Xử lý từng báo cáo (phân tách bằng ký tự xuống dòng)
                while '\n' in buffer:
                    # Lấy báo cáo đầu tiên
                    report_json, buffer = buffer.split('\n', 1)
                    
                    # Xử lý báo cáo
                    self._process_report(report_json, address)
        
        except Exception as e:
            logger.error(f"Lỗi khi xử lý client {address[0]}:{address[1]}: {e}")
        
        finally:
            # Đóng kết nối và xóa khỏi danh sách
            try:
                client_socket.close()
            except:
                pass
            
            with self.client_lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
    
    def _process_report(self, report_json, address):
        """Xử lý báo cáo bất thường từ client"""
        try:
            # Parse JSON
            report = json.loads(report_json)
            
            # In thông tin báo cáo
            flow_id = report["flow"]["id"]
            anomaly_score = report["anomaly"]["score"]
            flow_score = report["anomaly"]["flow_score"]
            
            logger.info(f"Báo cáo từ {address[0]}: {flow_id} - Score: {anomaly_score:.2f}, Flow Score: {flow_score}")
            
            # Lưu báo cáo vào file
            self._save_report(report)
            
            # Cập nhật thống kê
            self.stats["total_reports"] += 1
            
        except json.JSONDecodeError:
            logger.warning(f"Dữ liệu không hợp lệ từ {address[0]}: {report_json}")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý báo cáo từ {address[0]}: {e}")
    
    def _save_report(self, report):
        """Lưu báo cáo vào file"""
        try:
            # Tạo tên file dựa trên thời gian hiện tại
            now = datetime.now()
            date_dir = os.path.join(self.save_dir, now.strftime("%Y-%m-%d"))
            
            # Tạo thư mục theo ngày nếu chưa tồn tại
            os.makedirs(date_dir, exist_ok=True)
            
            # Tạo tên file
            flow_id = report["flow"]["id"].replace(":", "-").replace("/", "-")
            timestamp = now.strftime("%H%M%S")
            filename = f"{timestamp}_{flow_id}.json"
            
            # Lưu vào file
            file_path = os.path.join(date_dir, filename)
            with open(file_path, 'w') as f:
                json.dump(report, f, indent=2)
    
        except Exception as e:
            logger.error(f"Lỗi khi lưu báo cáo: {e}")
            # Lưu vào thư mục tạm thời
            temp_dir = "./temp_reports"
            os.makedirs(temp_dir, exist_ok=True)
            temp_file = os.path.join(temp_dir, f"failed_{timestamp}.json")
            with open(temp_file, 'w') as f:
                json.dump(report, f, indent=2)
            logger.warning(f"Báo cáo đã được lưu tạm thời tại: {temp_file}")
    
    def _stats_display_loop(self):
        """Thread hiển thị thống kê"""
        while self.running:
            try:
                # Tính thời gian chạy
                uptime = time.time() - self.stats["start_time"]
                hours, remainder = divmod(uptime, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                # Hiển thị thống kê
                with self.client_lock:
                    active_clients = len(self.clients)
                
                logger.info(f"Thống kê: Uptime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}, "
                           f"Clients: {active_clients}, Total Clients: {self.stats['total_clients']}, "
                           f"Reports: {self.stats['total_reports']}")
                
                # Cập nhật 30 giây một lần
                time.sleep(30)
            
            except Exception as e:
                logger.error(f"Lỗi khi hiển thị thống kê: {e}")
                time.sleep(60)  # Thử lại sau 1 phút nếu gặp lỗi

def main():
    # Parse tham số dòng lệnh
    parser = argparse.ArgumentParser(description='Server nhận báo cáo bất thường từ packet sniffer')
    parser.add_argument('-H', '--host', default='0.0.0.0', help='Địa chỉ lắng nghe (mặc định: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int, default=9999, help='Cổng lắng nghe (mặc định: 9999)')
    parser.add_argument('-d', '--dir', default='./anomaly_reports', help='Thư mục lưu báo cáo (mặc định: ./anomaly_reports)')
    args = parser.parse_args()
    
    # Khởi động server
    server = AnomalyServer(host=args.host, port=args.port, save_dir=args.dir)
    
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Đã nhận tín hiệu dừng từ người dùng")
    finally:
        server.stop()

if __name__ == "__main__":
    main()