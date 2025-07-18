import dbapi

class AuthAnswers:
    Register = 0
    Success = 1

def check_user_by_phone(phone_number: str) -> AuthAnswers:
    users = dbapi.get_users_gy_phone(phone_number)
    if (len(users) == 0):
        return AuthAnswers.Register
    return AuthAnswers.Success

def check_admin(phone_number: str) -> bool:
    is_adm = dbapi.get_admin(phone_number)
    return is_adm[0] == 1

check_admin('+73323945103')