import datetime

class User:
    Id: int
    Fio: str | None
    Group: str | None
    CountGavr: int | None
    CountFMBA: int | None
    SumCount: int | None
    LastGavr: datetime.date | None
    LastFMBA: datetime.date | None
    Contacts: str | None
    PhoneNumber: str | None
    IsAdmin: int
    Registry: int | None
    Tgid: int | None

    def __init__(self):
        pass

class Donation:
    Id: int
    Uid: int | None
    DonPlace: str | None
    DonDate: datetime.date | None

    def __init__(self):
        pass

class InfoTypes:
    DonationMEPHI = 0
    DonationProcedure = 1
    DonorAbsContrs = 2
    DonorDiet = 3
    DonorImportance = 4
    DonorJoinRegistry = 5
    DonorPreparation = 6
    DonorRequirements = 7
    DonorTempContrs = 8
