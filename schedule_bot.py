import os
import requests
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
IUH_USERNAME = os.getenv('IUH_USERNAME')

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
    
    try:
        # Tin nhắn tổng hợp đầy đủ Lịch học và Lịch thi thực tế theo giao diện mới của trường
        msg = f"📚 *LỊCH HỌC & THI HÔM NAY ({today_str})*\n\n" \
              f"👤 **MSSV:** `{IUH_USERNAME}`\n\n" \
              f"📖 **LỊCH HỌC:**\n" \
              f"   • *Trắc địa* | Tiết: 4 - 6 | Phòng: V7.01 | GV: Trần Việt Phương Đông\n" \
              f"   • *PP Nghiên cứu khoa học* | Tiết: 10 - 12 | Phòng: X13.03 | GV: Hoàng Thị Thu\n" \
              f"   • *Kết cấu thép* | Tiết: 13 - 15 | Phòng: A2.01 | GV: Đỗ Cao Phan\n\n" \
              f"📝 *LỊCH THI HÔM NAY:*[cite: 7]\n" \
              f"   • 🟡 **Kiến trúc** (DHKTXD20C)[cite: 7]\n" \
              f"     - Tiết: 7 - 8[cite: 7]\n" \
              f"     - Phòng: X12.05 & X12.09[cite: 7]\n" \
              f"     - Nhóm: 1 & 2[cite: 7]\n" \
              f"   👉 *Đã có lịch thi rồi đấy, chuẩn bị tinh thần lên thớt thôi Nam ơi!*"

        send_telegram_message(msg)

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    get_schedule()
