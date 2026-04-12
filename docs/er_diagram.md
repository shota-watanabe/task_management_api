```mermaid
erDiagram
users ||--o{ project_members : "has"
projects ||--o{ project_members : "has"
projects ||--o{ tasks : "contains"
users |o--o{ tasks : "assigned to"
tasks ||--o{ comments : "has"
users ||--o{ comments : "writes"
tasks ||--o{ task_labels : "has"
labels ||--o{ task_labels : "applied to"
users {
    BIGSERIAL id PK
    VARCHAR(50) username UK
    VARCHAR(255) email UK
    VARCHAR(255) password_hash
    TIMESTAMP created_at
    TIMESTAMP updated_at
}
projects {
    BIGSERIAL id PK
    VARCHAR(128) name
    TEXT description
    TIMESTAMP created_at
    TIMESTAMP updated_at
}
project_members {
    BIGSERIAL id PK
    BIGINT project_id FK
    BIGINT user_id FK
    VARCHAR(20) role
    TIMESTAMP created_at
    TIMESTAMP updated_at
}
tasks {
    BIGSERIAL id PK
    BIGINT project_id FK
    BIGINT assigned_user_id FK
    VARCHAR(128) title
    VARCHAR(20) status
    DATE start_date
    DATE expire_date
    DATE end_date
    TIMESTAMP created_at
    TIMESTAMP updated_at
}
comments {
    BIGSERIAL id PK
    BIGINT task_id FK
    BIGINT user_id FK
    TEXT content
    TIMESTAMP created_at
    TIMESTAMP updated_at
}
labels {
    BIGSERIAL id PK
    VARCHAR(50) name UK
    VARCHAR(7) color_code
    TIMESTAMP created_at
    TIMESTAMP updated_at
}
task_labels {
    BIGSERIAL id PK
    BIGINT task_id FK
    BIGINT label_id FK
    TIMESTAMP created_at
    TIMESTAMP updated_at
}
