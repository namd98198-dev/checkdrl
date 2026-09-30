import os
import json
import requests
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://doantn.iuh.edu.vn/'

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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        current_activities = {}
        
        # Chỉ quét các thẻ a nằm trong danh sách bài viết/hoạt động (thường có class hoặc nằm trong thẻ tin tức)
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            href = a['href']
            
            # Lọc chỉ lấy các tiêu đề bài viết thực tế (loại bỏ các menu hệ thống, footer, thông tin cá nhân)
            if len(text) > 20 and not any(k in text.lower() for k in ['hội sinh viên', 'việc làm', 'đoàn khoa', 'trang chủ', 'đăng xuất', 'tra cứu', 'thông tin']):
                if href.startswith('/'):
                    link = 'https://doantn.iuh.edu.vn' + href
                elif not href.startswith('http'):
                    link = 'https://doantn.iuh.edu.vn/' + href
                else:
                    link = href
                current_activities[text] = link

        print(f"Tìm thấy {len(current_activities)} hoạt động hợp lệ.")

        if not old_activities:
            # Khởi tạo lần đầu không bắn spam, chỉ lưu lại mốc
            all_current = list(current_activities.keys())
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(all_current, f, ensure_ascii=False, indent=2)
            print("Đã khởi tạo lịch sử thành công.")
            return

        new_items = set(current_activities.keys()) - old_activities
        
        if new_items:
            for name in new_items:
                link = current_activities[name]
                msg = f"🔥 *CÓ HOẠT ĐỘNG ĐIỂM RÈN LUYỆN MỚI!*\n\n📌 **Tên:** {name}\n🔗 [Bấm vào đây để xem chi tiết]({link})"
                send_telegram_message(msg)
            
            all_current = list(old_activities.union(current_activities.keys()))
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(all_current, f, ensure_ascii=False, indent=2)
        else:
            print("Không có hoạt động mới.")
                
    except Exception as e:
        print(f"Lỗi cào dữ liệu: {e}")

if __name__ == '__main__':
    check_activities()
