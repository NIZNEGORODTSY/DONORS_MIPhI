import datetime
from typing import Optional


class User:
    Id: int
    Fio: Optional[str] = None
    Group: Optional[str] = None
    CountGavr: Optional[str] = None
    CountFMBA: Optional[str] = None
    SumCount: Optional[int] = None
    LastGavr: Optional[datetime.date] = None
    LastFMBA: Optional[datetime.date] = None
    Contacts: Optional[str] = None
    PhoneNumber: Optional[str] = None
    IsAdmin: int
    Registry: Optional[int] = None
    Tgid: Optional[str] = None

    def __init__(self):
        pass


class Donation:
    Id: int
    Uid: Optional[int] = None
    DonPlace: Optional[str] = None
    DonDate: Optional[datetime.date] = None

    def __init__(self):
        pass

class Question:
    Id: int
    Uid: int
    QuestionMsg: str

    def __init__(self):
        pass

class UpcomingEvent:
    Id: int
    DonPlace: str
    DonDate: datetime.date

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
