import requests
import os

def generate_m3u(slug, is_default=False):
    api_url = f"https://phimapi.com/phim/{slug}"
    output_name = "default.m3u" if is_default else f"{slug}.m3u"
    
    try:
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        if not data.get("status"):
            print(f"[-] Lỗi slug: {slug}")
            return

        movie = data["movie"]
        name = movie["name"]
        poster = movie["poster_url"]
        
        # Mở file để ghi
        with open(output_name, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            for server in data["episodes"]:
                server_name = server['server_name']
                
                # KIỂM TRA: Nếu tên server có chứa "Vietsub" (không phân biệt hoa thường) thì bỏ qua
                if "vietsub" in server_name.lower():
                    print(f"    [SKIPPED] Đã ẩn nhóm Vietsub của phim: {name}")
                    continue
                
                # Gộp nhóm theo tên phim + bản dịch còn lại (Thuyết minh/Lồng tiếng)
                group = f"{name} - {server_name.replace('#', '').strip()}"
                
                for ep in server["server_data"]:
                    f.write(f'#EXTINF:-1 tvg-logo="{poster}" group-title="{group}",{name} - {ep["name"]}\n')
                    f.write(f'{ep["link_m3u8"]}\n')
                    
        print(f"[+] Hoàn tất: {output_name}")
        
    except Exception as e:
        print(f"[!] Lỗi hệ thống với slug {slug}: {e}")

if __name__ == "__main__":
    if os.path.exists("slugs.txt"):
        with open("slugs.txt", "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        for line in lines:
            if line.startswith("default:"):
                slug_val = line.split("default:")[1].strip()
                generate_m3u(slug_val, is_default=True)
            else:
                generate_m3u(line)
    else:
        print("Không tìm thấy file slugs.txt")
                    
