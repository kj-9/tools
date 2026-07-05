# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

VIMEO_EMBED_RE = re.compile(
    r"(?:https?:)?(?:\\?/\\?/|//)?player(?:\\?\.|\.)vimeo(?:\\?\.|\.)com(?:\\?/|/)video(?:\\?/|/)([0-9]+)"
)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 gitnation-subs/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except urllib.error.URLError as error:
        raise SystemExit(f"Failed to fetch GitNation page: {error}") from error


def find_vimeo_url(page_html: str) -> str:
    match = VIMEO_EMBED_RE.search(page_html)
    if not match:
        raise SystemExit("Could not find a Vimeo embed on this GitNation page.")
    return f"https://player.vimeo.com/video/{match.group(1)}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download subtitles from a GitNation page backed by a Vimeo embed."
    )
    parser.add_argument("gitnation_url", help="GitNation content page URL")
    parser.add_argument(
        "-l",
        "--lang",
        default="en",
        help="Subtitle language to download. Examples: en, es, en-x-autogen, all. Default: en",
    )
    parser.add_argument(
        "-P",
        "--path",
        default=".",
        help="Output directory for subtitle files. Default: current directory",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Only list available subtitles; do not download",
    )
    parser.add_argument(
        "--print-vimeo-url",
        action="store_true",
        help="Print the extracted Vimeo embed URL and exit",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    page_html = fetch_text(args.gitnation_url)
    vimeo_url = find_vimeo_url(page_html)

    if args.print_vimeo_url:
        print(vimeo_url)
        return 0

    print(f"GitNation URL: {args.gitnation_url}", file=sys.stderr)
    print(f"Vimeo URL:     {vimeo_url}", file=sys.stderr)

    if args.list:
        command = [
            "uvx",
            "yt-dlp",
            "--referer",
            args.gitnation_url,
            "--list-subs",
            vimeo_url,
        ]
    else:
        Path(args.path).mkdir(parents=True, exist_ok=True)
        command = [
            "uvx",
            "yt-dlp",
            "-P",
            args.path,
            "--referer",
            args.gitnation_url,
            "--sub-langs",
            args.lang,
            "--write-subs",
            "--write-auto-subs",
            "--skip-download",
            vimeo_url,
        ]

    try:
        return subprocess.run(command, check=False).returncode
    except FileNotFoundError:
        raise SystemExit("uvx is required. Install uv first: https://docs.astral.sh/uv/")


if __name__ == "__main__":
    raise SystemExit(main())
