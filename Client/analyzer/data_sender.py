import requests
import threading

class DataSender:
    def __init__(self, url="http://localhost:5001/api/add_packet"):
        self.url = url
        self.data_queue = []
        self.lock = threading.Lock()

    def add_data(self, packet_info, is_anomaly, anomaly_score, flow_score):
        """Thêm dữ liệu vào hàng đợi"""
        with self.lock:
            self.data_queue.append({
                "packet_info": packet_info,
                "is_anomaly": int(is_anomaly),
                "anomaly_score": float(anomaly_score),
                "flow_score": float(flow_score)
            })
        #print(f"[DEBUG] Đã thêm vào hàng đợi gửi: {packet_info['src_ip']}->{packet_info['dst_ip']}, is_anomaly={is_anomaly}, score={anomaly_score}")

    def send_data(self):
        """Gửi dữ liệu từ hàng đợi đến server"""
        with self.lock:
            if not self.data_queue:
                return
            
            data_to_send = self.data_queue[:]
            self.data_queue.clear()

        try:
            response = requests.post(self.url, json=data_to_send)
            if response.status_code == 200 or response.status_code == 201:
                print(f"[+] Gửi dữ liệu thành công: {response.json()}")
            else:
                print(f"[!] Lỗi khi gửi dữ liệu: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[!] Lỗi khi gửi dữ liệu đến dashboard: {e}")