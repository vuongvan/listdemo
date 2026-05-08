import requests
import os

def get_m3u_content(slug):
    url = f"https://ophim1.com/v1/api/phim/{slug}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json().get('data', {})
        item = data.get('item', {})
        if not item: return None

        movie_name = item.get('name', 'Movie')
        episodes_list = item.get('episodes', [])

        # Chọn server: Ưu tiên Thuyết minh/Lồng tiếng
        selected_server = None
        priority = ["thuyết minh", "lồng tiếng"]
        
        for server in episodes_list:
            name_low = server.get('server_name', '').lower()
            if any(p in name_low for p in priority):
                selected_server = server
                break
        
        if not selected_server and episodes_list:
            selected_server = episodes_list[0]
            
        if not selected_server: return None

        # Tạo nội dung M3U
        lines = ["#EXTM3U"]
        for ep in selected_server.get('server_data', []):
            lines.append(f"#EXTINF:-1, {movie_name} - Tập {ep.get('name')}")
            lines.append(ep.get('link_m3u8'))
        
        return "\n".join(lines)
    except Exception as e:
        print(f"Lỗi khi xử lý slug {slug}: {e}")
        return None

def main():
    if not os.path.exists('slugs.txt'):
        print("Không tìm thấy file slugs.txt")
        return

    # Tạo thư mục đầu ra để chứa các file m3u
    os.makedirs("output", exist_ok=True)

    with open('slugs.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line: continue

        if line.startswith("default:"):
            slug = line.replace("default:", "")
            filename = "default.m3u"
        else:
            slug = line
            filename = f"{slug}.m3u"

        print(f"Đang xử lý: {slug} -> {filename}")
        content = get_m3u_content(slug)
        
        if content:
            with open(f"output/{filename}", "w", encoding="utf-8") as out:
                out.write(content)

if __name__ == "__main__":
    main()
