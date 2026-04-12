# APIエンドポイント詳細設計書

## 共通仕様
- **ベースURL:** `/api/v1`
- **認証方式:** HTTP Bearer認証 (JWT)
- **レスポンス形式:** JSON

## 共通エラーレスポンス (Error Handling)

当APIのエラーレスポンスは、フロントエンドでのハンドリングを容易にするため、以下のJSONフォーマットで共通化して返却します。

**基本フォーマット**
```json
{
  "detail": "エラーの具体的なメッセージ",
  "error_code": "エラー種別を特定するコード（任意）"
}
```

### 1. バリデーションエラー（400 Bad Request）
リクエストのパラメータやJSONボディの型、必須項目の不足などがあった場合（FastAPIのPydanticが自動生成するフォーマットに準拠）。

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 2. 認証エラー (401 Unauthorized)
JWTトークンが送信されていない、または有効期限切れ・不正なトークンの場合。

```json
{
  "detail": "認証トークンが無効か、または不足しています。",
  "error_code": "UNAUTHORIZED"
}
```

### 3. 権限エラー (403 Forbidden)
認証はされているが、対象のリソース（プロジェクト作成など）に対する権限（Role）が不足している場合。

```json
{
  "detail": "この操作を実行する権限がありません。",
  "error_code": "PERMISSION_DENIED"
}
```

### 4. リソース未発見エラー (404 Not Found)
指定されたIDのプロジェクトやタスク、ユーザーが存在しない場合。

```json
{
  "detail": "指定されたタスク(ID: 999)は見つかりませんでした。",
  "error_code": "NOT_FOUND"
}
```

### 5. リソース競合エラー (409 Conflict)
すでに登録されているメールアドレスでの新規登録や、すでに設定されているラベルの重複登録など、一意制約（Unique）に違反した場合。

```json
{
  "detail": "このメールアドレスは既に登録されています。",
  "error_code": "ALREADY_EXISTS"
}
```

### 6. サーバー内部エラー (500 Internal Server Error)
データベースの接続エラーなど、バックエンド側で予期せぬ例外が発生した場合。

```json
{
  "detail": "サーバー内部でエラーが発生しました。しばらく経ってから再度お試しください。",
  "error_code": "INTERNAL_SERVER_ERROR"
}
```

---

## 1. 認証系 (Auth)

### 1.1 ユーザー登録
ユーザーを新規作成し、システムを利用可能にします。
- **Endpoint:** `POST /auth/signup`
- **Auth:** 不要

**リクエストボディ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| ユーザー名 | username | string | 〇 | |
| メールアドレス | email | string | 〇 | |
| パスワード | password | string | 〇 | 8文字以上 |

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "securePassword123"
}
```

**レスポンス(201 Created)**

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com"
}
```

### 1.2 ログイン
認証を行い、以降のリクエストに必要なJWTを発行します。
- **Endpoint:** `POST /auth/login`
- **Auth:** 不要

**リクエストボディ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| メールアドレス | email | string | 〇 | |
| パスワード | password | string | 〇 | 8文字以上 |

```json
{
  "email": "user1@example.com",
  "password": "securePassword123"
}
```

**レスポンス(200 OK)**

```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer"
}
```

## 2. プロジェクト系 (Projects)

### 2.1 プロジェクト一覧取得
自身が所属しているプロジェクトの一覧を取得します。
- **Endpoint:** `GET /projects`
- **Auth:** 必須

**レスポンス(201 Created)**

```json
[
  {
    "id": 10,
    "name": "新サービス開発プロジェクト",
    "description": "2027年ローンチ予定のプロジェクト",
    "my_role": "admin",
    "created_at": "2026-04-01T00:00:00Z"
  }
]
```

### 2.2 プロジェクト作成
新規プロジェクトを作成します。作成者は自動的に admin ロールとなります。
- **Endpoint:** `POST /projects`
- **Auth:** 必須

**リクエストボディ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| プロジェクト名 | name | string | 〇 | 128文字以下 |
| 説明 | description | string | 〇 | |

```json
{
  "name": "新サービス開発プロジェクト",
  "description": "次世代SaaSの開発"
}
```

**レスポンス(201 Created)**

```json
{
  "id": 10,
  "name": "新サービス開発プロジェクト",
  "description": "次世代SaaSの開発",
  "created_at": "2024-04-12T10:00:00Z"
}
```

## 3. プロジェクトメンバー系 (Members)

### 3.1 メンバー追加
プロジェクトに他のユーザーを招待（追加）します。
- **Endpoint:** `POST /projects/{project_id}/members`
- **Auth:** 必須（管理者のみ）

**リクエストボディ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| ユーザーID | user_id | bigint | 〇 | 128文字以下 |
| ロール | role | string | 〇 | |

```json
{
  "user_id": 5,
  "role": "member"
}
```

**レスポンス(201 Created)**

```json
{
  "project_id": 10,
  "user_id": 5,
  "role": "member"
}
```

## 4. タスク系 (Tasks)

### 4.1 タスク一覧取得
プロジェクト内のタスクを一覧取得します。
- **Endpoint:** `GET /projects/{project_id}/tasks`
- **Auth:** 必須

**クエリパラメータ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| ステータス | status | string | | |

**レスポンス(200 OK)**

```json
[
  {
    "id": 101,
    "title": "DB設計書の作成",
    "status": "todo",
    "assigned_user": {
      "id": 2,
      "username": "山田太郎"
    },
    "expire_date": "2024-05-01",
    "labels": [
      { "id": 1, "name": "重要", "color": "#FF0000" }
    ]
  }
]
```

### 4.2 タスク作成
プロジェクト内にタスクを作成します。
- **Endpoint:** `POST /projects/{project_id}/tasks`
- **Auth:** 必須（管理者のみ）

**リクエストボディ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| ユーザーID | assigned_user_id | bigint | 〇 | |
| 担当ユーザー名 | role | string | | |
| 開始予定日 | start_date | string | | |
| 開始予定日 | start_date | string | | |
| 完了期限日 | start_date | string | | |

```json
{
  "title": "API実装",
  "assigned_user_id": 2,
  "start_date": "2024-05-01",
  "expire_date": "2024-05-10"
}
```

**レスポンス(201 Created)**

```json
{
  "id": 102,
  "project_id": 10,
  "title": "API実装",
  "status": "todo",
  "created_at": "2024-04-12T10:00:00Z"
}
```

### 4.3 タスク更新
タスクのステータスや担当者を変更します。
- **Endpoint:** `PATCH /tasks/{task_id}`
- **Auth:** 必須（所属メンバーのみ）

**リクエストボディ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| タイトル | title | string | | |
| ステータス | status | string | | |
| 担当ユーザーID | assigned_user_id | bigint | | |
| 実際の完了日 | end_date | string | | |

```json
{
  "status": "doing"
}
```

**レスポンス(201 Created)**

```json
{
  "id": 102,
  "status": "doing",
  "updated_at": "2024-04-12T11:00:00Z"
}
```

## 5. コメント系 (Comments)

### 5.1 コメント投稿
タスクに対してコメントを投稿します。
- **Endpoint:** `POST /tasks/{task_id}/comments`
- **Auth:** 必須

**リクエストボディ**
| 項目名 | カラム名 | 型 | 必須 | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| 内容 | content | string | 〇 | |

```json
{
  "content": "設計のレビューをお願いします。"
}
```

**レスポンス(201 Created)**

```json
{
  "id": 501,
  "task_id": 102,
  "user_id": 1,
  "content": "設計のレビューをお願いします。",
  "created_at": "2024-04-12T12:00:00Z"
}
```
