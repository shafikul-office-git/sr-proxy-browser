from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class ProxyCheckRequest(BaseModel):
    host: str = Field(..., min_length=1, max_length=253)
    port: int = Field(..., ge=1, le=65535)
    username: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, max_length=255)
    protocol: Literal["http", "https", "socks4", "socks5"] = "http"
    timeout: int | None = Field(default=10, ge=1, le=120)

    @field_validator("host")
    @classmethod
    def validate_host(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Host cannot be empty")

        if any(char.isspace() for char in value):
            raise ValueError("Host cannot contain whitespace")

        return value

    @field_validator("username", "password")
    @classmethod
    def validate_credentials(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Credentials cannot be empty")

        return value

    @model_validator(mode="after")
    def validate_authentication(self):
        if (self.username is None) != (self.password is None):
            raise ValueError(
                "Username and password must be provided together"
            )

        return self