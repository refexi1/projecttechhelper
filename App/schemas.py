import json
from pydantic import BaseModel, Field, ValidationError, field_validator


class TroubleshootingResponse(BaseModel):
    problem: str = Field(min_length=1)
    os_type: str = Field(min_length=1)
    steps: list[str] = Field(min_length=1)

    @field_validator("problem", "os_type")
    @classmethod
    def check_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text cannot be empty")
        return value.strip()

    @field_validator("steps")
    @classmethod
    def check_steps(cls, value: list[str]) -> list[str]:
        if any(not step.strip() for step in value):
            raise ValueError("Steps cannot be empty")
        return [step.strip() for step in value]


def validate_ai_response(response_text: str) -> dict:
    try:
        data = json.loads(response_text)
        result = TroubleshootingResponse.model_validate(data)

        return {
            "success": True,
            "data": result.model_dump(),
            "error": None,
        }

    except (json.JSONDecodeError, ValidationError, ValueError, TypeError) as error:
        return {
            "success": False,
            "data": None,
            "error": str(error),
        }
