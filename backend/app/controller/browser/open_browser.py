
import subprocess
from utility.helper_function import check_chrome_installed

def open_browser(debug_port, profile_path, proxy_info=None):
    chrome_check = check_chrome_installed()
    if not chrome_check['status']:
        return {"message": "Google Chrome is not installed on this system."}
    
    chrome_path = chrome_check['path']
    chrome_args = [
        chrome_path,
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={profile_path}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--disable-client-side-phishing-detection",
        "--disable-webrtc",
        "--disable-webrtc-encryption,"
        "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
        "--webrtc-ip-handling-policy=disable_non_proxied_udp",
        "--disable-media-stream"

        # "--disable-extensions",      # Extensions লোড করবেন না
        # "--disable-sync",            # Chrome Sync অক্ষম করুন
        # "--disable-plugins"          # Plugins লোড করবেন না

    ]

    proxy_info = proxy_info or {}
    proxy_host = proxy_info.get("proxy_host")
    proxy_port = proxy_info.get("proxy_port")
    proxy_username = proxy_info.get("proxy_username")
    proxy_password = proxy_info.get("proxy_password")

    if proxy_host and proxy_port:
        # if proxy_username and proxy_password:
        #     proxy_server = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
        # else:
        proxy_server = f"http://{proxy_host}:{proxy_port}"
        chrome_args.append(f"--proxy-server={proxy_server}")

    try:
        subprocess.Popen(chrome_args)
        return {
            "message": "Google Chrome has been opened successfully.",
            "debug_port": debug_port,
            "debug_url": f"http://localhost:{debug_port}"
        }
    # https://browserleaks.com/webrtc
    # https://ip8.com/
    except Exception as e:
        return {"message": f"Error opening Chrome: {str(e)}"}

