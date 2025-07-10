# crypto_util.py
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class CryptoUtil:
    def __init__(self, key: bytes):
        """
        Khởi tạo CryptoUtil với một khóa AES.
        Key phải dài 16 bytes (AES-128), 24 bytes (AES-192), hoặc 32 bytes (AES-256).
        """
        if len(key) not in [16, 24, 32]:
            raise ValueError("Khóa AES phải dài 16, 24, hoặc 32 bytes.")
        self.key = key
        self.backend = default_backend()
        self.iv_size = algorithms.AES.block_size // 8  # 16 bytes for AES

    def encrypt(self, plaintext: str) -> str:
        """
        Mã hóa một chuỗi plaintext.
        Trả về một chuỗi base64 chứa (IV + ciphertext).
        """
        plaintext_bytes = plaintext.encode('utf-8')
        iv = os.urandom(self.iv_size) # Tạo IV ngẫu nhiên

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # PKCS7 padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext_bytes) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Prepend IV to ciphertext and then base64 encode
        return base64.b64encode(iv + ciphertext).decode('utf-8')

    def decrypt(self, b64_encrypted_data: str) -> str:
        """
        Giải mã một chuỗi base64 (IV + ciphertext).
        Trả về chuỗi plaintext gốc.
        """
        encrypted_data_bytes = base64.b64decode(b64_encrypted_data.encode('utf-8'))
        
        iv = encrypted_data_bytes[:self.iv_size]
        ciphertext = encrypted_data_bytes[self.iv_size:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # PKCS7 unpadding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext_bytes = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        
        return plaintext_bytes.decode('utf-8')

# Ví dụ sử dụng (chỉ để test, có thể bỏ qua trong file thực tế nếu không cần)
if __name__ == '__main__':
    test_key = os.urandom(32) # AES-256 key
    crypto_instance = CryptoUtil(test_key)
    
    original_message = "Đây là một thông điệp bí mật cần được mã hóa!"
    print(f"Original: {original_message}")
    
    encrypted_message = crypto_instance.encrypt(original_message)
    print(f"Encrypted (Base64): {encrypted_message}")
    
    decrypted_message = crypto_instance.decrypt(encrypted_message)
    print(f"Decrypted: {decrypted_message}")
    
    assert original_message == decrypted_message
    print("CryptoUtil test successful!")