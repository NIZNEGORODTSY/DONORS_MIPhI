import dbapi

def get_uid(tgid: int) -> int:
    res = dbapi.get_uid(tgid)
    return res[0]

def check_user_by_phone(phone_number: str) -> bool:
    users = dbapi.get_users_gy_phone(phone_number)
    if (len(users) == 0):
        return False
    return True

def check_admin(tgid: int) -> bool:
    res = dbapi.get_admin(tgid)
    return res[0] == 1

def add_user(phone_number: str, tgid: int):
    dbapi.add_user(phone_number, tgid)

def add_fio(tgid: int, fio: str):
    dbapi.add_fio(tgid, fio)

def add_ugroup(tgid: int, ugroup: str):
    dbapi.add_ugroup(tgid, ugroup)

def add_contacts(tgid: int, contacts: str):
    dbapi.add_contacts(tgid, contacts)

def add_donation(tgid: int):
    uid = get_uid(tgid)
    dbapi.add_donation(uid)

def add_donation_donplace(tgid: int, donplace: int): # 0 - Гавр, 1 - ФМБА
    uid = get_uid(tgid)
    dbapi.add_donation_donplace(uid, donplace)

def get_user(tgid: int):
    res = dbapi.get_user(tgid)
    return res[0]
