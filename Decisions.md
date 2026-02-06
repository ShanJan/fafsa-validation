# Architectural and Design Decisions

This document explains the key design decisions made while implementing the FAFSA Validation Service. The goal is to make the reasoning behind the implementation clear.

---

## Why FastAPI

FastAPI was chosen because:

* It provides automatic JSON parsing and validation
* It integrates tightly with Pydantic models
* It generates interactive API documentation automatically (Swagger)
* It requires very little boilerplate

This makes it well-suited for small, clear HTTP services like this one. And also saves a lot of time. 

---

## Why Pydantic Models

Pydantic models are used to define:

* The shape of incoming FAFSA application data
* The structure of validation results

Benefits:

* Automatic type validation
* Clear error messages for invalid input

The input models match the provided JSON structure exactly to minimize transformation logic.

---

## Why Validation Functions Instead of Classes

All validation rules are implemented as simple Python functions instead of individual classes.

This decision was made because:

* The number of rules is small (7 total)
* Each rule is simple and stateless
* Functions are easier to read
* Functions are easier to test
* Quick Solution for the time limit

If the rule set grows significantly, this approach can be refactored into a class-based system. 

---

## Why a Single Validation File

All validation rules live in `validation.py`.

This keeps:

* All business logic in one place
* The rule execution order explicit
* The code easy to navigate
* No need to over-complicate a simple task

For a take-home assignment, clarity and simplicity were prioritized over maximum extensibility.

---

## Severity Levels

Each validation rule returns a severity level (currently `ERROR`).

The overall application validity is determined by checking whether any ERROR-level rules failed.

This allows for future extension (e.g., warnings that do not block submission).

This is also mostly for logging and not for a proper response for the client to see. 

---

## Testing Strategy

Validation logic is written as pure functions, which makes it easy to test without running the API.

Tests focus on:

* Individual rule behavior
* End-to-end validation of valid and invalid applications

The FastAPI layer itself is thin and intentionally left mostly untested, as it delegates work to the validation layer.

---

## Summary

The design favors:

* Readability
* Simplicity
* Explicit behavior
* Ease of explanation