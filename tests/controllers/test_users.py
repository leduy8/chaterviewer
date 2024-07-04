from app.utils.jwt import create_access_token
from tests.dummy_data import create_dummy_text


class TestGetUserInfoController:
    def test_get_user_info_success(self, client, db, user, access_token):
        res = client.get(
            "/users/me", headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        )
        assert res.status_code == 200

        res_data = res.json()
        assert res_data["email"] == user.email
        assert res_data["name"] == user.name
        assert "uuid" in res_data
        assert "created_at" in res_data
        assert "updated_at" in res_data
        assert "id" not in res_data
        assert "password" not in res_data
        assert "password_hash" not in res_data
        assert "password_salt" not in res_data

    def test_get_user_info_failed_no_access_token(self, client, db, user):
        res = client.get("/users/me", headers={"Content-Type": "application/json"})
        assert res.status_code == 401

        res_data = res.json()
        assert res_data["detail"] == "Token is either missing or invalid"

    def test_get_user_info_failed_invalid_access_token_user_not_found(self, client, db, user):
        invalid_access_token = create_access_token({"uuid": create_dummy_text(32)})

        res = client.get(
            "/users/me", headers={"Content-Type": "application/json", "Authorization": f"Bearer {invalid_access_token}"}
        )
        assert res.status_code == 401

        res_data = res.json()
        assert res_data["detail"] == "Token is invalid"

    def test_get_user_info_failed_invalid_access_token_secret_key(self, client, db, user, invalid_access_token):
        res = client.get(
            "/users/me", headers={"Content-Type": "application/json", "Authorization": f"Bearer {invalid_access_token}"}
        )
        assert res.status_code == 401

        res_data = res.json()
        assert res_data["detail"] == "Token is invalid"


class TestUpdateUserInfoController:
    def setup_method(self, method):
        self.data = {"name": create_dummy_text(10)}

    def test_update_user_info_success(self, client, db, user, access_token):
        res = client.put(
            "/users/info",
            json=self.data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == 200

        res_data = res.json()
        assert res_data["name"] == self.data["name"]

    def test_update_user_info_failed_invalid_access_token_user_not_found(self, client, db, user):
        invalid_access_token = create_access_token({"uuid": create_dummy_text(32)})

        res = client.put(
            "/users/info",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {invalid_access_token}"},
        )
        assert res.status_code == 401

        res_data = res.json()
        assert res_data["detail"] == "Token is invalid"

    def test_update_user_info_failed_invalid_access_token_secret_key(self, client, db, user, invalid_access_token):
        res = client.put(
            "/users/info",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {invalid_access_token}"},
        )
        assert res.status_code == 401

        res_data = res.json()
        assert res_data["detail"] == "Token is invalid"

    def test_update_user_info_failed_invalid_name(self, client, db, user, access_token):
        self.data["name"] = 1234

        res = client.put(
            "/users/info",
            json=self.data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == 422

        res_data = res.json()
        assert res_data["detail"][0]["msg"] == "Input should be a valid string"
