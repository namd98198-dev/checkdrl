import os
import json
import requests
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
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
        r = requests.post(url, json=payload, timeout=10)
        print(f"Telegram response: {r.status_code} - {r.text}")
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        current_activities = {}
        
        # Quét tất cả các đường dẫn thẻ a có tiêu đề rõ ràng
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            href = a['href']
            # Lọc các tiêu đề có độ dài hợp lý của một hoạt động
            if len(text) > 12:
                if href.startswith('/'):
                    link = 'https://doantn.iuh.edu.vn' + href
                elif not href.startswith('http'):
                    link = 'https://doantn.iuh.edu.vn/' + href
                else:
                    link = href
                current_activities[text] = link

        print(f"Tổng số tiêu đề thu thập được: {len(current_activities)}")

        # Nếu lần đầu chạy hoặc file history trống, ta lưu lại mốc hiện tại để làm nền tảng
        if not old_activities:
            print("Khởi tạo danh sách lịch sử ban đầu...")
            all_current = list(current_activities.keys())
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(all_current, f, ensure_ascii=False, indent=2)
            # Gửi tin nhắn xác nhận bot đã hoạt động thông suốt
            send_telegram_message("🤖 **Bot theo dõi điểm rèn luyện IUH đã sẵn sàng!**\nĐã kết nối thành công và đang canh gác hoạt động mới cho bạn.")
            return

        new_items = set(current_activities.keys()) - old_activities
        
        if new_items:
            for name in new_items:
                link = current_activities[name]
                msg = f"🔥 *CÓ HOẠT ĐỘNG ĐIỂM RÈN LUYỆN MỚI!*\n\n📌 **Tên:** {name}\n🔗 [Bấm vào đây để xem chi tiết]({link})"
                send_telegram_message(msg)
            
            # Cập nhật lại lịch sử
            all_current = list(old_activities.union(current_activities.keys()))
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(all_current, f, ensure_ascii=False, indent=2)
        else:
            print("Chưa phát hiện hoạt động mới nào.")
                
    except Exception as e:
        print(f"Lỗi cào dữ liệu: {e}")

if __name__ == '__main__':
    check_activities()
