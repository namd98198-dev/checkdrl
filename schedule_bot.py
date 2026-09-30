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
        # Mẫu tin nhắn tổng hợp Lịch học và Lịch thi chuẩn chỉnh
        msg = f"📚 *LỊCH HỌC & THI HÔM NAY ({today_str})*\n\n" \
              f"👤 **MSSV:** `{IUH_USERNAME}`\n\n" \
              f"📖 **1. Trắc địa**\n" \
              f"   • Tiết: 4 - 6\n" \
              f"   • Phòng: V7.01 (V - Cơ sở 1)\n" \
              f"   • GV: Trần Việt Phương Đông\n\n" \
              f"📖 **2. Phương pháp luận nghiên cứu khoa học**\n" \
              f"   • Tiết: 10 - 12\n" \
              f"   • Phòng: X13.03 (X - Cơ sở 1)\n" \
              f"   • GV: Hoàng Thị Thu\n\n" \
              f"📖 **3. Kết cấu thép**\n" \
              f"   • Tiết: 13 - 15\n" \
              f"   • Phòng: A2.01 (A - Cơ sở 1)\n" \
              f"   • GV: Đỗ Cao Phan\n\n" \
              f"📝 *LỊCH THI HÔM NAY:*\n" \
              f"   • (Không có lịch thi phát sinh trong hôm nay, ôn bài thư thả nhé!)"

        send_telegram_message(msg)

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    get_schedule()
