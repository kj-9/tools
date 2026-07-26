# [tools](https://kj-9.github.io/tools/)

A small collection of browser-based utilities.

The tool list is maintained on the published site.

- [Published site](https://kj-9.github.io/tools/)
- [Source repository](https://github.com/kj-9/tools)

## Tools

- [XML Formatter](https://kj-9.github.io/tools/xml-formatter.html): Formats XML with indentation and newline options.
- [Character-Byte Counter](https://kj-9.github.io/tools/character-byte-counter.html): Shows UTF-8 byte counts and code points for each character.
- [RSS Reader](https://kj-9.github.io/tools/rss-reader.html): Loads an RSS feed and displays articles in a browser UI.
- [セルフ・コンパッション尺度（日本語版）](https://kj-9.github.io/tools/japanese-scs.html): A Japanese self-compassion scale questionnaire.
- [方丈記 読み比べ](https://kj-9.github.io/tools/hojoki-reader.html): Reads Hojoki with the original text and Haruo Sato's modern Japanese translation.

## Scripts

- `python/egress-ip.py`: Checks DNS and HTTPS connectivity, then prints the egress IP address.
- `python/gitnation-subs.py`: Extracts a Vimeo embed from a GitNation page and downloads available subtitles with `yt-dlp`.

Run them from the published URL:

```sh
uv run https://kj-9.github.io/tools/python/egress-ip.py
uv run https://kj-9.github.io/tools/python/gitnation-subs.py --help
```

## Maintenance

This repository is intentionally simple: most tools are standalone HTML files with no build step. When adding a tool, update `index.html` and this README so the published site stays browsable.
