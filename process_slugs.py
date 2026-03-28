import requests
import os

def generate_m3u(slug, is_default=False):
    api_url = f"https://phimapi.com/phim/{slug}"
    output_name = "default.m3u" if is_default else f"{slug}.m3u"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if not data.get("status"):
            print(f"[-] Bỏ qua {slug}: Không tìm thấy dữ liệu.")
            return

        movie = data["movie"]
        movie_name = movie["name"]
        poster = movie["poster_url"]
        episodes_data = data["episodes"]

        with open(output_name, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for server in episodes_data:
                server_name = server["server_name"]
                for ep in server["server_data"]:
                    # Gộp nhóm: Tên phim + Loại (Vietsub/Thuyết Minh)
                    group = f"{movie_name} ({server_name})"
                    f.write(f'#EXTINF:-1 tvg-logo="{poster}" group-title="{group}",{movie_name} - {ep["name"]}\n')
                    f.write(f'{ep["link_m3u8"]}\n')
        print(f"[+] Thành công: {output_name}")

    except Exception as e:
        print(f"[!] Lỗi khi xử lý {slug}: {e}")

if __name__ == "__main__":
    if not os.path.exists("slugs.txt"):
        print("Không tìm thấy file slugs.txt")
        exit(1)

    with open("slugs.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        if line.startswith("default:"):
            slug = line.replace("default:", "").strip()
            generate_m3u(slug, is_default=True)
        else:
            generate_m3u(line)
          
