# dh_utils.py
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import struct # Thêm import này
import logging

DH_PARAMETER_KEY_SIZE = 2048  # Kích thước bit cho tham số DH, ví dụ 2048 hoặc 3072

# Thiết lập logger cho module này
logger = logging.getLogger("dh_utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("dh_utils.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(file_handler)

def generate_dh_parameters() -> dh.DHParameters: # <--- ĐÂY LÀ HÀM BỊ THIẾU
    """Tạo tham số DH (p, g)."""
    return dh.generate_parameters(generator=2, key_size=DH_PARAMETER_KEY_SIZE, backend=default_backend())

def serialize_dh_parameters(parameters: dh.DHParameters) -> bytes:
    """Chuyển đổi tham số DH sang dạng PEM bytes."""
    return parameters.parameter_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.ParameterFormat.PKCS3
    )

def deserialize_dh_parameters(pem_bytes: bytes) -> dh.DHParameters:
    """Chuyển đổi PEM bytes sang đối tượng tham số DH."""
    try:
        params = serialization.load_pem_parameters(pem_bytes, backend=default_backend())
        logger.info("[DH_UTILS] Đã deserialize DH parameters thành công.")
        return params
    except Exception as e:
        logger.error(f"[DH_UTILS][ERROR] Lỗi khi deserialize DH parameters: {e}")
        raise

def generate_dh_private_key(parameters: dh.DHParameters) -> dh.DHPrivateKey:
    """Tạo khóa riêng DH từ các tham số đã cho."""
    return parameters.generate_private_key()

def serialize_dh_public_key(public_key: dh.DHPublicKey) -> bytes:
    """Chuyển đổi khóa công khai DH sang dạng PEM bytes."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_dh_public_key(key_bytes: bytes) -> dh.DHPublicKey:
    """Chuyển đổi PEM bytes sang đối tượng khóa công khai DH."""
    try:
        pubkey = serialization.load_pem_public_key(key_bytes, backend=default_backend())
        logger.info("[DH_UTILS] Đã deserialize DH public key thành công.")
        return pubkey
    except Exception as e:
        logger.error(f"[DH_UTILS][ERROR] Lỗi khi deserialize DH public key: {e}")
        raise

def derive_aes_key_from_shared(shared_secret: bytes, key_length_bytes: int = 32) -> bytes:
    """
    Dẫn xuất khóa AES từ shared secret của DH bằng HKDF.
    key_length_bytes: 16 (AES-128), 24 (AES-192), 32 (AES-256).
    """
    try:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=key_length_bytes,
            salt=None,
            info=b'anomaly_reporter_aes_key', 
            backend=default_backend()
        )
        key = hkdf.derive(shared_secret)
        logger.info("[DH_UTILS] Đã derive AES key từ shared secret thành công.")
        return key
    except Exception as e:
        logger.error(f"[DH_UTILS][ERROR] Lỗi khi derive AES key: {e}")
        raise

def send_message_dh(sock, data_bytes: bytes):
    """Gửi độ dài của message (4-byte big-endian int) sau đó là message."""
    msg_len = len(data_bytes)
    len_prefix = struct.pack('>I', msg_len) # Gói độ dài thành 4 bytes, big-endian
    try:
        sock.sendall(len_prefix)
        sock.sendall(data_bytes)
    except sock.error as e:
        # Ghi log hoặc raise một exception cụ thể hơn nếu cần
        raise ConnectionAbortedError(f"Lỗi socket khi gửi message DH: {e}")


def recv_message_dh(sock) -> bytes:
    """Nhận message bằng cách đọc độ dài trước (4-byte big-endian int)."""
    try:
        # Đọc 4 byte đầu tiên để lấy độ dài
        len_prefix = sock.recv(4)
        if not len_prefix or len(len_prefix) < 4:
            # Nếu không nhận đủ 4 byte, có thể kết nối đã đóng hoặc có vấn đề
            raise ConnectionAbortedError("Kết nối đóng hoặc không nhận đủ prefix độ dài message DH.")
        
        msg_len = struct.unpack('>I', len_prefix)[0]
        
        # Giới hạn kích thước message hợp lý để tránh tấn công DoS bằng cách gửi độ dài lớn
        if msg_len > 10 * 1024 * 1024: # Ví dụ: giới hạn 10MB
            raise ValueError(f"Message quá lớn: {msg_len} bytes.")

        # Nhận toàn bộ message dựa trên độ dài đã đọc
        chunks = []
        bytes_recd = 0
        while bytes_recd < msg_len:
            # Đọc phần còn lại, hoặc tối đa 4096 bytes một lần
            chunk = sock.recv(min(msg_len - bytes_recd, 4096)) 
            if not chunk:
                raise ConnectionAbortedError("Kết nối đóng trước khi nhận toàn bộ message DH.")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        
        return b"".join(chunks)
    except sock.error as e:
        raise ConnectionAbortedError(f"Lỗi socket khi nhận message DH: {e}")
    except struct.error as e:
        raise ValueError(f"Lỗi giải nén prefix độ dài message DH: {e}")