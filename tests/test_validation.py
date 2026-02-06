from validation import run_validations
from models.application import FAFSAApplication

# ---------- Valid application test ----------

def test_valid_application():
    valid_app = FAFSAApplication(
        studentInfo={
            "firstName": "Jane",
            "lastName": "Smith",
            "ssn": "123456789",
            "dateOfBirth": "2003-05-15"
        },
        dependencyStatus="dependent",
        maritalStatus="single",
        household={
            "numberInHousehold": 4,
            "numberInCollege": 1
        },
        income={
            "studentIncome": 5000,
            "parentIncome": 65000
        },
        stateOfResidence="CA"
    )

    result = run_validations(valid_app)

    assert result["valid"] is True
    assert all(r.passed for r in result["results"])


# ---------- Invalid application test ----------

def test_invalid_application():
    invalid_app = FAFSAApplication(
        studentInfo={
            "firstName": "John",
            "lastName": "Doe",
            "ssn": "invalid",
            "dateOfBirth": "2015-01-01"
        },
        dependencyStatus="dependent",
        maritalStatus="married",
        household={
            "numberInHousehold": 2,
            "numberInCollege": 5
        },
        income={
            "studentIncome": -1000
        },
        stateOfResidence="XX"
    )

    result = run_validations(invalid_app)

    assert result["valid"] is False

    failed_rules = [r for r in result["results"] if not r.passed]
    assert len(failed_rules) > 0
