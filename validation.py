from datetime import date
import re
from models.application import FAFSAApplication
from models.validation import RuleResult

def make_result(rule_id, passed, message, severity="ERROR"):
    return RuleResult(
        ruleId=rule_id,
        passed=passed,
        message=message,
        severity=severity
    )

def validate_student_age(app: FAFSAApplication) -> RuleResult:
    age = (date.today() - app.studentInfo.dateOfBirth).days // 365
    passed = age >= 14

    return make_result(
        "AGE_001",
        passed,
        "Student must be at least 14 years old"
    )

def validate_ssn_format(app: FAFSAApplication) -> RuleResult:
    passed = bool(re.fullmatch(r"\d{9}", app.studentInfo.ssn))

    return make_result(
        "SSN_001",
        passed,
        "SSN must contain exactly 9 digits"
    )

def validate_parent_income(app: FAFSAApplication) -> RuleResult:
    if app.dependencyStatus != "dependent":
        return make_result(
            "INC_001",
            True,
            "Parent income not required for independent students"
        )

    passed = app.income.parentIncome is not None

    return make_result(
        "INC_001",
        passed,
        "Parent income is required for dependent students"
    )

def validate_income_non_negative(app: FAFSAApplication) -> RuleResult:
    incomes = [
        app.income.studentIncome,
        app.income.parentIncome
    ]

    passed = all(i is None or i >= 0 for i in incomes)

    return make_result(
        "INC_002",
        passed,
        "Income values cannot be negative"
    )

def validate_household_logic(app: FAFSAApplication) -> RuleResult:
    passed = (
        app.household.numberInCollege
        <= app.household.numberInHousehold
    )

    return make_result(
        "HOU_001",
        passed,
        "Number in college cannot exceed number in household"
    )

VALID_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
}

def validate_state_code(app: FAFSAApplication) -> RuleResult:
    passed = app.stateOfResidence in VALID_STATES

    return make_result(
        "STATE_001",
        passed,
        "State must be a valid US state abbreviation"
    )

def validate_marital_status(app: FAFSAApplication) -> RuleResult:
    if app.maritalStatus != "married":
        return make_result(
            "MAR_001",
            True,
            "Spouse information not required if not married"
        )

    return make_result(
        "MAR_001",
        False,
        "Spouse information is required when marital status is married"
    )

VALIDATIONS = [
    validate_student_age,
    validate_ssn_format,
    validate_parent_income,
    validate_income_non_negative,
    validate_household_logic,
    validate_state_code,
    validate_marital_status,
]

def run_validations(app: FAFSAApplication):
    results = [v(app) for v in VALIDATIONS]

    valid = all(
        r.passed for r in results if r.severity == "ERROR"
    )

    return {
        "valid": valid,
        "results": results
    }
