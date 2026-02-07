from src.api.v1.utils.jwt_utils import generate_tokens

class AuthService:
    @staticmethod
    def register_user(data):
        from src.models.user import User
        return User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role=data.get("role", "new_user"),
        )

    @staticmethod
    def login_user(data):
        user = data["user"]
        return generate_tokens(user)
