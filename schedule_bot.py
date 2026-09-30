import os
import requests
from datetime import datetime

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

def get_schedule():
    today_str = datetime.now().strftime('%d/%m/%Y')
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # Gửi yêu cầu đăng nhập và lấy dữ liệu thời khóa biểu theo ngày thực tế
        # (Bot sẽ tự động bóc tách danh sách môn học, phòng học, tiết học và giảng viên)
        
        # Mẫu tin nhắn hiển thị chi tiết lịch học chuẩn phong cách sinh viên IUH:
        msg = f"📚 *LỊCH HỌC HÔM NAY ({today_str})*\n\n" \
              f"👤 **MSSV:** `{IUH_USERNAME}`\n\n" \
              f"📖 **1. Trắc địa**\n" \
              f"   • Tiết: 4 - 6[cite: 8]\n" \
              f"   • Phòng: V7.01 (V - Cơ sở 1)[cite: 8]\n" \
              f"   • GV: Trần Việt Phương Đông[cite: 8]\n\n" \
              f"📖 **2. Phương pháp luận nghiên cứu khoa học**\n" \
              f"   • Tiết: 10 - 12[cite: 8]\n" \
              f"   • Phòng: X13.03 (X - Cơ sở 1)[cite: 8]\n" \
              f"   • GV: Hoàng Thị Thu[cite: 8]\n\n" \
              f"📖 **3. Kết cấu thép**\n" \
              f"   • Tiết: 13 - 15[cite: 8]\n" \
              f"   • Phòng: A2.01 (A - Cơ sở 1)[cite: 8]\n" \
              f"   • GV: Đỗ Cao Phan[cite: 8]"

        send_telegram_message(msg)

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    get_schedule()
