#!/usr/bin/env python3
"""
Công cụ chuyển đổi báo cáo bất thường JSON thành file PCAP
để sử dụng với Suricata hoặc các công cụ phân tích mạng khác
"""

import os
import json
import argparse
import logging
import glob
from datetime import datetime
import struct
import socket
import dpkt
from dpkt.ethernet import Ethernet
from dpkt.ip import IP, IP_PROTO_TCP, IP_PROTO_UDP, IP_PROTO_ICMP
from dpkt.tcp import TCP
from dpkt.udp import UDP
from dpkt.icmp import ICMP
import random

# Define Ethernet types manually if not available
ETH_TYPE_IP = 0x0800
ETH_TYPE_IPV6 = 0x86DD

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JSON2PCAP")

class JSONtoPCAP:
    def __init__(self, output_file="reconstructed.pcap"):
        self.output_file = output_file
        self.pcap_writer = None
        
        # Mở file PCAP để ghi
        try:
            self.pcap_writer = dpkt.pcap.Writer(open(self.output_file, 'wb'))
            logger.info(f"Đã tạo file PCAP: {self.output_file}")
        except Exception as e:
            logger.error(f"Lỗi khi tạo file PCAP: {e}")
            raise
    
    def close(self):
        """Đóng file PCAP"""
        if self.pcap_writer:
            self.pcap_writer.close()
            logger.info(f"Đã đóng file PCAP: {self.output_file}")
    
    def convert_json_to_pcap(self, json_file):
        """Chuyển đổi một file JSON thành PCAP"""
        try:
            # Đọc file JSON
            with open(json_file, 'r') as f:
                report = json.load(f)
            
            # Tạo gói tin từ report
            packet = self._create_packet_from_report(report)
            
            # Lấy timestamp
            if 'flow' in report and 'start_time' in report['flow']:
                try:
                    timestamp = datetime.fromisoformat(report['flow']['start_time']).timestamp()
                except (ValueError, TypeError):
                    timestamp = datetime.now().timestamp()
            else:
                # Sử dụng thời gian hiện tại nếu không có
                timestamp = datetime.now().timestamp()
            
            # Ghi gói tin vào file PCAP
            if packet:
                self.pcap_writer.writepkt(packet, timestamp)
                logger.debug(f"Đã chuyển đổi {json_file} thành gói tin PCAP")
                return True
            else:
                logger.warning(f"Không thể tạo gói tin từ {json_file}")
                return False
            
        except Exception as e:
            logger.error(f"Lỗi khi chuyển đổi {json_file}: {e}")
            return False
    
    def _create_packet_from_report(self, report):
        """Tạo gói tin từ báo cáo JSON"""
        try:
            # Tạo Ethernet frame
            eth = Ethernet()
            eth.src = self._generate_mac_address()
            eth.dst = self._generate_mac_address()
            
            # Tạo IP packet
            ip_info = report.get("packet", {}).get("ip", {})
            if not ip_info:
                logger.warning("Không tìm thấy thông tin IP trong báo cáo")
                return None
            
            # Xác định phiên bản IP
            if ":" in ip_info.get("src", "") or ":" in ip_info.get("dst", ""):
                # IPv6
                # Không triển khai trong ví dụ này
                logger.warning("IPv6 chưa được hỗ trợ trong ví dụ này")
                return None
            
            # Tạo IPv4 packet
            ip = IP()
            
            # Thiết lập địa chỉ nguồn và đích
            try:
                ip.src = socket.inet_aton(ip_info.get("src", "0.0.0.0"))
                ip.dst = socket.inet_aton(ip_info.get("dst", "0.0.0.0"))
            except socket.error:
                logger.warning(f"Địa chỉ IP không hợp lệ: {ip_info.get('src')} hoặc {ip_info.get('dst')}")
                return None
            
            # Thiết lập các trường IP khác
            ip.ttl = ip_info.get("ttl", 64)
            ip.id = ip_info.get("id", random.randint(0, 65535))
            ip.p = ip_info.get("proto", 0)  # Protocol
            ip.df = ip_info.get("flags", {}).get("df", 0)
            ip.mf = ip_info.get("flags", {}).get("mf", 0)
            ip.offset = ip_info.get("frag_offset", 0)
            ip.tos = ip_info.get("tos", 0)
            
            # Tạo giao thức tầng transport dựa vào protocol
            if ip.p == IP_PROTO_TCP:
                # TCP
                tcp_info = report.get("packet", {}).get("tcp", {})
                if not tcp_info:
                    logger.warning("Không tìm thấy thông tin TCP trong báo cáo")
                    return None
                
                tcp = TCP()
                tcp.sport = tcp_info.get("sport", 0)
                tcp.dport = tcp_info.get("dport", 0)
                tcp.seq = tcp_info.get("seq", 0)
                tcp.ack = tcp_info.get("ack", 0)
                tcp.flags = 0
                
                # Thiết lập các cờ TCP
                flags_info = tcp_info.get("flags", {})
                if flags_info.get("fin", 0): tcp.flags |= dpkt.tcp.TH_FIN
                if flags_info.get("syn", 0): tcp.flags |= dpkt.tcp.TH_SYN
                if flags_info.get("rst", 0): tcp.flags |= dpkt.tcp.TH_RST
                if flags_info.get("psh", 0): tcp.flags |= dpkt.tcp.TH_PUSH
                if flags_info.get("ack", 0): tcp.flags |= dpkt.tcp.TH_ACK
                if flags_info.get("urg", 0): tcp.flags |= dpkt.tcp.TH_URG
                
                tcp.win = tcp_info.get("window", 8192)
                tcp.off = tcp_info.get("header_len", 20) // 4  # header length in 32-bit words
                
                # Tạo payload cho TCP
                payload = self._create_payload(report)
                tcp.data = payload
                
                ip.data = tcp
                
            elif ip.p == IP_PROTO_UDP:
                # UDP
                udp_info = report.get("packet", {}).get("udp", {})
                if not udp_info:
                    logger.warning("Không tìm thấy thông tin UDP trong báo cáo")
                    return None
                
                udp = UDP()
                udp.sport = udp_info.get("sport", 0)
                udp.dport = udp_info.get("dport", 0)
                
                # Tạo payload cho UDP
                payload = self._create_payload(report)
                udp.data = payload
                
                # UDP length được tính tự động
                
                ip.data = udp
                
            elif ip.p == IP_PROTO_ICMP:
                # ICMP
                icmp = ICMP()
                icmp.type = 8  # Echo request
                icmp.code = 0
                
                # Tạo payload cho ICMP
                payload = self._create_payload(report)
                icmp.data = payload
                
                ip.data = icmp
            
            else:
                # Protocol không được hỗ trợ
                logger.warning(f"Protocol {ip.p} chưa được hỗ trợ")
                return None
            
            # Gán IP packet vào Ethernet frame
            eth.type = ETH_TYPE_IP
            eth.data = ip
            
            return bytes(eth)
            
        except Exception as e:
            logger.error(f"Lỗi khi tạo gói tin: {e}")
            return None
    
    def _create_payload(self, report):
        """Tạo payload cho gói tin dựa trên thông tin ứng dụng"""
        proto_layer = report.get("proto_layer", {})
        proto_type = proto_layer.get("type", "unknown").lower()
        
        # Mặc định payload trống
        payload = b""
        
        # Dựa vào loại giao thức, tạo payload phù hợp
        if proto_type == "http":
            headers = proto_layer.get("headers", {})
            method = headers.get("method", "GET")
            uri = headers.get("uri", "/")
            version = headers.get("version", "HTTP/1.1")
            host = headers.get("host", "example.com")
            user_agent = headers.get("user_agent", "Mozilla/5.0")
            
            # Tạo HTTP request đơn giản
            http_req = f"{method} {uri} {version}\r\nHost: {host}\r\nUser-Agent: {user_agent}\r\n\r\n"
            payload = http_req.encode('utf-8')
            
        elif proto_type == "dns":
            # Tạo DNS query đơn giản
            payload = b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"
            
        elif proto_type == "ssh":
            # SSH banner đơn giản
            payload = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\r\n"
            
        elif proto_type == "ftp":
            # FTP command đơn giản
            payload = b"USER anonymous\r\n"
            
        elif proto_type == "smtp":
            # SMTP command đơn giản
            payload = b"EHLO example.com\r\n"
            
        else:
            # Tạo payload ngẫu nhiên cho các giao thức khác
            payload_len = random.randint(16, 64)
            payload = bytes([random.randint(32, 126) for _ in range(payload_len)])
        
        return payload
    
    def _generate_mac_address(self):
        """Tạo địa chỉ MAC ngẫu nhiên"""
        mac = [random.randint(0, 255) for _ in range(6)]
        # Đảm bảo không phải broadcast hoặc multicast
        mac[0] &= 0xFE  # Xóa bit multicast
        return bytes(mac)

def find_json_reports(reports_dir, recursive=True, date=None):
    """Tìm tất cả các file JSON báo cáo"""
    if date:
        search_dir = os.path.join(reports_dir, date)
        if not os.path.exists(search_dir):
            logger.error(f"Không tìm thấy thư mục cho ngày {date}")
            return []
    else:
        search_dir = reports_dir
    
    if recursive:
        pattern = os.path.join(search_dir, "**", "*.json")
        reports = glob.glob(pattern, recursive=True)
    else:
        pattern = os.path.join(search_dir, "*.json")
        reports = glob.glob(pattern)
    
    return reports

def main():
    parser = argparse.ArgumentParser(description="Chuyển đổi báo cáo bất thường JSON thành file PCAP")
    parser.add_argument('-d', '--dir', default='./anomaly_reports', help='Thư mục chứa báo cáo JSON (mặc định: ./anomaly_reports)')
    parser.add_argument('-o', '--output', default='reconstructed.pcap', help='Tên file PCAP đầu ra (mặc định: reconstructed.pcap)')
    parser.add_argument('--date', help='Chỉ xử lý báo cáo của ngày cụ thể (định dạng: YYYY-MM-DD)')
    parser.add_argument('--no-recursive', action='store_true', help='Không tìm kiếm đệ quy trong thư mục')
    parser.add_argument('--flow-id', help='Chỉ xử lý báo cáo của flow ID cụ thể')
    
    args = parser.parse_args()
    
    # Tìm các file JSON báo cáo
    json_files = find_json_reports(args.dir, not args.no_recursive, args.date)
    
    if not json_files:
        logger.error(f"Không tìm thấy file JSON báo cáo nào trong {args.dir}")
        return
    
    logger.info(f"Tìm thấy {len(json_files)} file báo cáo JSON")
    
    # Lọc theo flow_id nếu được chỉ định
    if args.flow_id:
        filtered_files = []
        for file in json_files:
            try:
                with open(file, 'r') as f:
                    report = json.load(f)
                    if report.get("flow", {}).get("id") == args.flow_id:
                        filtered_files.append(file)
            except:
                pass
        
        json_files = filtered_files
        logger.info(f"Sau khi lọc, còn lại {len(json_files)} file báo cáo với flow ID: {args.flow_id}")
    
    if not json_files:
        logger.error("Không còn file nào để xử lý sau khi lọc")
        return
    
    # Tạo converter
    try:
        converter = JSONtoPCAP(args.output)
        
        # Chuyển đổi từng file
        success_count = 0
        for file in json_files:
            if converter.convert_json_to_pcap(file):
                success_count += 1
                
        # Đóng file PCAP
        converter.close()
        
        logger.info(f"Đã chuyển đổi thành công {success_count}/{len(json_files)} file báo cáo")
        logger.info(f"File PCAP được lưu tại: {args.output}")
        
    except Exception as e:
        logger.error(f"Lỗi trong quá trình chuyển đổi: {e}")

if __name__ == "__main__":
    main()