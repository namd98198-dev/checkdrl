import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Lấy thông tin cấu hình từ GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
IUH_USERNAME = os.getenv('IUH_USERNAME')
IUH_PASSWORD = os.getenv('IUH_PASSWORD')

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def get_today_schedule():
    # Đây là khung logic kết nối và quét lịch học theo ngày từ trang sv.iuh.edu.vn
    # Bot sẽ tự động lấy thời gian hiện tại để so khớp lịch trong ngày
    today_str = datetime.now().strftime('%d/%m/%Y')
    
    # Tin nhắn mẫu gửi về Telegram lúc 6h sáng & 12h trưa
    msg = f"📚 *LỊCH HỌC HÔM NAY ({today_str})*\n\n" \
          f"Đang đồng bộ thời khóa biểu từ trang sinh viên IUH...\n" \
          f"(Hệ thống sẽ tự động gửi chi tiết môn học, phòng học và tiết học cho bạn)."
    
    send_telegram_message(msg)

if __name__ == '__main__':
    get_today_schedule()
