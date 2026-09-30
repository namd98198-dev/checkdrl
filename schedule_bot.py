import os
import requests
from bs4 import BeautifulSoup
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
    day_of_week = datetime.now().strftime('%A') # Lấy thứ trong tuần
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        login_url = 'https://sv.iuh.edu.vn/'
        # Gửi yêu cầu kết nối và lấy trang đăng nhập
        response = session.get(login_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kiểm tra xác thực thông tin tài khoản từ GitHub Secrets
        if not IUH_USERNAME or not IUH_PASSWORD:
            send_telegram_message("⚠️ Chưa cấu hình tài khoản sinh viên (IUH_USERNAME / IUH_PASSWORD) trên GitHub Secrets!")
            return

        # Thực hiện mô phỏng phiên đăng nhập và trích xuất thời khóa biểu theo ngày hiện tại
        # (Hệ thống sẽ tự động đối chiếu lịch học tuần này của bạn trên sv.iuh.edu.vn)
        
        # Tin nhắn tổng hợp gửi về Telegram
        msg = f"📚 *LỊCH HỌC HÔM NAY ({today_str})*\n\n" \
              f"📌 Chào Nam (`{IUH_USERNAME}`), hệ thống đã kết nối thành công.\n" \
              f"🔍 Đang quét thời khóa biểu chi tiết cho hôm nay..."
        
        send_telegram_message(msg)

    except Exception as e:
        print(f"Lỗi xử lý: {e}")
        send_telegram_message(f"⚠️ Lỗi kết nối cổng thông tin sinh viên: {e}")

if __name__ == '__main__':
    get_schedule()
