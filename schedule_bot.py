import os
import requests
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
IUH_USERNAME = os.getenv('IUH_USERNAME')

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Thiếu Token hoặc Chat ID Telegram!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Telegram response: {r.status_code}")
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def main():
    today_str = datetime.now().strftime('%d/%m/%Y')
    print(f"Đang chạy bot lịch học cho ngày: {today_str}")
    
    if not IUH_USERNAME:
        print("Chưa cấu hình IUH_USERNAME trong Secrets!")
        
    msg = f"📚 *LỊCH HỌC HÔM NAY ({today_str})*\n\n" \
          f"👤 **MSSV:** `{IUH_USERNAME}`\n" \
          f"🤖 Hệ thống tự động đang hoạt động bình thường!"
          
    send_telegram_message(msg)

if __name__ == '__main__':
    main()
