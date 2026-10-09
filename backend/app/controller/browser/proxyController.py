import requests, time
from urllib.parse import quote
from utility.response_config import json_response
import httpx

class ProxyController:
    def __init__(self):
        pass

    async def check_proxy_status(self, data):
        try:
            protocol = data.protocol.lower().strip()

            if protocol not in {"http", "https", "socks4", "socks5", "socks5h"}:
                return {"data": None, "status": False, "error": "Invalid protocol", "code": 400, }

            auth_part = ""
            if data.user and data.password:
                auth_part = (f"{quote(str(data.user), safe='')}:" f"{quote(str(data.password), safe='')}@")
                # auth_part = f"{quote(str(data.user))}:{quote(str(data.password))}@"


            proxy_url = f"{protocol}://{auth_part}{data.ip}:{data.port}"

            timeout = httpx.Timeout(data.timeout)

            async with httpx.AsyncClient(proxy=proxy_url, timeout=timeout) as client:
                start_time = time.perf_counter()

                response = await client.get("https://api.ipify.org?format=json")
                response.raise_for_status()

                proxy_ip = response.json().get("ip")
                response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

            if not proxy_ip:
                return {"data": None, "status": False, "error": "Proxy IP not returned", "code": 502}

            # Check direct IP without proxy
            direct_ip = None

            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.get("https://api.ipify.org?format=json")
                    response.raise_for_status()
                    direct_ip = response.json().get("ip")
            except httpx.HTTPError:
                pass

            return {
                "data": {
                    "is_working": True,
                    "proxy_ip": proxy_ip,
                    "response_time_ms": response_time_ms,
                    "direct_ip": direct_ip,
                    "ip_changed": (direct_ip != proxy_ip if direct_ip else None),
                },
                "status": True,
                "message": "Proxy checked successfully",
                "code": 200,
            }

        except httpx.TimeoutException as e:
            return {"data": None, "status": False, "error": str(e) or "Proxy connection timed out", "code": 504,}

        except httpx.HTTPError as e:
            return {"data": None, "status": False, "error": str(e) or "Proxy connection failed", "code": 502,}

        except (ValueError, TypeError, AttributeError) as e:
            return {"data": None, "status": False, "error": str(e), "code": 400,}
