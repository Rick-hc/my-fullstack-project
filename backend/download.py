import os
import urllib.request

# 保存先ディレクトリを用意
os.makedirs("raw", exist_ok=True)

# targets.txt から URL を読み込み
with open("targets.txt", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

# 取得ループ
for url in urls:
    try:
        print(f"Downloading: {url}")
        # URL末尾をファイル名に（末尾がスラッシュなら index.html）
        fname = url.rstrip("/").split("/")[-1] or "index.html"
        out_path = os.path.join("raw", fname)
        # ダウンロード＆保存
        urllib.request.urlretrieve(url, out_path)
        print(f"  → Saved to {out_path}\n")
    except Exception as e:
        print(f"  ✕ Error fetching {url}: {e}\n")
