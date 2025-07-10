# Cấu hình mặc định
DEFAULT_INTERFACE = "wlp45s0"
DEFAULT_OUTPUT_DIR = "./captures"
DEFAULT_MODEL_PATH = "./model/anomaly_model.pkl"
MAX_PCAP_SIZE = 100 * 1024 * 1024  # 100MB

# Tùy chọn hiển thị
TABLE_UPDATE_INTERVAL = 5  # Cập nhật bảng sau mỗi 5 gói tin
MODEL_UPDATE_INTERVAL = 100  # Cập nhật mô hình sau mỗi 100 gói tin
FLOW_ALERT_THRESHOLD = 1  # Ngưỡng cảnh báo luồng bất thường

# Cấu hình server báo cáo bất thường
ANOMALY_REPORT_ENABLED = True
ANOMALY_REPORT_SERVER = "24.144.118.38"
ANOMALY_REPORT_PORT = 9999
ANOMALY_REPORT_RETRY = 5  # Seconds between reconnection attempts
ANOMALY_REPORT_QUEUE_SIZE = 1000  # Maximum number of reports in queue

# Ngưỡng phát hiện bất thường
ANOMALY_THRESHOLD = -0.5  # Ngưỡng điểm bất thường (thấp hơn = bất thường)
FLOW_SCORE_THRESHOLD = 3  # Ngưỡng điểm luồng để báo cáo

SENDER_EMAIL = "your_gmail_address@gmail.com"
