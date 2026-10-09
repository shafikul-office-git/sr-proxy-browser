import requests
from urllib.parse import quote


def check_proxy_status(
    ip: str,
    port: int | str,
    user: str | None = None,
    password: str | None = None,
    protocol: str = "http",
    timeout: int = 10,
) -> bool:
    """
    Returns:
        True  -> Proxy is working
        False -> Proxy is not working
    """

    try:
        protocol = protocol.lower().strip()

        if protocol not in {"http", "https", "socks4", "socks5", "socks5h"}:
            return False

        # Better DNS handling for SOCKS5
        if protocol == "socks5":
            protocol = "socks5h"

        auth_part = ""
        if user and password:
            auth_part = f"{quote(str(user))}:{quote(str(password))}@"

        proxy_url = f"{protocol}://{auth_part}{ip}:{port}"

        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }

        response = requests.get(
            "https://api.ipify.org?format=json",
            proxies=proxies,
            timeout=timeout,
        )

        response.raise_for_status()

        data = response.json()

        return bool(data.get("ip"))

    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.ProxyError,
        requests.exceptions.RequestException,
        ValueError,
    ):
        return False