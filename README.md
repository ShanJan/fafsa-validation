# FAFSA Validation Service

This project implements a simple HTTP service that validates FAFSA application data using a set of business rules ("edits"). It is designed to be easy to read, easy to explain, and easy to extend.

The service is implemented using **FastAPI** and **Pydantic** and exposes a single validation endpoint.

---

## What This Service Does

* Accepts FAFSA application data as JSON via an HTTP API
* Applies a fixed set of validation rules
* Returns detailed validation results explaining:

  * Which rules passed or failed
  * Why a rule failed
  * Whether the application is overall valid

---

## Validation Rules Implemented

The service implements the following required rules:

1. Student must be at least 14 years old
2. Student SSN must be exactly 9 digits
3. Parent income is required if the student is dependent
4. Income values cannot be negative
5. Number in college cannot exceed number in household
6. State of residence must be a valid US state abbreviation
7. Spouse information is required if marital status is "married"

All rules are applied to every application, and failures are reported individually.

---

## Project Structure

```
fa fsa-validator/
│
├── main.py                # FastAPI application and HTTP endpoints
├── validation.py          # All validation rules and validation runner
├── models/
│   ├── application.py     # FAFSA input data models (Pydantic)
│   └── validation.py      # Validation response models
├── requirements.txt
```

Each file has a single responsibility:

* `main.py` handles HTTP only
* `validation.py` contains all business rules
* `models/` contains data definitions

---

## Running the Service

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Start the server

```
uvicorn main:app --reload
```

The service will be available at:

* [http://127.0.0.1:8000](http://127.0.0.1:8000)
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (interactive API documentation)

---

## Using the API

### Endpoint

```
POST /validate
```

### Example Request

```json
{
  "studentInfo": {
    "firstName": "Jane",
    "lastName": "Smith",
    "ssn": "123456789",
    "dateOfBirth": "2003-05-15"
  },
  "dependencyStatus": "dependent",
  "maritalStatus": "single",
  "household": {
    "numberInHousehold": 4,
    "numberInCollege": 1
  },
  "income": {
    "studentIncome": 5000,
    "parentIncome": 65000
  },
  "stateOfResidence": "CA"
}
```

### Example Response

```json
{
  "valid": true,
  "results": [
    {
      "ruleId": "AGE_001",
      "passed": true,
      "message": "Student must be at least 14 years old",
      "severity": "ERROR"
    }
  ]
}
```

---

## Testing

Basic automated tests can be run using `pytest`. See the documentation in `decisions.md` for details on the testing approach.

---
