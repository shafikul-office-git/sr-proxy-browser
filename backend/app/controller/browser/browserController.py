import random
import threading
import asyncio
import json
from playwright.sync_api import sync_playwright, BrowserContext, Page


# ================================================================
# STEALTH SCRIPT TEMPLATE — ফাংশন মাস্কিং লুকানোর বাইপাস সহ
# ================================================================

def build_stealth_script(browser_conf) -> str:
    fake_brands = ['Not/A)Brand', 'Not:A-Brand', 'Not_A Brand']
    chosen_fake_brand = random.choice(fake_brands)
    fake_version = str(random.randint(8, 99))
    chrome_major = browser_conf.chrome_version.split(".")[0]
    canvas = browser_conf.canvas_noise
    audio_noise = round(random.uniform(0.00001, 0.0001), 6)
    proxy_ip = browser_conf.ip_info.get('query', 'None')

    # জাভাস্ক্রিপ্ট এবং পাইথন সিনট্যাক্স এরর এড়াতে টেমপ্লেট মেথড ব্যবহার করা হয়েছে
    template = """
    (() => {
        const nativeToString = Function.prototype.toString;
        const spyMap = new WeakMap();

        // toString() এর মাধ্যমে মাস্কিং ডিটেকশন বাইপাস
        Function.prototype.toString = function toString() {
            if (spyMap.has(this)) {
                return spyMap.get(this);
            }
            return nativeToString.call(this);
        };

        // সাধারণ নেটিভ ফাংশন প্যাচ করার হেল্পার
        function patchNative(obj, key, fake) {
            const original = obj[key];
            if (original) {
                spyMap.set(fake, nativeToString.call(original));
                obj[key] = fake;
            }
        }

        // গেটার মেথড (যেমন webdriver, deviceMemory) প্যাচ করার হেল্পার
        function patchGetter(obj, key, fakeGet) {
            const descriptor = Object.getOwnPropertyDescriptor(obj, key);
            if (descriptor && descriptor.get) {
                spyMap.set(fakeGet, nativeToString.call(descriptor.get));
                Object.defineProperty(obj, key, {
                    ...descriptor,
                    get: fakeGet
                });
            } else {
                const fakeNativeString = "function get " + key + "() { [native code] }";
                spyMap.set(fakeGet, fakeNativeString);
                Object.defineProperty(obj, key, {
                    get: fakeGet,
                    configurable: true,
                    enumerable: true
                });
            }
        }

        // ── webdriver ──
        patchGetter(Navigator.prototype, 'webdriver', () => undefined);

        // ── hardware ──
        patchGetter(Navigator.prototype, 'hardwareConcurrency', () => __HARDWARE_CONCURRENCY__);
        patchGetter(Navigator.prototype, 'deviceMemory',        () => __DEVICE_MEMORY__);

        // ── language ──
        patchGetter(Navigator.prototype, 'language',  () => '__BROWSER_LANGUAGE__');
        patchGetter(Navigator.prototype, 'languages', () => __BROWSER_LANGUAGES__);
        patchGetter(Navigator.prototype, 'plugins',   () => [1, 2, 3, 4, 5]);

        // ── Screen Dimension Spoof (উইন্ডো সাইজ এবং স্ক্রিন সাইজ সামঞ্জস্য করা) ──
        patchGetter(Screen.prototype, 'width', () => __WINDOW_WIDTH__);
        patchGetter(Screen.prototype, 'height', () => __WINDOW_HEIGHT__);
        patchGetter(Screen.prototype, 'availWidth', () => __WINDOW_WIDTH__);
        patchGetter(Screen.prototype, 'availHeight', () => __WINDOW_HEIGHT__);

        // ── userAgentData ──
        const uaData = {
            brands: [
                { brand: '__CHOSEN_FAKE_BRAND__', version: '__FAKE_VERSION__' },
                { brand: 'Chromium',      version: '__CHROME_MAJOR__' },
                { brand: 'Google Chrome', version: '__CHROME_MAJOR__' }
            ],
            mobile: false,
            platform: 'Windows'
        };
        const fakeGetHighEntropy = function getHighEntropyValues(hints) {
            return Promise.resolve({
                brands: uaData.brands,
                mobile: uaData.mobile,
                platform: uaData.platform,
                platformVersion: "10.0.0",
                architecture: "x86",
                bitness: "64",
                model: ""
            });
        };
        spyMap.set(fakeGetHighEntropy, "function getHighEntropyValues() { [native code] }");
        uaData.getHighEntropyValues = fakeGetHighEntropy;
        patchGetter(Navigator.prototype, 'userAgentData', () => uaData);

        // ── WebGL spoof ──
        const makeWebGLGetParameter = (original) => {
            const fakeGetParameter = function getParameter(parameter) {
                if (parameter === 37445) return "__WEBGL_VENDOR__";
                if (parameter === 37446) return "__WEBGL_RENDERER__";
                return original.call(this, parameter);
            };
            return fakeGetParameter;
        };
        if (window.WebGLRenderingContext) {
            const origWebGL = WebGLRenderingContext.prototype.getParameter;
            patchNative(WebGLRenderingContext.prototype, 'getParameter', makeWebGLGetParameter(origWebGL));
        }
        if (window.WebGL2RenderingContext) {
            const origWebGL2 = WebGL2RenderingContext.prototype.getParameter;
            patchNative(WebGL2RenderingContext.prototype, 'getParameter', makeWebGLGetParameter(origWebGL2));
        }

        // ── Canvas noise ──
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        const fakeToDataURL = function toDataURL(...args) {
            const ctx = this.getContext('2d');
            if (ctx) {
                try {
                    const shift = { r: __CANVAS_R__, g: __CANVAS_G__, b: __CANVAS_B__, a: __CANVAS_A__ };
                    const imageData = ctx.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        if (imageData.data[i + 3] > 0) {
                            imageData.data[i]     = (imageData.data[i] + shift.r) % 256;
                            imageData.data[i + 1] = (imageData.data[i + 1] + shift.g) % 256;
                            imageData.data[i + 2] = (imageData.data[i + 2] + shift.b) % 256;
                        }
                    }
                    ctx.putImageData(imageData, 0, 0);
                } catch(e) {}
            }
            return originalToDataURL.apply(this, args);
        };
        patchNative(HTMLCanvasElement.prototype, 'toDataURL', fakeToDataURL);

        const originalToBlob = HTMLCanvasElement.prototype.toBlob;
        const fakeToBlob = function toBlob(callback, ...args) {
            const ctx = this.getContext('2d');
            if (ctx) {
                try {
                    const shift = { r: __CANVAS_R__, g: __CANVAS_G__, b: __CANVAS_B__, a: __CANVAS_A__ };
                    const imageData = ctx.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        if (imageData.data[i + 3] > 0) {
                            imageData.data[i]     = (imageData.data[i] + shift.r) % 256;
                            imageData.data[i + 1] = (imageData.data[i + 1] + shift.g) % 256;
                            imageData.data[i + 2] = (imageData.data[i + 2] + shift.b) % 256;
                        }
                    }
                    ctx.putImageData(imageData, 0, 0);
                } catch(e) {}
            }
            return originalToBlob.call(this, callback, ...args);
        };
        patchNative(HTMLCanvasElement.prototype, 'toBlob', fakeToBlob);

        // ── Audio Context spoof ──
        if (window.AudioBuffer) {
            const originalGetChannelData = AudioBuffer.prototype.getChannelData;
            const fakeGetChannelData = function getChannelData(channel) {
                const data = originalGetChannelData.call(this, channel);
                try {
                    for (let i = 0; i < data.length; i++) {
                        data[i] += __AUDIO_NOISE__ * (Math.random() - 0.5) * 0.00001;
                    }
                } catch(e) {}
                return data;
            };
            patchNative(AudioBuffer.prototype, 'getChannelData', fakeGetChannelData);
        }

        if (window.AnalyserNode) {
            const originalGetFloatFrequencyData = AnalyserNode.prototype.getFloatFrequencyData;
            const fakeGetFloatFrequencyData = function getFloatFrequencyData(array) {
                const res = originalGetFloatFrequencyData.call(this, array);
                try {
                    for (let i = 0; i < array.length; i++) {
                        array[i] += __AUDIO_NOISE__ * (Math.random() - 0.5);
                    }
                } catch(e) {}
                return res;
            };
            patchNative(AnalyserNode.prototype, 'getFloatFrequencyData', fakeGetFloatFrequencyData);
        }

        // ── WebRTC Spoofing (Local IP leaks এড়ানোর জন্য) ──
        if (window.RTCPeerConnection) {
            const origCreateOffer = RTCPeerConnection.prototype.createOffer;
            const fakeCreateOffer = function createOffer(...args) {
                return origCreateOffer.apply(this, args).then(offer => {
                    try {
                        const proxyIp = "__PROXY_IP__";
                        if (proxyIp && proxyIp !== "None") {
                            offer.sdp = offer.sdp.replace(/candidate:.+?\\s\\d+\\.\\d+\\.\\d+\\.\\d+\\s/g, `candidate:1 1 UDP 1 ${proxyIp} `);
                        }
                    } catch(e) {}
                    return offer;
                });
            };
            patchNative(RTCPeerConnection.prototype, 'createOffer', fakeCreateOffer);
        }
    })();
    """

    # ডাইনামিক ডাটা রিপ্লেসমেন্ট
    script = template
    script = script.replace('__HARDWARE_CONCURRENCY__', str(browser_conf.hardware_concurrency))
    script = script.replace('__DEVICE_MEMORY__', str(browser_conf.device_memory))
    script = script.replace('__BROWSER_LANGUAGE__', browser_conf.browser_language)
    script = script.replace('__BROWSER_LANGUAGES__', json.dumps(browser_conf.browser_languages))
    script = script.replace('__WINDOW_WIDTH__', str(browser_conf.window_width))
    script = script.replace('__WINDOW_HEIGHT__', str(browser_conf.window_height))
    script = script.replace('__CHOSEN_FAKE_BRAND__', chosen_fake_brand)
    script = script.replace('__FAKE_VERSION__', fake_version)
    script = script.replace('__CHROME_MAJOR__', chrome_major)
    script = script.replace('__WEBGL_VENDOR__', browser_conf.webgl_vendor)
    script = script.replace('__WEBGL_RENDERER__', browser_conf.webgl_renderer)
    script = script.replace('__CANVAS_R__', str(canvas['r']))
    script = script.replace('__CANVAS_G__', str(canvas['g']))
    script = script.replace('__CANVAS_B__', str(canvas['b']))
    script = script.replace('__CANVAS_A__', str(canvas['a']))
    script = script.replace('__AUDIO_NOISE__', str(audio_noise))
    script = script.replace('__PROXY_IP__', proxy_ip)

    return script


# ================================================================
# PROXY CONFIG
# ================================================================

def build_proxy_config(proxy_type: str, proxy_info: dict) -> dict | None:
    if not proxy_info or not proxy_info.get('proxy_host'):
        return None

    type_map = {
        'http':   'http',
        'https':  'http',
        'socks4': 'socks4',
        'socks5': 'socks5',
    }
    scheme = type_map.get(str(proxy_type).lower(), 'http')
    proxy_config = {
        "server": f"{scheme}://{proxy_info['proxy_host']}:{proxy_info['proxy_port']}"
    }
    u = proxy_info.get('proxy_username')
    pw = proxy_info.get('proxy_password')
    if u and pw:
        proxy_config["username"] = str(u)
        proxy_config["password"] = str(pw)
    return proxy_config


# ================================================================
# BROWSER THREAD
# ================================================================

def _browser_thread(
    debug_port, profile_path, browser_conf,
    proxy_type, proxy_info,
    result: dict, ready_event: threading.Event
):
    try:
        timezone = browser_conf.ip_info.get('timezone', 'UTC')
        stealth_script = build_stealth_script(browser_conf)
        proxy_config = build_proxy_config(proxy_type, proxy_info)

        # কানেকশন ড্রপ এড়াতে এবং WebRTC লিক কমাতে ক্রোম আর্গুমেন্ট যুক্ত করা হয়েছে
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-dev-shm-usage",
            "--ignore-certificate-errors",                 # SSL রিলেটেড কানেকশন ক্লোজড এড়াতে
            "--allow-running-insecure-content",
            "--force-webrtc-ip-handling-policy=disable_non_proxied_udp", # WebRTC লিক বন্ধ করতে
            "--webrtc-ip-handling-policy=disable_non_proxied_udp",
            "--no-pings",
            "--disable-background-networking",
            f"--window-size={browser_conf.window_width},{browser_conf.window_height}",
            f"--lang={browser_conf.browser_language}",
        ]

        fake_brands = ['Not/A)Brand', 'Not:A-Brand', 'Not_A Brand']
        chosen_fake_brand = random.choice(fake_brands)
        chrome_major = browser_conf.chrome_version.split(".")[0]

        launch_kwargs = {
            "headless": False,
            "args": launch_args,
            "user_data_dir": profile_path,   
            "channel": "chrome",
            "timezone_id": timezone,         
            "user_agent": browser_conf.user_agent,
            "locale": browser_conf.browser_language,
            "viewport": {"width": browser_conf.window_width, "height": browser_conf.window_height} 
        }

        if proxy_config:
            launch_kwargs["proxy"] = proxy_config

        def setup_page(page: Page):
            """
            নতুন ট্যাবের ভিউপোর্ট এবং মেকানিক্স CDP দিয়ে ওভাররাইড করা
            """
            try:
                cdp = context.new_cdp_session(page)
                cdp.send("Emulation.setTimezoneOverride", {"timezoneId": timezone})
                cdp.send("Network.setUserAgentOverride", {
                    "userAgent": browser_conf.user_agent,
                    "platform": "Win32",  
                    "acceptLanguage": browser_conf.browser_language,
                    "userAgentMetadata": {
                        "brands": [
                            {"brand": chosen_fake_brand, "version": f"{chrome_major}.0.0.0"},
                            {"brand": "Chromium", "version": f"{chrome_major}.0.0.0"},
                            {"brand": "Google Chrome", "version": f"{chrome_major}.0.0.0"}
                        ],
                        "fullVersionList": [
                            {"brand": chosen_fake_brand, "version": browser_conf.chrome_version},
                            {"brand": "Chromium", "version": browser_conf.chrome_version},
                            {"brand": "Google Chrome", "version": browser_conf.chrome_version}
                        ],
                        "platform": "Windows",
                        "platformVersion": "10.0.0",
                        "architecture": "x86",
                        "model": "",
                        "mobile": False,
                        "bitness": "64"
                    }
                })

                cdp.send("Emulation.setDeviceMetricsOverride", {
                    "width": browser_conf.window_width,
                    "height": browser_conf.window_height,
                    "deviceScaleFactor": 1,
                    "mobile": False,
                    "screenWidth": browser_conf.window_width,
                    "screenHeight": browser_conf.window_height,
                })
                print(f"✅ Page setup configured: {page.url or 'blank'}")
            except Exception as e:
                print(f"⚠️ Page CDP error: {e}")

        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(**launch_kwargs)

            # সব উইন্ডোতে স্ক্রিপ্ট ইনজেক্ট করা হচ্ছে
            context.add_init_script(stealth_script)

            # নতুন পেজ খোলা মাত্রই (কোনো প্রকার ডিলে ছাড়া) setup_page রান করা হবে
            def on_new_page(page: Page):
                print(f"🆕 New tab opened")
                setup_page(page)

            context.on("page", on_new_page)

            # প্রথম পেজ
            page = context.pages[0] if context.pages else context.new_page()
            setup_page(page)

            # কানেকশন ক্লোজড হয়ে থ্রেড ক্র্যাশ করা এড়াতে ট্রাই-ক্যাচ
            try:
                page.goto("https://pixelscan.net/fingerprint-check/", wait_until="domcontentloaded", timeout=45000)
            except Exception as nav_err:
                print(f"⚠️ Navigation status: {nav_err}. (We keeping the browser open for debugging)")

            print(f"✅ Browser running | Port: {debug_port} | TZ: {timezone} | Proxy: {proxy_config}")
            result.update({"status": "success", "message": "Browser opened", "debug_port": debug_port})
            ready_event.set()

            context.wait_for_event("close", timeout=0)

    except Exception as e:
        print(f"❌ Browser thread error: {e}")
        result.update({"status": "error", "message": str(e)})
        ready_event.set()


# ================================================================
# PUBLIC ASYNC FUNCTION
# ================================================================

async def open_browser_playwright(
    debug_port: int,
    profile_path: str,
    browser_conf,
    proxy_type: str = 'http',
    proxy_info: dict = None
):
    result = {}
    ready_event = threading.Event()

    threading.Thread(
        target=_browser_thread,
        args=(debug_port, profile_path, browser_conf, proxy_type, proxy_info, result, ready_event),
        daemon=True,
        name=f"browser-{debug_port}"
    ).start()

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: ready_event.wait(timeout=15))

    return result