def test_signup(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "id" in data


def test_signup_duplicate_email(client, registered_user):
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "anotheruser",
            "email": registered_user["email"],  # 同じメールアドレスを使う
            "password": "anotherpassword",
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "このメールアドレスは既に登録されています。"


def test_login_success(client, registered_user):
    # registered_user フィクスチャが事前にユーザーを作るので、実行順序に依存しない
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["email"],
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "メールアドレスまたはパスワードが間違っています"
