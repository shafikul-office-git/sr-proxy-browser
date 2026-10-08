
from passlib.context import CryptContext

# Argon2 use (no length limit)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    "Password hash  (SHA256 no use)"
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    "Password verify"
    return pwd_context.verify(plain, hashed)



import os, requests,random,socket, time

from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Argon2 use (no length limit)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def human_delay(min_seconds=3, max_seconds=7):
    """Pauses for a random amount of time to mimic human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def hash_password(password: str) -> str:
    "Password hash  (SHA256 no use)"
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    "Password verify"
    return pwd_context.verify(plain, hashed)

def is_value_exists(db: Session, model, column, value) -> bool:
    """
    Check if a value already exists in a specific column
    """
    return db.query(model).filter(column == value).first() is not None


def check_chrome_installed():
    """
    Check if Chrome is already installed in the system or not
    """
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    for path in chrome_paths:
        if os.path.isfile(path):
            return { 'path': path, 'status': True }
            
    return { 'status': False }

def get_timezone_from_ip(ip_address):
    """
    Try multiple free IP geolocation APIs in order.
    Falls back to next provider on failure.
    Returns default (Bangladesh) if all fail.
    """

    # ── Provider 1: ip-api.com ──────────────────────────────────────────────
    try:
        r = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5).json()
        if r.get("status") == "success":
            return r
    except Exception as e:
        print(f"[ip-api.com] failed: {e}")

    # ── Provider 2: ipapi.co ────────────────────────────────────────────────
    try:
        r = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5).json()
        if r.get("timezone") and not r.get("error"):
            return {
                "status":     "success",
                "country":    r.get("country_name"),
                "countryCode":r.get("country_code"),
                "region":     r.get("region_code"),
                "regionName": r.get("region"),
                "city":       r.get("city"),
                "zip":        r.get("postal"),
                "lat":        r.get("latitude"),
                "lon":        r.get("longitude"),
                "timezone":   r.get("timezone"),
                "isp":        r.get("org"),
                "org":        r.get("org"),
                "as":         r.get("asn"),
                "query":      ip_address,
            }
    except Exception as e:
        print(f"[ipapi.co] failed: {e}")

    # ── Provider 3: ip.sb ──────────────────────────────────────────────────
    try:
        r = requests.get(f"https://api.ip.sb/geoip/{ip_address}", timeout=5).json()
        if r.get("timezone"):
            return {
                "status":     "success",
                "country":    r.get("country"),
                "countryCode":r.get("country_code"),
                "region":     r.get("region_code"),
                "regionName": r.get("region"),
                "city":       r.get("city"),
                "zip":        r.get("postal_code"),
                "lat":        r.get("latitude"),
                "lon":        r.get("longitude"),
                "timezone":   r.get("timezone"),
                "isp":        r.get("isp"),
                "org":        r.get("organization"),
                "as":         r.get("asn"),
                "query":      ip_address,
            }
    except Exception as e:
        print(f"[ip.sb] failed: {e}")

    # ── Provider 4: freeipapi.com ──────────────────────────────────────────
    try:
        r = requests.get(f"https://freeipapi.com/api/json/{ip_address}", timeout=5).json()
        if r.get("timeZone"):
            return {
                "status":     "success",
                "country":    r.get("countryName"),
                "countryCode":r.get("countryCode"),
                "region":     r.get("regionCode"),
                "regionName": r.get("regionName"),
                "city":       r.get("cityName"),
                "zip":        r.get("zipCode"),
                "lat":        r.get("latitude"),
                "lon":        r.get("longitude"),
                "timezone":   r.get("timeZone"),
                "isp":        None,
                "org":        None,
                "as":         None,
                "query":      ip_address,
            }
    except Exception as e:
        print(f"[freeipapi.com] failed: {e}")

    # ── Default fallback ───────────────────────────────────────────────────
    print("[fallback] All providers failed. Returning default (Bangladesh).")
    return {
        "status":     "success",
        "country":    "Bangladesh",
        "countryCode":"BD",
        "region":     "C",
        "regionName": "Dhaka Division",
        "city":       "Dhaka",
        "zip":        "1216",
        "lat":        23.8233,
        "lon":        90.365,
        "timezone":   "Asia/Dhaka",
        "isp":        "Ranks Telecom Ltd.",
        "org":        "Ranks Telecom Ltd",
        "as":         "AS38210 Ranks Telecom Limited",
        "query":      "202.72.235.29",
    }


def get_chrome_version():
    response = requests.get("https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Windows", timeout=5).json()
    if response and isinstance(response, list) and len(response) > 0:
        return response
    
def build_fingerprint():
    """
    Generate random but realistic fingerprint values
    """

    screen_sizes = [
        (1920, 1080),
        (1366, 768),
        (1536, 864),
        (1440, 900),
        (1600, 900)
    ]

    gpu_profiles = [
        ("Intel Inc.", "Intel Iris OpenGL Engine"),
        ("NVIDIA Corporation", "NVIDIA GeForce GTX 1660"),
        ("ATI Technologies Inc.", "AMD Radeon Pro"),
    ]


    width, height = random.choice(screen_sizes)
    webgl_vendor, webgl_renderer = random.choice(gpu_profiles)

    user_agents = get_chrome_version()
    chrome_version = user_agents[random.randint(0, len(user_agents)-2)]["version"] if user_agents else "148.0.7778.180"
    user_agent =  f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"

    return {
        "width": width,
        "height": height,
        "device_memory": random.choice([4, 8, 16, 32]),
        "hardware_concurrency": random.choice([8, 4, 6, 8, 6]),
        "webgl_vendor": webgl_vendor,
        "webgl_renderer": webgl_renderer,
        "user_agent": user_agent,
        "chrome_version": chrome_version,
        "platform": random.choice(["Win32", "Win64"])
    }

def get_languages(country_code):

    LANGUAGE_BY_COUNTRY = {
        # ── Americas ──────────────────────────────────────────────────────
        "US": {"language": "en-US", "languages": ["en-US", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CA": {"language": "en-CA", "languages": ["en-CA", "fr-CA", "en", "fr"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MX": {"language": "es-MX", "languages": ["es-MX", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BR": {"language": "pt-BR", "languages": ["pt-BR", "pt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "AR": {"language": "es-AR", "languages": ["es-AR", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CL": {"language": "es-CL", "languages": ["es-CL", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CO": {"language": "es-CO", "languages": ["es-CO", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PE": {"language": "es-PE", "languages": ["es-PE", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "VE": {"language": "es-VE", "languages": ["es-VE", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "EC": {"language": "es-EC", "languages": ["es-EC", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BO": {"language": "es-BO", "languages": ["es-BO", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PY": {"language": "es-PY", "languages": ["es-PY", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "UY": {"language": "es-UY", "languages": ["es-UY", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "GY": {"language": "en-GY", "languages": ["en-GY", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SR": {"language": "nl-SR", "languages": ["nl-SR", "nl", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CU": {"language": "es-CU", "languages": ["es-CU", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "DO": {"language": "es-DO", "languages": ["es-DO", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PR": {"language": "es-PR", "languages": ["es-PR", "en-PR", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "GT": {"language": "es-GT", "languages": ["es-GT", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "HN": {"language": "es-HN", "languages": ["es-HN", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SV": {"language": "es-SV", "languages": ["es-SV", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "NI": {"language": "es-NI", "languages": ["es-NI", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CR": {"language": "es-CR", "languages": ["es-CR", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PA": {"language": "es-PA", "languages": ["es-PA", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "JM": {"language": "en-JM", "languages": ["en-JM", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "TT": {"language": "en-TT", "languages": ["en-TT", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "HT": {"language": "fr-HT", "languages": ["fr-HT", "ht", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BB": {"language": "en-BB", "languages": ["en-BB", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BS": {"language": "en-BS", "languages": ["en-BS", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BZ": {"language": "en-BZ", "languages": ["en-BZ", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},

        # ── Europe ────────────────────────────────────────────────────────
        "GB": {"language": "en-GB", "languages": ["en-GB", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "FR": {"language": "fr-FR", "languages": ["fr-FR", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "DE": {"language": "de-DE", "languages": ["de-DE", "de", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "IT": {"language": "it-IT", "languages": ["it-IT", "it", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ES": {"language": "es-ES", "languages": ["es-ES", "es", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PT": {"language": "pt-PT", "languages": ["pt-PT", "pt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "NL": {"language": "nl-NL", "languages": ["nl-NL", "nl", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BE": {"language": "nl-BE", "languages": ["nl-BE", "fr-BE", "de-BE", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CH": {"language": "de-CH", "languages": ["de-CH", "fr-CH", "it-CH", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "AT": {"language": "de-AT", "languages": ["de-AT", "de", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SE": {"language": "sv-SE", "languages": ["sv-SE", "sv", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "NO": {"language": "nb-NO", "languages": ["nb-NO", "nn-NO", "no", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "DK": {"language": "da-DK", "languages": ["da-DK", "da", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "FI": {"language": "fi-FI", "languages": ["fi-FI", "sv-FI", "fi", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PL": {"language": "pl-PL", "languages": ["pl-PL", "pl", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CZ": {"language": "cs-CZ", "languages": ["cs-CZ", "cs", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SK": {"language": "sk-SK", "languages": ["sk-SK", "sk", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "HU": {"language": "hu-HU", "languages": ["hu-HU", "hu", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "RO": {"language": "ro-RO", "languages": ["ro-RO", "ro", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BG": {"language": "bg-BG", "languages": ["bg-BG", "bg", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "HR": {"language": "hr-HR", "languages": ["hr-HR", "hr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "RS": {"language": "sr-RS", "languages": ["sr-RS", "sr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SI": {"language": "sl-SI", "languages": ["sl-SI", "sl", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BA": {"language": "bs-BA", "languages": ["bs-BA", "hr-BA", "sr-BA", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ME": {"language": "sr-ME", "languages": ["sr-ME", "sr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MK": {"language": "mk-MK", "languages": ["mk-MK", "mk", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "AL": {"language": "sq-AL", "languages": ["sq-AL", "sq", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "GR": {"language": "el-GR", "languages": ["el-GR", "el", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "RU": {"language": "ru-RU", "languages": ["ru-RU", "ru", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "UA": {"language": "uk-UA", "languages": ["uk-UA", "uk", "ru", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BY": {"language": "be-BY", "languages": ["be-BY", "ru-BY", "be", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MD": {"language": "ro-MD", "languages": ["ro-MD", "ru-MD", "ro", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "LT": {"language": "lt-LT", "languages": ["lt-LT", "lt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "LV": {"language": "lv-LV", "languages": ["lv-LV", "lv", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "EE": {"language": "et-EE", "languages": ["et-EE", "et", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "IS": {"language": "is-IS", "languages": ["is-IS", "is", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "IE": {"language": "en-IE", "languages": ["en-IE", "ga-IE", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MT": {"language": "mt-MT", "languages": ["mt-MT", "en-MT", "mt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CY": {"language": "el-CY", "languages": ["el-CY", "tr-CY", "el", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "LU": {"language": "lb-LU", "languages": ["lb-LU", "fr-LU", "de-LU", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "LI": {"language": "de-LI", "languages": ["de-LI", "de", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MC": {"language": "fr-MC", "languages": ["fr-MC", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SM": {"language": "it-SM", "languages": ["it-SM", "it", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "VA": {"language": "it-VA", "languages": ["it-VA", "la", "it", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "AD": {"language": "ca-AD", "languages": ["ca-AD", "ca", "es", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "XK": {"language": "sq-XK", "languages": ["sq-XK", "sr-XK", "sq", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},

        # ── Middle East ───────────────────────────────────────────────────
        "SA": {"language": "ar-SA", "languages": ["ar-SA", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "AE": {"language": "ar-AE", "languages": ["ar-AE", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "QA": {"language": "ar-QA", "languages": ["ar-QA", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "KW": {"language": "ar-KW", "languages": ["ar-KW", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "BH": {"language": "ar-BH", "languages": ["ar-BH", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "OM": {"language": "ar-OM", "languages": ["ar-OM", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "YE": {"language": "ar-YE", "languages": ["ar-YE", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "IQ": {"language": "ar-IQ", "languages": ["ar-IQ", "ku-IQ", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "SY": {"language": "ar-SY", "languages": ["ar-SY", "ku-SY", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "LB": {"language": "ar-LB", "languages": ["ar-LB", "fr-LB", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "JO": {"language": "ar-JO", "languages": ["ar-JO", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "PS": {"language": "ar-PS", "languages": ["ar-PS", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "IL": {"language": "he-IL", "languages": ["he-IL", "ar-IL", "he", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "David", "Frank Ruehl", "Miriam"]},
        "TR": {"language": "tr-TR", "languages": ["tr-TR", "tr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "IR": {"language": "fa-IR", "languages": ["fa-IR", "fa", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Traditional Arabic", "Simplified Arabic"]},

        # ── Asia ──────────────────────────────────────────────────────────
        "CN": {"language": "zh-CN", "languages": ["zh-CN", "zh", "en"], "fonts": ["Arial", "Times New Roman", "Microsoft YaHei", "SimSun", "SimHei", "NSimSun"]},
        "TW": {"language": "zh-TW", "languages": ["zh-TW", "zh", "en"], "fonts": ["Arial", "Times New Roman", "Microsoft JhengHei", "MingLiU", "PMingLiU"]},
        "HK": {"language": "zh-HK", "languages": ["zh-HK", "en-HK", "zh", "en"], "fonts": ["Arial", "Times New Roman", "Microsoft JhengHei", "MingLiU_HKSCS"]},
        "MO": {"language": "zh-MO", "languages": ["zh-MO", "pt-MO", "zh", "en"], "fonts": ["Arial", "Times New Roman", "Microsoft JhengHei", "MingLiU_HKSCS"]},
        "JP": {"language": "ja-JP", "languages": ["ja-JP", "ja", "en"], "fonts": ["Arial", "Times New Roman", "Meiryo", "Yu Gothic", "MS Gothic", "MS Mincho", "MS PGothic"]},
        "KR": {"language": "ko-KR", "languages": ["ko-KR", "ko", "en"], "fonts": ["Arial", "Times New Roman", "Malgun Gothic", "Gulim", "Batang", "Dotum"]},
        "KP": {"language": "ko-KP", "languages": ["ko-KP", "ko"], "fonts": ["Arial", "Times New Roman", "Malgun Gothic", "Gulim"]},
        "IN": {"language": "hi-IN", "languages": ["hi-IN", "en-IN", "hi", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Nirmala UI", "Mangal", "Kokila"]},
        "PK": {"language": "ur-PK", "languages": ["ur-PK", "en-PK", "ur", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Nirmala UI", "Traditional Arabic", "Urdu Typesetting"]},
        "BD": {"language": "bn-BD", "languages": ["bn-BD", "bn", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Nirmala UI", "Vrinda", "Shonar Bangla"]},
        "LK": {"language": "si-LK", "languages": ["si-LK", "ta-LK", "si", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Nirmala UI", "Iskoola Pota"]},
        "NP": {"language": "ne-NP", "languages": ["ne-NP", "ne", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Nirmala UI", "Mangal"]},
        "BT": {"language": "dz-BT", "languages": ["dz-BT", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Nirmala UI"]},
        "MV": {"language": "dv-MV", "languages": ["dv-MV", "dv", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "MV Boli"]},
        "AF": {"language": "fa-AF", "languages": ["fa-AF", "ps-AF", "fa", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Traditional Arabic", "Simplified Arabic"]},
        "MM": {"language": "my-MM", "languages": ["my-MM", "my", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Myanmar Text", "Padauk"]},
        "TH": {"language": "th-TH", "languages": ["th-TH", "th", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Leelawadee UI", "Tahoma", "Cordia New"]},
        "VN": {"language": "vi-VN", "languages": ["vi-VN", "vi", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "KH": {"language": "km-KH", "languages": ["km-KH", "km", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Leelawadee UI", "Khmer UI"]},
        "LA": {"language": "lo-LA", "languages": ["lo-LA", "lo", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Leelawadee UI", "Lao UI"]},
        "MY": {"language": "ms-MY", "languages": ["ms-MY", "zh-MY", "ta-MY", "ms", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SG": {"language": "en-SG", "languages": ["en-SG", "zh-SG", "ms-SG", "ta-SG", "en"], "fonts": ["Arial", "Times New Roman", "Microsoft YaHei", "Nirmala UI", "Georgia"]},
        "ID": {"language": "id-ID", "languages": ["id-ID", "id", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PH": {"language": "fil-PH", "languages": ["fil-PH", "en-PH", "fil", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "TL": {"language": "pt-TL", "languages": ["pt-TL", "tet", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BN": {"language": "ms-BN", "languages": ["ms-BN", "ms", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MN": {"language": "mn-MN", "languages": ["mn-MN", "mn", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Mongolian Baiti"]},
        "KZ": {"language": "kk-KZ", "languages": ["kk-KZ", "ru-KZ", "kk", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "UZ": {"language": "uz-UZ", "languages": ["uz-UZ", "ru-UZ", "uz", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "TM": {"language": "tk-TM", "languages": ["tk-TM", "ru-TM", "tk", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "KG": {"language": "ky-KG", "languages": ["ky-KG", "ru-KG", "ky", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "TJ": {"language": "tg-TJ", "languages": ["tg-TJ", "ru-TJ", "tg", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "AZ": {"language": "az-AZ", "languages": ["az-AZ", "ru-AZ", "az", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "AM": {"language": "hy-AM", "languages": ["hy-AM", "hy", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sylfaen"]},
        "GE": {"language": "ka-GE", "languages": ["ka-GE", "ka", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sylfaen"]},

        # ── Africa ────────────────────────────────────────────────────────
        "EG": {"language": "ar-EG", "languages": ["ar-EG", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "LY": {"language": "ar-LY", "languages": ["ar-LY", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "TN": {"language": "ar-TN", "languages": ["ar-TN", "fr-TN", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "DZ": {"language": "ar-DZ", "languages": ["ar-DZ", "fr-DZ", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "MA": {"language": "ar-MA", "languages": ["ar-MA", "fr-MA", "tzm", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "SD": {"language": "ar-SD", "languages": ["ar-SD", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "SS": {"language": "en-SS", "languages": ["en-SS", "ar-SS", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ET": {"language": "am-ET", "languages": ["am-ET", "om-ET", "am", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Nyala"]},
        "ER": {"language": "ti-ER", "languages": ["ti-ER", "ar-ER", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Nyala"]},
        "SO": {"language": "so-SO", "languages": ["so-SO", "ar-SO", "so", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima"]},
        "DJ": {"language": "fr-DJ", "languages": ["fr-DJ", "ar-DJ", "so-DJ", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima"]},
        "KE": {"language": "sw-KE", "languages": ["sw-KE", "en-KE", "sw", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "UG": {"language": "sw-UG", "languages": ["sw-UG", "en-UG", "sw", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "TZ": {"language": "sw-TZ", "languages": ["sw-TZ", "en-TZ", "sw", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "RW": {"language": "rw-RW", "languages": ["rw-RW", "fr-RW", "en-RW", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "BI": {"language": "rn-BI", "languages": ["rn-BI", "fr-BI", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "NG": {"language": "en-NG", "languages": ["en-NG", "ha-NG", "yo-NG", "ig-NG", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "GH": {"language": "en-GH", "languages": ["en-GH", "ak-GH", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "SN": {"language": "fr-SN", "languages": ["fr-SN", "wo-SN", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "CI": {"language": "fr-CI", "languages": ["fr-CI", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "CM": {"language": "fr-CM", "languages": ["fr-CM", "en-CM", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "CD": {"language": "fr-CD", "languages": ["fr-CD", "sw-CD", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "CG": {"language": "fr-CG", "languages": ["fr-CG", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "AO": {"language": "pt-AO", "languages": ["pt-AO", "pt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MZ": {"language": "pt-MZ", "languages": ["pt-MZ", "pt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ZA": {"language": "en-ZA", "languages": ["en-ZA", "af-ZA", "zu-ZA", "xh-ZA", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ZW": {"language": "en-ZW", "languages": ["en-ZW", "sn-ZW", "nd-ZW", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ZM": {"language": "en-ZM", "languages": ["en-ZM", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MW": {"language": "en-MW", "languages": ["en-MW", "ny-MW", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "BW": {"language": "en-BW", "languages": ["en-BW", "tn-BW", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "NA": {"language": "en-NA", "languages": ["en-NA", "af-NA", "de-NA", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MG": {"language": "mg-MG", "languages": ["mg-MG", "fr-MG", "mg", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MU": {"language": "en-MU", "languages": ["en-MU", "fr-MU", "mfe", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SC": {"language": "fr-SC", "languages": ["fr-SC", "en-SC", "crs", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "GA": {"language": "fr-GA", "languages": ["fr-GA", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "GQ": {"language": "es-GQ", "languages": ["es-GQ", "fr-GQ", "pt-GQ", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ST": {"language": "pt-ST", "languages": ["pt-ST", "pt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CV": {"language": "pt-CV", "languages": ["pt-CV", "pt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "GW": {"language": "pt-GW", "languages": ["pt-GW", "pt", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "GN": {"language": "fr-GN", "languages": ["fr-GN", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SL": {"language": "en-SL", "languages": ["en-SL", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "LR": {"language": "en-LR", "languages": ["en-LR", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "ML": {"language": "fr-ML", "languages": ["fr-ML", "bm-ML", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "BF": {"language": "fr-BF", "languages": ["fr-BF", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "NE": {"language": "fr-NE", "languages": ["fr-NE", "ha-NE", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "TD": {"language": "fr-TD", "languages": ["fr-TD", "ar-TD", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic"]},
        "MR": {"language": "ar-MR", "languages": ["ar-MR", "fr-MR", "ar", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Sakkal Majalla", "Traditional Arabic", "Simplified Arabic"]},
        "GM": {"language": "en-GM", "languages": ["en-GM", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "TG": {"language": "fr-TG", "languages": ["fr-TG", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "BJ": {"language": "fr-BJ", "languages": ["fr-BJ", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "CF": {"language": "fr-CF", "languages": ["fr-CF", "sg-CF", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Ebrima", "Georgia"]},
        "KM": {"language": "ar-KM", "languages": ["ar-KM", "fr-KM", "sw-KM", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Traditional Arabic", "Simplified Arabic"]},
        "LS": {"language": "st-LS", "languages": ["st-LS", "en-LS", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SZ": {"language": "ss-SZ", "languages": ["ss-SZ", "en-SZ", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "IO": {"language": "en-IO", "languages": ["en-IO", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},

        # ── Oceania ───────────────────────────────────────────────────────
        "AU": {"language": "en-AU", "languages": ["en-AU", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "NZ": {"language": "en-NZ", "languages": ["en-NZ", "mi-NZ", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PG": {"language": "en-PG", "languages": ["en-PG", "ho-PG", "tpi", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "FJ": {"language": "en-FJ", "languages": ["en-FJ", "fj-FJ", "hi-FJ", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "SB": {"language": "en-SB", "languages": ["en-SB", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "VU": {"language": "bi-VU", "languages": ["bi-VU", "fr-VU", "en-VU", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "WS": {"language": "sm-WS", "languages": ["sm-WS", "en-WS", "sm", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "TO": {"language": "to-TO", "languages": ["to-TO", "en-TO", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "KI": {"language": "en-KI", "languages": ["en-KI", "gil", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "FM": {"language": "en-FM", "languages": ["en-FM", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PW": {"language": "pau-PW", "languages": ["pau-PW", "en-PW", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "MH": {"language": "mh-MH", "languages": ["mh-MH", "en-MH", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "NR": {"language": "na-NR", "languages": ["na-NR", "en-NR", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "TV": {"language": "tvl-TV", "languages": ["tvl-TV", "en-TV", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "CK": {"language": "en-CK", "languages": ["en-CK", "rar-CK", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "PF": {"language": "fr-PF", "languages": ["fr-PF", "ty-PF", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
        "NC": {"language": "fr-NC", "languages": ["fr-NC", "fr", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]},
    }

    return LANGUAGE_BY_COUNTRY.get(
        country_code,
        {"language": "en-US", "languages": ["en-US", "en"], "fonts": ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana"]}
    )

def get_random_free_port( min_port: int = 1024,max_port: int = 49151,max_retry: int = 100) -> int:

    EXCLUDED_PORTS = {4000, 8000, 4158}
    for _ in range(max_retry):

        port = random.randint(min_port, max_port)

        if port in EXCLUDED_PORTS:
            continue

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            try:
                sock.bind(("localhost", port))
                # sock.bind(("127.0.0.1", port))
                return port

            except OSError:
                continue

    raise RuntimeError("Could not find a free port")


