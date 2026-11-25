import os
import re
import sys
import time
import unicodedata
import urllib.request

SOURCE = os.environ.get(
    "SOURCE_URL",
    "https://raw.githubusercontent.com/vietng228/m3u/main/new.m3u",
)
OUTPUT = os.environ.get("OUTPUT_FILE", "sorted.m3u")

# Thứ tự ưu tiên; mỗi nhóm là các tên (đã chuẩn hóa) được coi là cùng một kênh
PRIORITY = [
    {"htv2"},
    {"htv7"},
    {"thvl1", "vinhlong1", "thvinhlong1"},
    {"thvl2", "vinhlong2", "thvinhlong2"},
    {"thvl3", "vinhlong3", "thvinhlong3"},
    {"thvl4", "vinhlong4", "thvinhlong4"},
    {"thvl5", "vinhlong5", "thvinhlong5"},
]


def norm(s: str) -> str:
    """Bỏ dấu, bỏ khoảng trắng/ký tự đặc biệt, viết thường."""
    s = s.replace("Đ", "D").replace("đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def fetch(src: str) -> str:
    if src.startswith("http"):
        sep = "&" if "?" in src else "?"
        req = urllib.request.Request(
            f"{src}{sep}t={int(time.time())}",  # tránh cache của raw.githubusercontent
            headers={"User-Agent": "m3u-sorter"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8-sig")
    with open(src, encoding="utf-8-sig") as f:
        return f.read()


def parse(text: str):
    header, entries, cur = [], [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#EXTINF"):
            cur = [line]
            entries.append(cur)
        elif cur is not None:
            cur.append(line)
            if not line.startswith("#"):  # dòng URL -> kết thúc 1 kênh
                cur = None
        elif line.startswith("#") and not line.startswith("#EXTM3U"):
            header.append(line)
    return header, entries


def channel_name(entry) -> str:
    return entry[0].rsplit(",", 1)[-1].strip()


def priority_index(entry) -> int:
    n = norm(channel_name(entry))
    for i, aliases in enumerate(PRIORITY):
        if n in aliases:
            return i
    return len(PRIORITY)


def main():
    text = fetch(SOURCE)
    extm3u = next(
        (l.strip() for l in text.splitlines() if l.startswith("#EXTM3U")),
        "#EXTM3U",
    )
    header, entries = parse(text)
    if not entries:
        sys.exit("Không tìm thấy kênh nào, dừng để tránh ghi đè file rỗng.")

    entries.sort(key=priority_index)  # sort ổn định: kênh còn lại giữ nguyên thứ tự

    lines = [extm3u, *header]
    for e in entries:
        lines.extend(e)

    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    top = [channel_name(e) for e in entries if priority_index(e) < len(PRIORITY)]
    print(f"{len(entries)} kênh. Đầu danh sách: {top}")


if __name__ == "__main__":
    main()
