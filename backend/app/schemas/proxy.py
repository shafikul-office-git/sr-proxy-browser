from pydantic import BaseModel

class ProxyCheckRequest(BaseModel):
    ip: str
    port: int
    user: str | None = None
    password: str | None = None
    protocol: str = "http"
    timeout: int | None = 10