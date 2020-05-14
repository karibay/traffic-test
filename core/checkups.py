from abc import ABC, abstractmethod

from .utils import personal_number_is_ie
from .exceptions import AmountNotInRangeException, AgeNotInRangeException, UserIsIEException, UserIsBlackListedException
from .models import BlackList

class BaseChekup(ABC):
    def __init__(self, application):
        self.application = application

    @abstractmethod
    def perform_check(self):
        pass


class ProgramChekup(BaseChekup):
    def perform_check(self):
        if self.application.amount not in self.application.program.amount_range:
            print(self.application.amount)
            raise AmountNotInRangeException()
        if self.application.applied_by.age not in self.application.program.age_range:
            raise AgeNotInRangeException()


class IECheckup(BaseChekup):
    def perform_check(self):
        print(self.application.applied_by.personal_number)
        if personal_number_is_ie(self.application.applied_by.personal_number):
            raise UserIsIEException()


class BlackListCheckup(BaseChekup):
    def perform_check(self):
        if BlackList.objects.filter(personal_number=self.application.applied_by.personal_number).exists():
            raise UserIsBlackListedException()
