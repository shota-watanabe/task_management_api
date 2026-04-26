# チーム向けタスク管理API

## 概要
複数プロジェクトを兼務するメンバーの負荷状況や進捗を、シンプルに可視化・管理するための軽量なタスク管理APIです。

## 🛠 技術スタック
バックエンドおよびインフラの主要な技術スタックは以下の通りです。

**Backend**
* **言語:** Python 3.11
* **フレームワーク:** FastAPI
* **ORM:** SQLAlchemy
* **DBマイグレーション:** Alembic
* **認証:** JWT (PyJWT / bcrypt)
* **テスト:** pytest
* **Linter / Formatter:** Ruff

**Database & Infrastructure**
* **データベース:** PostgreSQL 15
* **インフラ:** Docker / Docker Compose

---

## 🚀 環境構築手順

本プロジェクトは Docker を使用して完全にコンテナ化されています。以下の手順でローカル環境を構築してください。

### 前提条件
* Git がインストールされていること
* Docker および Docker Compose がインストールされ、起動していること

### セットアップ手順

**1. リポジトリのクローン**
```bash
git clone https://github.com/shota-watanabe/task_management_api.git
```
```bash
cd task_management_api
```

**2. 環境変数の設定**
サンプルファイルをコピーして、ローカル用の環境変数ファイル（`.env`）を作成します。
```bash
cp .env.sample .env
```
※ 必要に応じて `.env` 内の `SECRET_KEY` などの値を変更してください。

**3. コンテナのビルドと起動**
```bash
docker compose up -d --build
```

**4. データベースのマイグレーション**
コンテナが起動したら、Alembicを使用してデータベースのテーブルを作成します。
```bash
docker compose exec api alembic upgrade head
```

---

## 📖 APIドキュメント (Swagger UI)

サーバーが起動すると、FastAPIの自動生成ドキュメントにアクセスできます。ブラウザから以下のURLを開いてください。

* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc

APIのエンドポイント一覧や、ブラウザ上からのAPIリクエストのテストは Swagger UI から実行可能です。

---

## ✅ テストの実行方法
コンテナが起動している状態で、以下のコマンドを実行すると `pytest` による自動テストが走ります。
```bash
docker compose exec api pytest -v
```
