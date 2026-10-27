
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, ConfigDict, model_validator


class ProfileForm(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    group: str = Field(default="No group", max_length=100)
    startPage: HttpUrl
    notes: str = Field(default="", max_length=2000)

    os: str = Field(min_length=1, max_length=50)
    browser: str = Field(min_length=1, max_length=50)

    userAgent: Literal["auto", "custom"] = "auto"
    customUserAgent: str = Field(default="", max_length=1000)

    screen: str = Field(min_length=1, max_length=30)
    language: str = Field(min_length=1, max_length=50)
    timezone: str = Field(min_length=1, max_length=100)

    webrtc: bool = True
    canvas: bool = True
    cookies: bool = True

    @model_validator(mode="after")
    def validate_user_agent(self):
        if self.userAgent == "custom" and not self.customUserAgent.strip():
            raise ValueError(
                "customUserAgent is required when userAgent is custom"
            )
        return self


class ProxyInfo(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    protocol: Literal["No proxy", "HTTP", "HTTPS", "SOCKS5", "SOCKS4"]
    host: str = Field(default="", max_length=253)
    port: int | None = Field(default=None, ge=1, le=65535)
    username: str = Field(default="", max_length=255)
    password: str = Field(default="", max_length=255)

    @model_validator(mode="after")
    def validate_proxy(self):
        if self.protocol == "No proxy":
            return self

        if not self.host:
            raise ValueError("Proxy host is required")

        if self.port is None:
            raise ValueError("Proxy port is required")

        return self


class ProfileCheckRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    env: str = Field(min_length=1, max_length=100)
    form: ProfileForm
    proxy: ProxyInfo
    launch: bool = False

    @model_validator(mode="after")
    def validate_environment(self):
        expected_env = f"{self.form.browser}, {self.form.os}"

        if self.env != expected_env:
            raise ValueError(
                f"env must be '{expected_env}'"
            )

        return self