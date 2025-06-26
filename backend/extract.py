from bs4 import BeautifulSoup

# 1. バイナリモードで読み込む
with open("raw/term.htm", "rb") as rf:
    raw_bytes = rf.read()

# 2. BeautifulSoup に解析させつつエンコーディング判定
soup = BeautifulSoup(raw_bytes, "html.parser", from_encoding=None)

# 3. テキスト抽出
text = soup.get_text(separator="\n")

# 4. ファイルに書き出し（UTF-8 で保存）
with open("raw/term.txt", "w", encoding="utf-8") as wf:
    wf.write(text)

print("✅ raw/term.txt にテキストを出力しました")
