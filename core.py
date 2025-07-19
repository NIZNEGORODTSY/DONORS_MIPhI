import dbapi
from objects import *


def get_uid(tgid: int) -> int:
    res = dbapi.get_uid(tgid)
    return res[0]


def check_user_by_phone(phone_number: str) -> bool:
    users = dbapi.get_users_gy_phone(phone_number)
    return len(users) != 0
    # if len(users) == 0:
    #     return False
    # return True


def check_admin(tgid: int) -> bool:
    res = dbapi.get_admin(tgid)
    return res[0] == 1


def add_user(phone_number: str, tgid: int):
    return dbapi.add_user(phone_number, tgid)


def add_fio(tgid: int, fio: str):
    dbapi.add_fio(tgid, fio)


def add_ugroup(tgid: int, ugroup: str):
    return dbapi.add_ugroup(tgid, ugroup)


def add_contacts(tgid: int, contacts: str):
    return dbapi.add_contacts(tgid, contacts)


def add_donation(tgid: int) -> int:
    uid = get_uid(tgid)
    return dbapi.add_donation(uid)


def add_donation_donplace(tgid: int, donplace: int):  # 0 - Гавр, 1 - ФМБА
    uid = get_uid(tgid)
    return dbapi.add_donation_donplace(uid, donplace)


def get_user(tgid: int) -> User:
    ans = dbapi.get_user(tgid)

    res = User()
    res.Id = ans[0][0]
    res.Fio = ans[0][1]
    res.Group = ans[0][2]
    res.CountGavr = ans[0][3]
    res.CountFMBA = ans[0][4]
    res.SumCount = ans[0][5]
    res.LastGavr = ans[0][6]
    res.LastFMBA = ans[0][7]
    res.Contacts = ans[0][8]
    res.PhoneNumber = ans[0][9]
    res.IsAdmin = ans[0][10]
    res.Registry = ans[0][11]
    res.Tgid = ans[0][12]

    return res


def get_user_history(uid: int) -> list[Donation]:
    ans = dbapi.get_donation_history(uid)

    res = []

    for donation in ans:
        Don = Donation()
        Don.Id = donation[0]
        Don.Uid = uid
        Don.DonPlace = donation[2]
        Don.DonDate = donation[3]

        res.append(Don)

    return res


def get_admins() -> list[User]:
    ans = dbapi.get_admins()

    res = []

    for u in ans:
        adm = User()
        adm.Id = u[0]
        adm.Fio = u[1]
        adm.Group = u[2]
        adm.CountGavr = u[3]
        adm.CountFMBA = u[4]
        adm.SumCount = u[5]
        adm.LastGavr = u[6]
        adm.LastFMBA = u[7]
        adm.Contacts = u[8]
        adm.PhoneNumber = u[9]
        adm.IsAdmin = u[10]
        adm.Registry = u[11]
        adm.Tgid = u[12]

        res.append(adm)

    return res


def add_donor(fio: str, ugroup: str, registry: str):  # добавление пользователя админом
    dbapi.add_donor(fio, ugroup, registry)


def add_question(uid: int, question: str):
    dbapi.add_question(uid, question)


def get_all_questions() -> list[Question]:
    ans = dbapi.get_all_questions()

    res = []

    for q in ans:
        question = Question()
        question.Id = q[0]
        question.Uid = q[1]
        question.QuestionMsg = q[2]
        question.HasReply = q[3] == 1
        question.IsSeen = q[4] == 1
        question.Answer = q[5]
        res.append(question)

    return res


def get_info_message(info_type: int) -> str:
    if info_type == InfoTypes.DonationMEPHI:
        filepath = 'donation_mephi'
    elif info_type == InfoTypes.DonationProcedure:
        filepath = 'donation_procedure'
    elif info_type == InfoTypes.DonorAbsContrs:
        filepath = 'donor_abs_contraindications'
    elif info_type == InfoTypes.DonorDiet:
        filepath = 'donor_diet'
    elif info_type == InfoTypes.DonorImportance:
        filepath = 'donor_importance'
    elif info_type == InfoTypes.DonorJoinRegistry:
        filepath = 'donor_join_registry'
    elif info_type == InfoTypes.DonorPreparation:
        filepath = 'donor_preparation'
    elif info_type == InfoTypes.DonorRequirements:
        filepath = 'donor_requirements'
    elif info_type == InfoTypes.DonorTempContrs:
        filepath = 'donor_temp_contraindications'

    with open('messages/' + filepath + '.txt', 'r') as f:
        res = f.read()

    return res

def get_upcoming_events() -> list[UpcomingEvent]:
    ans = dbapi.get_upcoming_events()

    res = []

    for e in ans:
        event = UpcomingEvent()
        event.Id = e[2]
        event.DonPlace = e[0]
        event.DonDate = e[1]
        res.append(event)
    return res

get_all_questions()
