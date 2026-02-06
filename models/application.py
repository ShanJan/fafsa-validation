from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentInfo(BaseModel):
    firstName: str
    lastName: str
    ssn: str
    dateOfBirth: date

class HouseholdInfo(BaseModel):
    numberInHousehold: int
    numberInCollege: int

class IncomeInfo(BaseModel):
    studentIncome: float
    parentIncome: Optional[float] = None

class FAFSAApplication(BaseModel):
    studentInfo: StudentInfo
    dependencyStatus: str
    maritalStatus: str
    household: HouseholdInfo
    income: IncomeInfo
    stateOfResidence: str
