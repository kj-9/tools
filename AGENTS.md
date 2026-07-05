# Repository Guidelines

## Project Structure & Module Organization

This repository is a no-build GitHub Pages collection of small tools. Top-level `*.html` files are standalone browser utilities and are published directly. `index.html` is the tool directory and should be updated whenever a public tool is added, renamed, or removed. `README.md` mirrors the published catalog and script usage. Python command-line utilities live in `python/` and use PEP 723 inline metadata so they can run through `uv` from either a local path or the published URL. The empty `src/` tree is not part of the current published surface.

## Build, Test, and Development Commands

- `npx --yes http-server . -p 4173 -c-1`: serve the static site locally with caching disabled.
- `uv run python/egress-ip.py`: run the egress IP diagnostic script locally.
- `uv run python/gitnation-subs.py --help`: inspect the GitNation subtitle downloader CLI.
- `uv run https://kj-9.github.io/tools/python/egress-ip.py`: verify published Python script execution.

There is no build step or package install required for the HTML tools.

## Coding Style & Naming Conventions

Use plain HTML, CSS, and vanilla JavaScript unless a tool clearly needs a dependency. Keep each browser tool self-contained in a kebab-case file such as `xml-formatter.html`. Match the existing two-space indentation in HTML/CSS/JS. Python scripts target Python `>=3.9`, prefer standard-library dependencies, use snake_case for functions, and keep CLI behavior in `main()`.

## Testing Guidelines

No formal test framework is configured. For HTML tools, manually open the page through a local static server and test the main workflow, empty/error states, and mobile-width layout. For Python scripts, run the relevant `uv run ... --help` or a safe dry-run command before changing README or homepage examples. When editing `index.html`, confirm every listed local link resolves.

## Commit & Pull Request Guidelines

Recent history uses short, imperative commit messages, for example `Improve tools index` and `Update README and add index.html for tool descriptions and layout`. Keep commits focused on one tool or documentation change. Pull requests should include a concise summary, affected pages/scripts, manual verification commands, and screenshots for visible UI changes.

## Security & Configuration Tips

Do not commit credentials, API keys, downloaded subtitle files, or environment-specific output. Python scripts intended for published `uv run` usage should avoid private package dependencies and local-only assumptions.
