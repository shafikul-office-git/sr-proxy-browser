from pydantic import BaseModel

class ProxyCheckRequest(BaseModel):
    host: str
    port: int
    username: str | None = None
    password: str | None = None
    protocol: str = "http"
    timeout: int | None = 10