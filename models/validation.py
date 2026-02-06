from pydantic import BaseModel
from typing import List

class RuleResult(BaseModel):
    ruleId: str
    passed: bool
    message: str
    severity: str  # ERROR or WARNING

class ValidationResponse(BaseModel):
    valid: bool
    results: List[RuleResult]
