import enum

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator, EmailStr


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class UserRegistration(BaseModel):
    username: str = Field(max_length=50)
    role: RoleEnum = RoleEnum.USER
    first_name: str = Field(max_length=20)
    last_name: str | None = Field(default=None, max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @field_validator("email", "username", "first_name", "last_name")
    @classmethod
    def validate_fields(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserResponse(BaseModel):
    id: int
    username: str
    role: RoleEnum
    first_name: str
    last_name: str | None
    email: EmailStr
    password_hash: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, max_length=50)
    first_name: str | None = Field(default=None, max_length=20)
    last_name: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    confirm_password: str | None = Field(default=None, min_length=8, max_length=128)

    @field_validator("email", "username", "first_name", "last_name")
    @classmethod
    def validate_fields(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip() if v is not None else v

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password is not None or self.confirm_password is not None:
            if self.password != self.confirm_password:
                raise ValueError("Passwords do not match")
        return self
