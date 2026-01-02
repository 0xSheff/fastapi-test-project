from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints, field_validator
from password_strength import PasswordPolicy

from apps.core.schemas import IdSchema


class UserPasswordSchema(BaseModel):
    password: str = Field(examples=["H12fghjhh_+"])

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        password_policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
        )

        errors = password_policy.test(value)
        if not errors:
            return value

        error_messages = []
        for error in errors:
            error_name = error.name()
            if error_name == "length":
                error_messages.append(f"Password must be at least {error.length} characters")
            elif error_name == "uppercase":
                error_messages.append(f"Password must contain at least {error.count} uppercase letter(s)")
            elif error_name == "numbers":
                error_messages.append(f"Password must contain at least {error.count} didit(s)")
            elif error_name == "special":
                error_messages.append(f"Password must contain at least {error.count} special character(s)")
        raise ValueError("; ".join(error_messages))


class BaseUserSchema(BaseModel):
    email: EmailStr = Field(description="Email of the user", examples=["example@mail.com"])
    name: Annotated[
        str,
        StringConstraints(
            pattern="^[a-zA-Z0-9_-]+$",
            strip_whitespace=True,
            min_length=3,
            max_length=50,
        )
    ] = Field(examples=["Casper_19"])


class RegisterUserSchema(BaseUserSchema, UserPasswordSchema):
    pass


class RegisteredUserSchema(IdSchema, BaseUserSchema):
    pass
