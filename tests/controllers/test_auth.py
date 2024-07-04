from app.utils.jwt import create_access_token


class TestAuthSignUpController:
    def setup_method(self, method):
        self.data = {"email": "duy123@gmail.com", "password": "Duy123456!", "name": "duy"}

    def test_sign_up_success(self, client, db):
        res = client.post("/auth/signup", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 200

        res_data = res.json()
        assert res_data["email"] == self.data["email"]
        assert res_data["name"] == self.data["name"]
        assert "uuid" in res_data
        assert "created_at" in res_data
        assert "updated_at" in res_data
        assert "id" not in res_data
        assert "password" not in res_data
        assert "password_hash" not in res_data
        assert "password_salt" not in res_data

    def test_sign_up_failed_invalid_email(self, client, db):
        self.data["email"] = "random string"

        res = client.post("/auth/signup", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 422

        res_data = res.json()
        assert (
            res_data["detail"][0]["msg"] == "value is not a valid email address: An email address must have an @-sign."
        )

    def test_sign_up_failed_invalid_password(self, client, db):
        self.data["password"] = "123456"

        res = client.post("/auth/signup", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 422

        res_data = res.json()
        assert (
            res_data["detail"][0]["msg"]
            == "Value error, Password must contain at least 1 uppercase, 1 lowercase, 1 number, and 1 special character"
        )

    def test_sign_up_failed_invalid_name(self, client, db):
        self.data["name"] = 1234

        res = client.post("/auth/signup", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 422

        res_data = res.json()
        assert res_data["detail"][0]["msg"] == "Input should be a valid string"


class TestAuthLoginController:
    def setup_method(self, method):
        self.data = {"email": "duy123@gmail.com", "password": "Duy123456!"}

    def test_login_success(self, client, db, user):
        res = client.post("/auth/login", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 200

        res_data = res.json()
        assert "access_token" in res_data
        assert res_data["access_token"] == create_access_token({"uuid": user.uuid})

    def test_login_failed_invalid_email(self, client, db, user):
        self.data["email"] = "random email"

        res = client.post("/auth/login", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 422

        res_data = res.json()
        assert (
            res_data["detail"][0]["msg"] == "value is not a valid email address: An email address must have an @-sign."
        )

    def test_login_failed_invalid_password(self, client, db, user):
        self.data["password"] = "123456"

        res = client.post("/auth/login", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 422

        res_data = res.json()
        assert (
            res_data["detail"][0]["msg"]
            == "Value error, Password must contain at least 1 uppercase, 1 lowercase, 1 number, and 1 special character"
        )

    def test_login_failed_wrong_credentials(self, client, db, user):
        self.data["email"] = "email@email.com"
        self.data["password"] = "Pass123!"

        res = client.post("/auth/login", json=self.data, headers={"Content-Type": "application/json"})
        assert res.status_code == 400

        res_data = res.json()
        assert res_data["detail"] == "Wrong email or password"
