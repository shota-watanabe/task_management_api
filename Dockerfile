# 軽量なPythonイメージを使用
FROM python:3.11-slim

# コンテナ内の作業ディレクトリを設定
WORKDIR /src

# 環境変数を設定（Pythonがpycファイルを作成しない、バッファリングしない設定）
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 依存ライブラリをインストール
# 先にrequirements.txtだけコピーすることで、ソース修正時にキャッシュを効かせビルドを速くする
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY ./app ./app

# FastAPIを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
