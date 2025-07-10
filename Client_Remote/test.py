# test.py (phiên bản đã sửa lỗi)

import socket
import json
from dh_utils import (
    deserialize_dh_parameters,
    generate_dh_private_key,
    serialize_dh_public_key,
    deserialize_dh_public_key,
    derive_aes_key_from_shared,
    send_message_dh,
    recv_message_dh
)
from crypto_util import CryptoUtil

# --- THÔNG TIN SERVER ---
# Thay thế bằng IP public của Droplet của bạn
SERVER_HOST = '24.144.118.38' 
SERVER_PORT = 9999

def perform_dh_key_exchange(sock) -> CryptoUtil:
    """Thực hiện trao đổi khóa DH với server và trả về CryptoUtil."""
    try:
        print("[Client] Bắt đầu trao đổi khóa Diffie-Hellman...")

        # 1. Nhận tham số DH từ server
        server_dh_params_pem = recv_message_dh(sock)
        server_dh_parameters = deserialize_dh_parameters(server_dh_params_pem)
        print("[Client] Đã nhận tham số DH.")

        # 2. Nhận khóa công khai của server
        server_public_key_pem = recv_message_dh(sock)
        server_dh_public_key = deserialize_dh_public_key(server_public_key_pem)
        print("[Client] Đã nhận khóa công khai của server.")

        # 3. Client tạo cặp khóa của riêng mình dựa trên tham số của server
        client_private_key = generate_dh_private_key(server_dh_parameters)
        client_public_key = client_private_key.public_key()
        client_public_key_pem = serialize_dh_public_key(client_public_key)

        # 4. Gửi khóa công khai của client cho server
        send_message_dh(sock, client_public_key_pem)
        print("[Client] Đã gửi khóa công khai của mình.")

        # 5. Tính toán shared secret và dẫn xuất khóa AES
        shared_secret = client_private_key.exchange(server_dh_public_key)
        aes_key = derive_aes_key_from_shared(shared_secret, key_length_bytes=32)
        
        print("[Client] Trao đổi khóa thành công. Khóa AES đã được tạo.")
        return CryptoUtil(aes_key)

    except Exception as e:
        print(f"[Client] Lỗi trong quá trình trao đổi khóa: {e}")
        return None

def main():
    # Tạo một kết nối TCP thông thường, KHÔNG dùng SSL
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print(f"Đang kết nối tới {SERVER_HOST}:{SERVER_PORT}...")
            sock.connect((SERVER_HOST, SERVER_PORT))
            print("Kết nối thành công!")

            # Thực hiện trao đổi khóa để có được crypto_util
            crypto_util = perform_dh_key_exchange(sock)

            if not crypto_util:
                print("Không thể thiết lập kênh an toàn. Thoát.")
                return

            # Bây giờ bạn đã có một kênh an toàn.
            # Hãy tạo một báo cáo mẫu để gửi đi.
            report_data = {
                "agent": {"id": "agent-001", "hostname": "client-machine"},
                "flow": {"id": "192.168.1.10-12345", "start_time": "2024-01-01T12:00:00"},
                "packet": {"ip": {"src": "192.168.1.10", "dst": "8.8.8.8", "proto": 6}, "tcp": {"sport": 12345, "dport": 53}},
                "anomaly": {"score": 0.95, "flow_score": "High", "detection_method": "ML Model"}
            }
            report_json_str = json.dumps(report_data)

            # Mã hóa báo cáo
            encrypted_report = crypto_util.encrypt(report_json_str)

            # Gửi dữ liệu đã mã hóa (nhớ thêm dấu xuống dòng như server đang mong đợi)
            print("Đang gửi báo cáo đã mã hóa...")
            sock.sendall(encrypted_report.encode('utf-8') + b'\n')
            print("Đã gửi báo cáo.")

            # (Tùy chọn) Chờ nhận lệnh từ server (ví dụ: lệnh block)
            # while True:
            #     response = sock.recv(4096)
            #     if not response:
            #         break
            #     print(f"Nhận được từ server: {response.decode()}")

        except ConnectionRefusedError:
            print("Kết nối bị từ chối. Server có đang chạy không?")
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
        finally:
            print("Đóng kết nối.")

if __name__ == "__main__":
    main()