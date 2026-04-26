# 開発ガイドライン

## 1. ディレクトリ構成
本プロジェクトは、FastAPIのベストプラクティスに基づいたレイヤードアーキテクチャを採用しています。

```text
.
├── alembic/              # DBマイグレーションスクリプト
├── app/                  # アプリケーションソースコード
│   ├── core/             # 設定管理・セキュリティ関連（JWT発行など）
│   ├── crud/             # DB操作ロジック（Create, Read, Update, Delete）
│   ├── models/           # SQLAlchemyのDBモデル定義
│   ├── routers/          # APIエンドポイントの定義（ルーティング）
│   ├── schemas/          # Pydanticモデル（バリデーション・型定義）
│   ├── database.py       # DB接続設定
│   └── main.py           # アプリのエントリポイント
├── docs/                 # 設計ドキュメント類
├── tests/                # 自動テストコード
├── .env                  # 環境変数（Git管理対象外）
├── alembic.ini           # Alembic設定ファイル
├── docker-compose.yml    # Docker構成定義
├── Dockerfile            # APIサーバーのビルド定義
├── pyproject.toml        # Ruff（静的解析）設定
├── pytest.ini            # pytest設定
└── requirements.txt      # 依存ライブラリ一覧
```

## 2. コーディング規約
### 2.1 命名規則
- ファイル名・変数名・関数名
  - `snake_case` を使用します（例: `user_id`, `get_current_user`）。
- クラス名
  - `PascalCase` を使用します（例: `User`, `ProjectCreate`）。
- 定数名
  - `UPPER_SNAKE_CASE` を使用します。

### 2.2 データベース
- 型選択
  - 主キーなどのIDには `Integer` 型を採用し、メモリ効率を最適化します。
- 時刻
  - タイムゾーンは `Asia/Tokyo（JST）`を基本とし、DB保存時およびAPIレスポンスの時間を日本時間に統一します。
- マイグレーション
  - スキーマ変更は必ず `alembic` を通して行います。

### 2.3 バリデーション (Pydantic)
- V2準拠
  - 最新の `Pydantic V2` の記法に従います。
- Config定義
  - `class Config` ではなく `ConfigDict` を使用します。
- ORM連携
  - レスポンスモデルでは `from_attributes = True` を設定します。

### 2.4 セキュリティ
- パスワード
  - `bcrypt` を用いてハッシュ化し、平文での保存を禁止します。
- 認証
  - JWTトークンによる認証を行い、秘匿情報は `.env` ファイルで管理します。

## 3. ツール・コマンド
### コード整形と品質チェック
Ruff を使用して、コードの自動整形と静的解析を行います。
- 1行の最大文字数: 119文字。
- 実行コマンド

```bash
# 整形とimportソート
docker compose exec api ruff format .
docker compose exec api ruff check --select I --fix .
```

### テスト
pytest を使用し、各機能の実装とセットでテストコードを記述します。

- 実行コマンド
```bash
docker compose exec api pytest -v
```
