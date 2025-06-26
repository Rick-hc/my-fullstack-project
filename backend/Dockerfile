# --- ベースイメージとして Amazon Linux 2023 を使用 ---
FROM amazonlinux:2023 AS base

# ① OS 更新 & pip インストール
RUN yum -y update && \
    yum -y install python3-pip

# ② 作業ディレクトリ設定
WORKDIR /opt/app

# ③ 依存関係のコピー＆インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- 本番用イメージ ---
FROM base AS prod

# ④ アプリ本体をコピー
COPY . .

# ⑤ 環境変数（本番では Secrets Manager 等から注入）
ENV PYTHONUNBUFFERED=1 \
    RAG_DATA_DIR=/opt/app/raw

# ⑥ ポート公開
EXPOSE 8000

# ⑦ 起動コマンド：Uvicorn で FastAPI を実行
CMD ["python3", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
