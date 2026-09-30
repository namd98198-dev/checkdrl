import os
import json
import requests
from bs4 import BeautifulSoup

# Lấy token và chat id từ môi trường bảo mật của GitHub
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Trang web điểm rèn luyện / Đoàn thanh niên IUH (hoặc trang danh sách hoạt động cụ thể)
URL = 'https://doantn.iuh.edu.vn/'

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Chưa cấu hình Token hoặc Chat ID!")
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
        print(f"Lỗi gửi tin nhắn Telegram: {e}")

def check_activities():
    history_file = 'history.json'
    old_activities = set()
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                old_activities = set(json.load(f))
        except Exception:
            old_activities = set()

    try:
        response = requests.get(URL, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        current_activities = {}
        # Quét các tiêu đề bài viết/hoạt động trên trang (thay đổi selector nếu cần thiết)
        for item in soup.select('h3 a, .title a, a.hoat-dong'): 
            name = item.get_text(strip=True)
            link = item.get('href', URL)
            if name:
                if link.startswith('/'):
                    link = 'https://doantn.iuh.edu.vn' + link
                current_activities[name] = link

        # Nếu trang web dùng cấu trúc khác, quét dự trù các thẻ h4 hoặc tiêu đề phổ biến
        if not current_activities:
            for item in soup.find_all('a'):
                text = item.get_text(strip=True)
                href = item.get('href')
                if href and len(text) > 15: # Lọc các đoạn text dài giống tên hoạt động
                    current_activities[text] = href

        new_items = set(current_activities.keys()) - old_activities
        
        if new_items:
            for name in new_items:
                link = current_activities[name]
                msg = f"🔥 **CÓ HOẠT ĐỘNG ĐIỂM RÈN LUYỆN MỚI!**\n\n📌 **Tên:** {name}\n🔗 [Bấm vào đây để xem chi tiết]({link})"
                send_telegram_message(msg)
            
            # Cập nhật lịch sử
            all_current = list(old_activities.union(current_activities.keys()))
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(all_current, f, ensure_ascii=False, indent=2)
        else:
            print("Không có hoạt động mới nào.")
                
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")

if __name__ == '__main__':
    check_activities()
  
