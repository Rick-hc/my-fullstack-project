import re
import textwrap

# ファイルパス
in_path = "raw/term.txt"
out_path = "raw/term_cleaned.txt"

# 1. 全文読み込み
with open(in_path, encoding="utf-8") as rf:
    raw = rf.read()

# 2. 「（1）」 が出てくる直前までをスキップ
first_idx = raw.find("（1）")
if first_idx != -1:
    content = raw[first_idx:]
else:
    content = raw  # 万一「（1）」が見つからなければ全文を使う

# 3. 全角括弧で始まる番号(1)～(n)でスプリット
chunks = re.split(r'(?=（\d+）)', content)

formatted = []
record_count = 0
for chunk in chunks:
    chunk = chunk.strip()
    if not chunk:
        continue

    # 4. 用語ラベルと定義に分割
    m = re.match(r'^(（\d+）\s*[^ \n]+)\s*(.*)$', chunk, re.DOTALL)
    if not m:
        continue

    term_label = m.group(1)
    definition = m.group(2).replace("\n", " ").strip()

    # 5. 不要要素を除去（URL、スクリプト変数など）
    definition = re.sub(r'https?://\S+', '', definition)
    definition = re.sub(r'google_[A-Za-z_]+', '', definition)

    # 6. 定義を80文字幅でラップ
    wrapped = textwrap.wrap(definition, width=80)

    # 7. 出力用リストに追加
    formatted.append(term_label)
    formatted.extend(wrapped)
    formatted.append("")  # レコード間に空行
    record_count += 1

# 8. ファイルへ書き出し
with open(out_path, "w", encoding="utf-8") as wf:
    wf.write("\n".join(formatted))

print(f"✅ {out_path} に {record_count} 件を整形して出力しました")
