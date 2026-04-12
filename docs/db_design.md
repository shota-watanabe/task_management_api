## 1. データベース物理設計書

すべてのテーブルにおいて、`id` は自動採番の主キー（PK）とします。

### 1.1 ユーザーテーブル (users)
| No | PK | UK | カラム名 | 項目名 | 概要 | データ型 | 長さ | NOT NULL | 列制約 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 〇 | | id | ユーザーID | ユーザーを一意に識別するID | BIGSERIAL | - | 〇 | | |
| 2 | | 〇 | username | ユーザー名 | ユーザーの表示名 | VARCHAR | 50 | 〇 | | |
| 3 | | 〇 | email | メールアドレス | ログインや通知用のアドレス | VARCHAR | 255 | 〇 | | |
| 4 | | | password_hash | パスワードハッシュ | 暗号化されたパスワード | VARCHAR | 255 | 〇 | | |
| 5 | | | created_at | 作成日時 | レコードの作成日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
| 6 | | | updated_at | 更新日時 | レコードの最終更新日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |

### 1.2 プロジェクトテーブル (projects)
| No | PK | UK | カラム名 | 項目名 | 概要 | データ型 | 長さ | NOT NULL | 列制約 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 〇 | | id | プロジェクトID | プロジェクトを一意に識別するID | BIGSERIAL | - | 〇 | | |
| 2 | | | name | プロジェクト名 | プロジェクトの名称 | VARCHAR | 128 | 〇 | | |
| 3 | | | description | 説明 | プロジェクトの詳細説明 | TEXT | - | | | |
| 4 | | | created_at | 作成日時 | レコードの作成日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
| 5 | | | updated_at | 更新日時 | レコードの最終更新日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |

### 1.3 プロジェクトメンバーテーブル (project_members)
| No | PK | UK | カラム名 | 項目名 | 概要 | データ型 | 長さ | NOT NULL | 列制約 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 〇 | | id | ID | メンバー紐付けを一意に識別するID | BIGSERIAL | - | 〇 | | |
| 2 | | | project_id | プロジェクトID | 紐づくプロジェクトのID | BIGINT | - | 〇 | FK (projects.id) | |
| 3 | | | user_id | ユーザーID | 紐づくユーザーのID | BIGINT | - | 〇 | FK (users.id) | |
| 4 | | | role | ロール | プロジェクト内の権限 | VARCHAR | 20 | 〇 | DEFAULT 'member' | 'admin' または 'member' |
| 5 | | | created_at | 作成日時 | レコードの作成日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
| 6 | | | updated_at | 更新日時 | レコードの最終更新日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |

### 1.4 タスクテーブル (tasks)
| No | PK | UK | カラム名 | 項目名 | 概要 | データ型 | 長さ | NOT NULL | 列制約 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 〇 | | id | タスクID | タスクを一意に識別するID | BIGSERIAL | - | 〇 | | |
| 2 | | | project_id | プロジェクトID | 紐づくプロジェクトのID | BIGINT | - | 〇 | FK (projects.id) | |
| 3 | | | assigned_user_id | 担当ユーザーID | タスクを担当するユーザーのID | BIGINT | - | | FK (users.id) | 未アサイン許容 |
| 4 | | | title | タイトル | タスクの名称 | VARCHAR | 128 | 〇 | | |
| 5 | | | status | ステータス | 現在の進行状況 | VARCHAR | 20 | 〇 | DEFAULT 'todo' | 'todo', 'doing', 'done' |
| 6 | | | start_date | 開始予定日 | タスクの開始予定日 | DATE | - | | | |
| 7 | | | expire_date | 完了期限日 | タスクの完了期限日 | DATE | - | | | |
| 8 | | | end_date | 実際の完了日 | タスクが実際に完了した日 | DATE | - | | | |
| 9 | | | created_at | 作成日時 | レコードの作成日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
| 10| | | updated_at | 更新日時 | レコードの最終更新日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |

### 1.5 コメントテーブル (comments)
| No | PK | UK | カラム名 | 項目名 | 概要 | データ型 | 長さ | NOT NULL | 列制約 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 〇 | | id | コメントID | コメントを一意に識別するID | BIGSERIAL | - | 〇 | | |
| 2 | | | task_id | タスクID | 紐づくタスクのID | BIGINT | - | 〇 | FK (tasks.id) | |
| 3 | | | user_id | ユーザーID | コメントを投稿したユーザーのID | BIGINT | - | 〇 | FK (users.id) | |
| 4 | | | content | 内容 | コメントの本文 | TEXT | - | 〇 | | |
| 5 | | | created_at | 作成日時 | レコードの作成日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
| 6 | | | updated_at | 更新日時 | レコードの最終更新日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |

### 1.6 ラベルテーブル (labels)
| No | PK | UK | カラム名 | 項目名 | 概要 | データ型 | 長さ | NOT NULL | 列制約 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 〇 | | id | ラベルID | ラベルを一意に識別するID | BIGSERIAL | - | 〇 | | |
| 2 | | 〇 | name | ラベル名 | ラベルの名称（例: "バグ"） | VARCHAR | 50 | 〇 | | |
| 3 | | | color_code | カラーコード | 画面表示用の色（例: "#FF0000"）| VARCHAR | 7 | | | UI表示用に持たせると実用的 |
| 4 | | | created_at | 作成日時 | レコードの作成日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
| 5 | | | updated_at | 更新日時 | レコードの最終更新日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |

### 1.7 タスクラベルテーブル (task_labels)
| No | PK | UK | カラム名 | 項目名 | 概要 | データ型 | 長さ | NOT NULL | 列制約 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 〇 | | id | ID | 紐付けを一意に識別するID | BIGSERIAL | - | 〇 | | |
| 2 | | 〇 | task_id | タスクID | 紐づくタスクのID | BIGINT | - | 〇 | FK (tasks.id) | UKはlabel_idと複合 |
| 3 | | 〇 | label_id | ラベルID | 紐づくラベルのID | BIGINT | - | 〇 | FK (labels.id) | UKはtask_idと複合 |
| 4 | | | created_at | 作成日時 | レコードの作成日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
| 5 | | | updated_at | 更新日時 | レコードの最終更新日時 | TIMESTAMP | - | 〇 | DEFAULT CURRENT_TIMESTAMP | |
