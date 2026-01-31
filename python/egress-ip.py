# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
import datetime
import socket
import subprocess
import sys
import time
import urllib.request
from typing import Optional

CHECK_HOSTS = [
    "ifconfig.me",
    "api.ipify.org",
    "icanhazip.com",
]

CHECK_URLS = [
    "https://ifconfig.me",
    "https://api.ipify.org",
    "https://icanhazip.com",
]

RETRIES = 3
TIMEOUT = 5


def _is_tty() -> bool:
    return sys.stderr.isatty()


def _color(code: str) -> str:
    return f"\x1b[{code}m" if _is_tty() else ""


def _level_style(level: str) -> tuple[str, str]:
    match level:
        case "OK":
            return (">", _color("32"))
        case "WARN":
            return ("!", _color("33"))
        case "ERR":
            return ("x", _color("31"))
        case "INFO":
            return ("i", _color("36"))
        case "FATAL":
            return ("!!", _color("31;1"))
        case "SUCCESS":
            return ("*", _color("32;1"))
        case _:
            return ("-", _color("0"))


def log(level: str, msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    icon, color = _level_style(level)
    reset = _color("0")
    print(f"{color}{ts} {icon} {level:<7}{reset} {msg}", file=sys.stderr, flush=True)


def check_dns(host: str) -> bool:
    try:
        socket.getaddrinfo(host, None)
        log("OK", f"DNS {host}")
        return True
    except Exception as e:
        log("ERR", f"DNS {host}: {e}")
        return False


def check_https(url: str) -> Optional[str]:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            body = r.read().decode().strip()
            return body
    except Exception as e:
        log("WARN", f"HTTPS {url}: {e}")
        return None


def dump_resolv_conf():
    try:
        log("INFO", "/etc/resolv.conf")
        with open("/etc/resolv.conf") as f:
            print(f.read().strip(), file=sys.stderr)
        log("INFO", "end /etc/resolv.conf")
    except Exception as e:
        log("WARN", f"cannot read /etc/resolv.conf: {e}")


def dump_ip_route():
    try:
        log("INFO", "ip route")
        subprocess.run(["ip", "route"], check=False)
        log("INFO", "end ip route")
    except FileNotFoundError:
        log("INFO", "ip command not available (macOS / minimal env)")


def main():
    log("INFO", "network diagnose start")

    # DNS check
    dns_ok = False
    for h in CHECK_HOSTS:
        if check_dns(h):
            dns_ok = True

    if not dns_ok:
        log("FATAL", "DNS resolution failed for all hosts")
        dump_resolv_conf()
        dump_ip_route()
        sys.exit(10)

    # HTTPS + IP check (retry)
    for attempt in range(1, RETRIES + 1):
        log("INFO", f"HTTPS attempt {attempt}/{RETRIES}")
        for url in CHECK_URLS:
            ip = check_https(url)
            if ip:
                log("SUCCESS", f"egress_ip={ip} via {url}")
                print(ip, flush=True)
                sys.exit(0)
        time.sleep(2)

    log("FATAL", "HTTPS reachable but IP check failed repeatedly")
    dump_resolv_conf()
    dump_ip_route()
    sys.exit(20)


if __name__ == "__main__":
    main()
