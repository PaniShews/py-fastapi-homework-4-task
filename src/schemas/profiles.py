from datetime import date

from fastapi import UploadFile, Form, File
from pydantic import BaseModel, field_validator

from validation import (
    validate_name,
    validate_image,
    validate_gender,
    validate_birth_date
)


class ProfileRequestSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: UploadFile

    model_config = {
        "arbitrary_types_allowed": True
    }

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, value: str) -> str:
        validate_name(value)
        return value.lower()

    @field_validator("info")
    @classmethod
    def validate_info(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Info field cannot be empty or contain only spaces.")
        return value

    @field_validator("gender")
    @classmethod
    def validate_gender_field(cls, value: str) -> str:
        validate_gender(value)
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date) -> date:
        validate_birth_date(value)
        return value

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, value: UploadFile) -> UploadFile:
        validate_image(value)
        return value

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        gender: str = Form(...),
        date_of_birth: date = Form(...),
        info: str = Form(...),
        avatar: UploadFile = File(...),
    ) -> "ProfileRequestSchema":
        return cls(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
            avatar=avatar,
        )


class ProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: str

    model_config = {
        "from_attributes": True
    }
