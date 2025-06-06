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
from datetime import datetime, timezone, date
import psycopg2 
import uuid
from dotenv import load_dotenv
from psycopg2.extras import Json
from json2pcap import JSONtoPCAP
from suricata_analyzer import SuricataAnalyzer, parse_eve_json
from cryptography.hazmat.primitives.asymmetric import dh
from crypto_util import CryptoUtil
from dh_utils import (
    serialize_dh_parameters,
    generate_dh_private_key,
    serialize_dh_public_key,
    deserialize_dh_public_key,
    derive_aes_key_from_shared,
    generate_dh_parameters,
    send_message_dh,
    recv_message_dh
)


# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AnomalyServer")
suricata_integration_logger = logging.getLogger("SuricataIntegration")
SURICATA_ALERT_BLOCK_SEVERITY_THRESHOLD=2
HIGH_SEVERITY_ANOMALY_SCORE_THRESHOLD = 0.8



class AnomalyServer:
    def __init__(self, host="0.0.0.0", port=9999, save_dir=None, suricata_bin="suricata", suricata_config=None, suricata_rules_dir=None):
        load_dotenv()
        self.host = host
        self.port = port
        if save_dir is None:
            base_dir = os.path.dirname(os.path.realpath(__file__))
            save_dir = os.path.join(base_dir, "anomaly_reports")


        # Tham số DH toàn cục của Server 
        self.SERVER_DH_PARAMETERS: dh.DHParameters = None
        self.SERVER_DH_PARAMETERS_PEM: bytes = None


        self.save_dir = save_dir
        self.json_subdir_name = "json_files"
        self.pcap_subdir_name = "pcap_files"
        self.suricata_output_subdir_name = "suricata_output"

        self.server_socket = None
        self.running = False
        self.clients = []
        self.client_lock = threading.Lock()

        self.suricata_bin = suricata_bin
        self.suricata_config = suricata_config
        self.suricata_rules_dir = suricata_rules_dir
        self.suricata_analyzer_instance = None 

        # Tạo thư mục lưu trữ báo cáo nếu chưa tồn tại
        if not os.path.exists(self.save_dir):
            os.makedirs(save_dir)
            logger.info(f"Đã tạo thư mục lưu trữ báo cáo: {save_dir}")
        
        # Thống kê
        self.stats = {
            "TOTAL_REPORTS": 0,
            "total_clients": 0,
            "start_time": time.time(),
            "suricata_alerts_found": 0,
            "block_commands_sent": 0,  
        }
        
        self._connect_db()

        try:    
            if self.suricata_bin: # Chỉ khởi tạo nếu suricata_bin được cung cấp
                self.suricata_analyzer_instance = SuricataAnalyzer(
                    suricata_bin=self.suricata_bin,
                    config_file=self.suricata_config,
                    rules_dir=self.suricata_rules_dir
                )

        except Exception as e:
            suricata_integration_logger.error(f"Không thể khởi tạo SuricataAnalyzer: {e}. Phân tích Suricata sẽ bị bỏ qua.")
            self.suricata_analyzer_instance = None

        self._initialize_global_dh_parameters_server()
        

    def _initialize_global_dh_parameters_server(self): 
        # global self.SERVER_DH_PARAMETERS, self.SERVER_DH_PARAMETERS_PEM
        if self.SERVER_DH_PARAMETERS is None:
            logger.info("Đang tạo tham số DH toàn cục cho server... (có thể mất vài giây)")
            self.SERVER_DH_PARAMETERS = generate_dh_parameters() # Sử dụng hàm từ dh_utils
            self.SERVER_DH_PARAMETERS_PEM = serialize_dh_parameters(self.SERVER_DH_PARAMETERS)
            logger.info("Đã tạo và serialize tham số DH toàn cục.")


    def _connect_db(self):
        
        self.db_conn = None
        try:
            self.db_conn = psycopg2.connect(
                host=os.environ.get('DBHOST'),
                port=int(os.environ.get('DBPORT')),
                dbname=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD')
            )
            self.db_conn.autocommit = True
            logger.info("Đã kết nối tới database")
        except Exception as e:
            logger.error(f"Lỗi khi kết nối database: {e}")

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

    def _perform_dh_key_exchange_for_client(self, client_socket, client_address_str) -> CryptoUtil:
            """Thực hiện trao đổi khóa DH với client và trả về CryptoUtil nếu thành công."""

            logger.info(f"[{client_address_str}] Bắt đầu trao đổi khóa Diffie-Hellman.")
            
            try:
                # 1. Server tạo cặp khóa DH (private/public) cho phiên này
                server_session_private_key = generate_dh_private_key(self.SERVER_DH_PARAMETERS)
                server_session_public_key = server_session_private_key.public_key()
                server_session_public_key_pem = serialize_dh_public_key(server_session_public_key)

                # 2. Server gửi tham số DH (PEM) và khóa công khai của mình (PEM) cho client
                # logger.debug(f"[{client_address_str}] Gửi tham số DH...")
                send_message_dh(client_socket, self.SERVER_DH_PARAMETERS_PEM)
                
                # logger.debug(f"[{client_address_str}] Gửi khóa công khai server...")
                send_message_dh(client_socket, server_session_public_key_pem)
                
                # 3. Server nhận khóa công khai của client
                # logger.debug(f"[{client_address_str}] Chờ khóa công khai của client...")
                client_public_key_pem = recv_message_dh(client_socket)
                client_dh_public_key = deserialize_dh_public_key(client_public_key_pem) # Server deserializes client's public key
                # logger.debug(f"[{client_address_str}] Đã nhận khóa công khai của client.")

                # 4. Server tính toán shared secret
                shared_secret_bytes = server_session_private_key.exchange(client_dh_public_key)
                
                # 5. Dẫn xuất khóa AES và khởi tạo CryptoUtil cho phiên này
                aes_key_session = derive_aes_key_from_shared(shared_secret_bytes, key_length_bytes=32)
                crypto_for_session = CryptoUtil(aes_key_session)
                
                logger.info(f"[{client_address_str}] Trao đổi khóa DH thành công. Khóa AES đã được dẫn xuất.")
                return crypto_for_session
            
            except (socket.timeout, ConnectionAbortedError, ValueError) as e_dh_exchange:
                logger.error(f"[{client_address_str}] Lỗi trong quá trình trao đổi DH: {e_dh_exchange}")
                return None
            except Exception as e_crypto: # Lỗi từ thư viện cryptography
                logger.error(f"[{client_address_str}] Lỗi crypto trong quá trình DH: {e_crypto}", exc_info=True)
                return None
    

    
    def _handle_client(self, client_socket, address):
        """Xử lý kết nối từ client"""

        client_address_str = f"{address[0]}:{address[1]}"
        logger.info(f"Đã chấp nhận kết nối từ {client_address_str}")
        
        crypto_for_session: CryptoUtil = None
        
        client_socket.settimeout(30) # Đặt timeout cho các bước trao đổi khóa DH
        crypto_for_session = self._perform_dh_key_exchange_for_client(client_socket, client_address_str)
        
        if not crypto_for_session:
            logger.error(f"[{client_address_str}] Trao đổi khóa DH thất bại. Đóng kết nối.")
            return # Thoát thread, finally sẽ đóng socket

        client_socket.settimeout(None) # Reset timeout cho hoạt động nhận dữ liệu bình thường
        logger.info(f"[{client_address_str}] Sẵn sàng nhận dữ liệu báo cáo mã hóa.")


        buffer = b""
        
        try:
            while self.running:
                # Nhận dữ liệu từ client
                data = client_socket.recv(4096)
                if not data:
                    logger.info(f"Client {address[0]}:{address[1]} đã ngắt kết nối")
                    break
                
                # Thêm dữ liệu vào buffer
                buffer += data
                
                # Xử lý từng báo cáo (phân tách bằng ký tự xuống dòng)
                while b'\n' in buffer:
                    # Lấy báo cáo đầu tiên
                    encrypted_report_part, buffer = buffer.split(b'\n', 1)
                    encrypted_report_str = encrypted_report_part.decode('utf-8').strip()

                    report_json = crypto_for_session.decrypt(encrypted_report_str)

                    # Xử lý báo cáo
                    self._process_report(report_json, client_socket, address)

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
    
    def _convert_report_to_pcap(self, json_report_path):
        """Chuyển đổi file JSON báo cáo đã lưu thành file PCAP."""
        if not json_report_path:
            logger.warning("Đường dẫn file JSON không hợp lệ, bỏ qua chuyển đổi PCAP.")
            return None

        try:
            json_dir = os.path.dirname(json_report_path)
            date_level_dir = os.path.dirname(json_dir)
            pcap_dir = os.path.join(date_level_dir, self.pcap_subdir_name)

            if not os.path.exists(pcap_dir):
                os.makedirs(pcap_dir)
                # logger.info(f"Đã tạo thư mục PCAP: {pcap_dir}")


            # Tạo tên file PCAP dựa trên file JSON
            base_pcap_filename = os.path.splitext(os.path.basename(json_report_path))[0] + ".pcap"
            pcap_output_path = os.path.join(pcap_dir, base_pcap_filename)
            
            # Sử dụng JSONtoPCAP
            converter = JSONtoPCAP(output_file=pcap_output_path)
            success = converter.convert_json_to_pcap(json_report_path)
            converter.close() 

            if success:
                # logger.info(f"Đã chuyển đổi thành công {json_report_path} thành {pcap_output_path}")
                return pcap_output_path 
            else:
                # logger.warning(f"Không thể chuyển đổi {json_report_path} thành PCAP.")
                return None 
        except Exception as e:
            logger.error(f"Lỗi trong quá trình chuyển đổi JSON sang PCAP cho file {json_report_path}: {e}", exc_info=True)
            return None 
        

    def _analyze_pcap_with_suricata(self, pcap_file_path, original_client_socket, associated_flow_id="N/A"):
            """Phân tích file PCAP bằng Suricata và xử lý kết quả."""
            if not self.suricata_analyzer_instance:
                suricata_integration_logger.warning(f"Suricata Analyzer chưa được khởi tạo. Bỏ qua phân tích PCAP: {pcap_file_path}")
                return None
            if not pcap_file_path or not os.path.exists(pcap_file_path):
                suricata_integration_logger.error(f"File PCAP không tồn tại hoặc đường dẫn không hợp lệ: {pcap_file_path}")
                return None

            # suricata_integration_logger.info(f"Bắt đầu phân tích Suricata cho PCAP: {pcap_file_path} (Flow: {associated_flow_id})")
            try:
                # Tạo thư mục output cho Suricata bên cạnh thư mục pcap_files
                pcap_dir = os.path.dirname(pcap_file_path) # Ví dụ: .../anomaly_reports/YYYY-MM-DD/pcap_files
                date_dir = os.path.dirname(pcap_dir)      # Ví dụ: .../anomaly_reports/YYYY-MM-DD
                
                # Tạo tên thư mục output dựa trên tên file PCAP để tránh trùng lặp
                pcap_basename = os.path.splitext(os.path.basename(pcap_file_path))[0]
                suricata_run_output_dir = os.path.join(date_dir, self.suricata_output_subdir_name, pcap_basename)
                os.makedirs(suricata_run_output_dir, exist_ok=True)

                eve_json_path = self.suricata_analyzer_instance.analyze_pcap(pcap_file_path, output_dir=suricata_run_output_dir)

                if eve_json_path and os.path.exists(eve_json_path):
                    # suricata_integration_logger.info(f"Phân tích Suricata hoàn tất. Kết quả EVE JSON tại: {eve_json_path}")
                    alerts = parse_eve_json(eve_json_path) # Sử dụng hàm parse từ suricata_analyzer.py
                    if alerts:
                        suricata_integration_logger.info(f"Tìm thấy {len(alerts)} cảnh báo Suricata cho PCAP: {pcap_file_path}")
                        
                        # Xử lý gửi lệnh block
                        ips_to_block_this_session = set() # Tránh gửi lệnh block trùng lặp cho cùng 1 IP từ 1 pcap
                        for alert_detail in alerts:
                            alert_severity = alert_detail.get("alert", {}).get("severity", 0)
                            if alert_severity >= SURICATA_ALERT_BLOCK_SEVERITY_THRESHOLD:
                                src_ip_to_block = alert_detail.get("src_ip")
                                if src_ip_to_block and src_ip_to_block not in ips_to_block_this_session:
                                    suricata_integration_logger.warning(
                                        f"Cảnh báo Suricata nguy hiểm (Severity: {alert_severity}) từ IP: {src_ip_to_block}. "
                                        f"Signature: {alert_detail.get('alert', {}).get('signature', 'N/A')}. "
                                        f"Gửi lệnh block cho agent."
                                    )
                                    # Kiểm tra socket trước khi gửi (cách tiếp cận đơn giản)
                                    if original_client_socket and original_client_socket.fileno() != -1:
                                        self._send_block_command(original_client_socket, src_ip_to_block)
                                        ips_to_block_this_session.add(src_ip_to_block)
                                        self.stats["block_commands_sent"] +=1
                                    else:
                                        suricata_integration_logger.warning(f"Client socket cho FlowID {associated_flow_id} dường như đã đóng. Không thể gửi lệnh block cho IP {src_ip_to_block}.")
                            
                    else:
                        None
                        # suricata_integration_logger.info(f"Không tìm thấy cảnh báo Suricata nào cho PCAP: {pcap_file_path} (Flow: {associated_flow_id})")
                    return eve_json_path
                else:
                    suricata_integration_logger.error(f"Phân tích Suricata cho {pcap_file_path} không tạo ra file eve.json hoặc file không tồn tại.")
                    return None
            except Exception as e:
                suricata_integration_logger.error(f"Lỗi trong quá trình phân tích Suricata cho PCAP {pcap_file_path}: {e}", exc_info=True)
                return None
        

    def _process_report(self, report_json, client_socket, address):
        """Xử lý báo cáo bất thường từ client"""
        try:
            # Parse JSON
            report = json.loads(report_json)

            # In thông tin báo cáo
            flow_id = report["flow"]["id"]
            anomaly_score = report["anomaly"]["score"]
            flow_score = report["anomaly"]["flow_score"]

            # Xác định protocol
            try:  
                ip_proto = report['packet']['ip']['proto']

                if ip_proto == 6 and 'tcp' in report['packet']:
                    proto = "TCP"
                elif ip_proto == 17 and 'udp' in report['packet']:
                    proto = "UDP"
                else:
                    proto = "ICMP"
                # report[]
                logger.info(f"Báo cáo từ {address[0]}: {flow_id} - Score: {anomaly_score:.2f}, Flow Score: {flow_score}")
            except KeyError:
                logger.warning(f"Không tìm thấy thông tin protocol trong báo cáo {flow_id}")

            # 1.Lưu báo cáo vào file
            abs_path = self._save_report(report)
            
            # 2. Chuyển đổi sang PCAP
            created_pcap_path  = self._convert_report_to_pcap(abs_path)
            
            # 3. Phân tích PCAP bằng Suricata 
            if created_pcap_path:
                # Chạy Suricata trong một thread riêng để không block _process_report
                # Điều này quan trọng nếu Suricata mất nhiều thời gian để chạy
                suricata_thread = threading.Thread(
                    target=self._analyze_pcap_with_suricata,
                    args=(created_pcap_path, client_socket, flow_id)
                )
                suricata_thread.daemon = True # Cho phép chương trình chính thoát ngay cả khi thread này đang chạy
                suricata_thread.start()


            self._save_report_to_db(report)

            # Cập nhật thống kê
            self.stats["TOTAL_REPORTS"] += 1
            
        except Exception as e:
            logger.error(f"Lỗi khi xử lý báo cáo từ {address[0]}: {e}")
    
    def _save_report(self, report):
        """Lưu báo cáo vào file"""
        try:
            # Tạo tên file dựa trên thời gian hiện tại
            now = datetime.now()
            date_dir = os.path.join(self.save_dir, now.strftime("%Y-%m-%d"))
            
            # Tạo thư mục theo ngày nếu chưa tồn tại
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)

            # Tạo tên file
            flow_id = report["flow"]["id"].replace(":", "-").replace("/", "-")
            timestamp = now.strftime("%H%M%S")
            filename = f"{timestamp}_{flow_id}.json"


            json_files_dir = os.path.join(date_dir, self.json_subdir_name)
            os.makedirs(json_files_dir, exist_ok=True)
            
            # Lưu vào file
            file_path = os.path.join(json_files_dir, filename)
            with open(file_path, 'w') as f:
                json.dump(report, f, indent=2)
            abs_path = os.path.abspath(file_path)
            logger.info(f"Đã lưu báo cáo vào file: {file_path}")
            return abs_path
            
        except Exception as e:
            logger.error(f"Lỗi khi lưu báo cáo: {e}")
            return None
    

    def _save_report_to_db(self, report):
        agent = report.get("agent", {})
        flow = report.get("flow", {})
        packet = report.get("packet", {})
        ip_layer = packet.get("ip", {})
        proto_num = ip_layer.get("proto")

        protocol_map = {6: "tcp", 17: "udp", 1: "icmp"}
        protocol = protocol_map.get(proto_num, "unknown")

        sport = None
        dport = None

        # lấy sport, dport và packet_size
        if protocol == "tcp" and "tcp" in packet:
            sport = packet["tcp"].get("sport")
            dport = packet["tcp"].get("dport")
            packet_size = packet["tcp"].get("header_len", 0)
        elif protocol == "udp" and "udp" in packet:
            sport = packet["udp"].get("sport")
            dport = packet["udp"].get("dport")
            packet_size = packet["udp"].get("length", 0)
        else:
            packet_size = 0  # fallback

        conn = self.db_conn
        cur = conn.cursor()

        try:
            # ====== 1. Insert/Update CLIENTS ======
            agent_id = agent.get("id")
            hostname = agent.get("hostname")
            os = agent.get("os")
            last_seen = datetime.now(timezone.utc)
            agent_ip_addr = agent.get("agent_ip_addr")
            

            cur.execute("""
                INSERT INTO "CLIENTS" ("ID", "HOSTNAME", "IP_ADDRESS", "OS", "STATUS", "LAST_SEEN")
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT ("ID") DO UPDATE SET
                "HOSTNAME" = EXCLUDED."HOSTNAME",
                "OS" = EXCLUDED."OS",
                "STATUS" = EXCLUDED."STATUS",
                "IP_ADDRESS" = EXCLUDED."IP_ADDRESS",
                "LAST_SEEN" = EXCLUDED."LAST_SEEN"
            """, (agent_id, hostname, agent_ip_addr, os, "active", last_seen))

            # ====== 2. Insert PACKETS ======
            packet_id = str(uuid.uuid4())
            timestamp = datetime.fromisoformat(flow["start_time"])
            source_ip = ip_layer.get("src")
            dest_ip = ip_layer.get("dst")
            source_port = sport
            dest_port = dport

            cur.execute("""
                INSERT INTO "PACKETS" ("ID", "TIMESTAMP",  "PROTOCOL", "SOURCE_IP", "DEST_IP", "SOURCE_PORT", "DEST_PORT", "AGENT_ID")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (packet_id, timestamp, protocol, source_ip, dest_ip, source_port, dest_port, agent_id))

            # ====== 3. Insert anomaly_reports ======
            anomaly_data = report.get("anomaly", {})
            proto_layer = report.get("proto_layer", {})
            app_protocol = proto_layer.get("type", "unknown")

            packet_count = flow.get("packet_count", 0)
            anomaly_score = anomaly_data.get("score")
            flow_score = anomaly_data.get("flow_score")
            detection_method = anomaly_data.get("detection_method")
            flow_id = flow.get("id")
            processed_time=anomaly_data.get("start_time")
            client_ip = agent_ip_addr
            cur.execute("""
                INSERT INTO "ANOMALY_REPORTS" (
                    "TIMESTAMP", "CLIENT_IP", "FLOW_ID",
                    "SRC_IP", "SRC_PORT", "DST_IP", "DST_PORT",
                    "PROTOCOL", "APP_PROTOCOL",
                    "PACKET_SIZE", "PACKET_COUNT",
                    "ANOMALY_SCORE", "FLOW_SCORE",
                    "DETECTION_METHOD", "IS_PROCESSED",
                    "PROCESSED_AT", "RAW_DATA"
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                timestamp,
                client_ip,
                flow_id,
                source_ip,
                source_port,
                dest_ip,
                dest_port,
                protocol,
                app_protocol,
                packet_size,
                packet_count,
                anomaly_score,
                flow_score,
                detection_method,
                True,
                processed_time,
                Json(report)
            ))


            # ====== 4. Commit and optionally block source IP ======
            
            update_query = """
                UPDATE "CLIENTS"
                SET "STATUS" = 'inactive'
                WHERE "LAST_SEEN" < NOW() - INTERVAL '5 minutes'
                AND "STATUS" != 'inactive'
            """
            cur.execute(update_query)

            # ====== 5. Cập nhật DAILY_STATISTICS ======

            current_date_db = date.today()
            is_actual_anomaly = 1 if anomaly_data.get("detection_method") else 0 
            high_severity = 1 if (anomaly_score is not None and anomaly_score >= HIGH_SEVERITY_ANOMALY_SCORE_THRESHOLD) else 0

            initial_top_protocols_json_str = json.dumps({protocol: 1})
            initial_top_flow_ids_json_str = json.dumps({flow_id: 1})

            sql_daily_stats = """
                INSERT INTO "DAILY_STATISTICS" ( 
                    "DATE", "TOTAL_REPORTS", "ANOMALY_COUNT", "HIGH_SEVERITY_COUNT", 
                    "TOP_PROTOCOLS", "TOP_FLOW_IDS"
                )
                VALUES (%(current_date)s, 1, %(anomaly_inc)s, %(high_sev_inc)s, %(init_proto_json)s::jsonb, %(init_flow_json)s::jsonb)
                ON CONFLICT ("DATE") DO UPDATE SET
                    "TOTAL_REPORTS" = "DAILY_STATISTICS"."TOTAL_REPORTS" + 1,
                    "ANOMALY_COUNT" = "DAILY_STATISTICS"."ANOMALY_COUNT" + EXCLUDED."ANOMALY_COUNT",
                    "HIGH_SEVERITY_COUNT" = "DAILY_STATISTICS"."HIGH_SEVERITY_COUNT" + EXCLUDED."HIGH_SEVERITY_COUNT",
                    "TOP_PROTOCOLS" = jsonb_set(
                        COALESCE("DAILY_STATISTICS"."TOP_PROTOCOLS", '{}'::jsonb),
                        ARRAY[%(proto_key)s],
                        to_jsonb((COALESCE(("DAILY_STATISTICS"."TOP_PROTOCOLS"->>%(proto_key)s)::int, 0) + 1)),
                        true 
                    ),
                    "TOP_FLOW_IDS" = jsonb_set(
                        COALESCE("DAILY_STATISTICS"."TOP_FLOW_IDS", '{}'::jsonb),
                        ARRAY[%(flow_key)s],
                        to_jsonb((COALESCE(("DAILY_STATISTICS"."TOP_FLOW_IDS"->>%(flow_key)s)::int, 0) + 1)),
                        true 
                    );
            """
            params_daily_stats = {
                "current_date": current_date_db,
                "anomaly_inc": is_actual_anomaly,
                "high_sev_inc": high_severity,
                "init_proto_json": initial_top_protocols_json_str,
                "init_flow_json": initial_top_flow_ids_json_str,
                "proto_key": protocol, 
                "flow_key": flow_id  
            }
            cur.execute(sql_daily_stats, params_daily_stats)
            
            
        except Exception as e:
            conn.rollback()
            print(f"Error saving report: {e}")
        finally:
            cur.close()


    
    # Cơ chế soft-block
    def _send_block_command(self, client_socket, ip_to_block):
        """Gửi lệnh block IP cho client"""
        try:
            command = {
                "action": "block_ip",
                "ip": ip_to_block,
                "reason": "Detected anomaly from this IP"
            }
            msg = json.dumps(command) + "\n"

            client_socket.sendall(msg.encode())
            logger.info(f"Đã gửi lệnh block IP {ip_to_block} cho client")
        except Exception as e:
            logger.error(f"Lỗi khi gửi lệnh block IP: {e}")



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
                           f"Reports: {self.stats['TOTAL_REPORTS']}")
                
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