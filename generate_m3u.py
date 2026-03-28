import requests
import json
import sys
import os

def generate_m3u(slug):
    api_url = f"https://phimapi.com/phim/{slug}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}")
        return

    if not data.get("status"):
        print(f"Không tìm thấy phim với slug: {slug}")
        return

    movie = data["movie"]
    movie_name = movie["name"]
    poster = movie["poster_url"]
    episodes_data = data["episodes"]

    file_name = f"{slug}.m3u"
    
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for server in episodes_data:
            # Lấy tên nhóm (Vietsub, Thuyết minh...) từ server_name
            server_name = server["server_name"]
            
            for ep in server["server_data"]:
                ep_name = ep["name"]
                link = ep["link_m3u8"]
                
                # Định dạng IPTV chuẩn
                # group-title sẽ giúp các trình phát IPTV phân loại thư mục
                f.write(f'#EXTINF:-1 tvg-logo="{poster}" group-title="{movie_name} ({server_name})",{movie_name} - {ep_name}\n')
                f.write(f"{link}\n")

    print(f"Đã tạo file thành công: {file_name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        slug_input = sys.argv[1]
        generate_m3u(slug_input)
    else:
        print("Vui lòng nhập slug phim.")
