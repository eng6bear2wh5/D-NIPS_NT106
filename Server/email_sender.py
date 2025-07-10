import smtplib
from email.mime.text import MIMEText
import json
import os
from Client.config import SENDER_EMAIL  # Đọc sender từ config.py

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_user_email(subject, body):
    """
    Gửi email cho user với nội dung tuỳ ý.
    subject: Tiêu đề email
    body: Nội dung email (plain text)
    """

    receiver = "23520766@gm.uit.edu.vn"
    password = "wmqj hzai ersu agdz"
    SENDER_EMAIL = "canopus1607@gmail.com"

    if not receiver or not password:
        print("[Email] Thiếu thông tin receiver_email hoặc password trong user.json")
        return False

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, password)
            server.sendmail(SENDER_EMAIL, receiver, msg.as_string())
        print(f"[Email] Đã gửi email thành công tới {receiver}")
        return True
    except Exception as e:
        print(f"[Email] Lỗi khi gửi email: {e}")
        return False

# Ví dụ sử dụng:
if __name__ == "__main__":
    send_user_email("Test IDS Email", "Đây là email test gửi từ hệ thống IDS.")
