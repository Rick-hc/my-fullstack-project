# 🦷 DentAssist-RAG MVP

> **React + FastAPI** で構築した歯科向け QA ボットの最小実装。  
> **LLM ➜ クエリ生成 ➜ ベクトル検索 ➜ Top-k 候補 UI ➜ 回答返却** のフローを再現します。

---

## 📁 ディレクトリ構成

```text
my-fullstack-project/
├─ backend/                 FastAPI + RAG ロジック
│  ├─ api.py                REST エンドポイント (/api/query, /api/answer)
│  ├─ ragPromptBuilder.py   LLM プロンプト生成 & コンテキスト結合
│  ├─ search_embeddings.py  ベクトル検索（NumPyのみ使用）
│  ├─ qa_utils.py           id → {Q,A} のマッピング読み込み
│  └─ raw/embeddings_full.json   ← QA + 埋め込みコーパス
├─ frontend/                React 18 + Vite + Chakra UI
│  ├─ src/components/ChatWindow.tsx   チャット画面 & 候補リスト
│  └─ ...
└─ README.md（本ファイル）

⚡ クイックスタート（ローカル動作）
# 1) 仮想環境（Python 3.11 または 3.12）
python -m venv .venv
. .venv\Scripts\activate          # mac/Linux は source .venv/bin/activate

# 2) 依存インストール
pip install -r backend/requirements.txt

# 3) OpenAI APIキーを設定（必須）
set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx   # mac/Linux は export

# 4) 起動
uvicorn backend.api:app --reload --port 8000

cd frontend
npm ci            # または pnpm install
npm run dev       # または pnpm dev

🏃 動作フロー
ユーザー入力
例: 在宅医療対応とは何ですか？

バックエンド処理

generate_query() が LLM（gpt-4.1-nano）で検索用クエリを生成。

search_embeddings.py がクエリを埋め込み→コサイン類似度→Top-k (=5) {id,Q,score} を返却。

フロント UI が Top-k 候補の Q を一覧表示。

候補クリック → /api/answer が id に対応する A を返す（LLM 呼び出しなし）。

答えをチャットに表示。


🔌 REST API 仕様
メソッド & パス	リクエスト	レスポンス	概要
POST /api/query	{question}	{items:[{id,q,score}]}	クエリ生成＋ベクトル検索
POST /api/answer	{chunk_id,question}	{answer}	id から A を取得（404 なら not found）

Swagger: http://localhost:8000/docs

📐 埋め込み JSON フォーマット
[
  {
    "id": "chunk_0001",
    "Q": "在宅医療対応とは何ですか？",
    "A": "在宅医療対応とは、歯科医師が ...",
    "embedding": [0.123, 0.456, ...]  // 3072 次元ベクトル
  }
]

Happy hacking! 🦷
