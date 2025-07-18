import dbapi
from typing import Tuple

class AuthAnswers:
    Register = 0
    Success = 1

def check_user_by_phone(phone_number: str) -> Tuple[AuthAnswers, list | None]:
    users = dbapi.get_users_gy_phone(phone_number)
    if (len(users) == 0):
        return AuthAnswers.Register, None
    return AuthAnswers.Success, users[0]