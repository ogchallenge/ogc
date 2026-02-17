#!/usr/bin/env python3
import hashlib
import json
import posixpath
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "docs"
YEARS = ["2024", "2025", "2026"]
DEFAULT_ROOT_HASH_TARGETS = ["*.html", "*.css"]
DEFAULT_YEAR_HASH_TARGETS = ["*.html", "*.css", "markdown"]
TEXT_EXTENSIONS = {".html", ".css", ".js", ".json", ".md", ".txt"}


def replace_path_token(text: str, old: str, new: str) -> str:
    pattern = rf"(?<![A-Za-z0-9_./-]){re.escape(old)}(?![A-Za-z0-9_./-])"
    return re.sub(pattern, new, text)


def short_hash(data: bytes, length: int = 10) -> str:
    return hashlib.sha256(data).hexdigest()[:length]


def file_hash(path: Path, length: int = 10) -> str:
    return short_hash(path.read_bytes(), length)


def hashed_name(filename: str, digest: str) -> str:
    src = Path(filename)
    return f"{src.stem}.{digest}{src.suffix}"


def create_default_hashing_config() -> None:
    content = (
        "# Files or folders to hash for this scope\n"
        "# - Wildcard example: *.html, *.css, assets/**/*.png\n"
        "# - Folder example: markdown\n"
        "# - File example: index.html\n"
        "\n"
        "*.html\n"
        "*.css\n"
        "markdown\n"
    )

    root_config = ROOT / "file_hashing.txt"
    if not root_config.exists():
        root_config.write_text(content, encoding="utf-8")

    for year in YEARS:
        config_path = ROOT / year / "file_hashing.txt"
        if not config_path.exists():
            config_path.write_text(content, encoding="utf-8")


def read_hash_targets(config_path: Path, default_targets: list[str]) -> list[str]:
    if not config_path.exists():
        return list(default_targets)

    targets: list[str] = []
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        targets.append(stripped)

    return targets or list(default_targets)


def is_markdown_target(target: str) -> bool:
    normalized = target.replace("\\", "/")
    return normalized == "markdown" or normalized.startswith("markdown/")


def resolve_target_files(year_dir: Path, targets: list[str]) -> set[Path]:
    files: set[Path] = set()

    for target in targets:
        normalized = target.replace("\\", "/")
        if is_markdown_target(normalized):
            continue

        has_glob = any(ch in normalized for ch in "*?[")
        if has_glob:
            matched = year_dir.glob(normalized)
        else:
            candidate = year_dir / normalized
            matched = [candidate] if candidate.exists() else []

        for path in matched:
            if path.is_file():
                files.add(path)
            elif path.is_dir():
                for nested in path.rglob("*"):
                    if nested.is_file():
                        files.add(nested)

    return files


def copy_source_to_dist() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)

    def _ignore(_dir: str, names: list[str]) -> set[str]:
        ignored = set()
        for name in names:
            if name in {"dist", "docs", ".git", ".vscode", "__pycache__"}:
                ignored.add(name)
        return ignored

    shutil.copytree(ROOT, DIST, ignore=_ignore)


def hash_markdown_files(year_dir: Path) -> tuple[dict[str, str], dict[str, str]]:
    markdown_dir = year_dir / "markdown"
    en_dir = markdown_dir / "en"
    ko_dir = markdown_dir / "ko"

    if not markdown_dir.exists():
        return {}, {}

    filenames = set()
    for lang_dir in (en_dir, ko_dir):
        if lang_dir.exists():
            for path in lang_dir.glob("*.md"):
                filenames.add(path.name)

    name_map: dict[str, str] = {}
    path_map: dict[str, str] = {}
    for filename in sorted(filenames):
        digest_source = b""
        for lang in ("en", "ko"):
            path = markdown_dir / lang / filename
            if path.exists():
                digest_source += path.read_bytes()
        digest = short_hash(digest_source)
        name_map[filename] = hashed_name(filename, digest)

    for lang in ("en", "ko"):
        lang_dir = markdown_dir / lang
        if not lang_dir.exists():
            continue
        for original, hashed in name_map.items():
            src = lang_dir / original
            dst = lang_dir / hashed
            if src.exists():
                src.rename(dst)
                src_rel = src.relative_to(year_dir).as_posix()
                dst_rel = dst.relative_to(year_dir).as_posix()
                path_map[src_rel] = dst_rel

    return name_map, path_map


def hash_sidebar_json(year_dir: Path, markdown_name_map: dict[str, str]) -> tuple[str | None, dict[str, str]]:
    sidebar_path = year_dir / "markdown" / "sidebar.json"
    if not sidebar_path.exists():
        return None, {}

    config = json.loads(sidebar_path.read_text(encoding="utf-8"))
    for page in config.get("pages", []):
        file_name = page.get("file")
        if file_name in markdown_name_map:
            page["file"] = markdown_name_map[file_name]

    content = json.dumps(config, ensure_ascii=False, indent=2) + "\n"
    digest = short_hash(content.encode("utf-8"))
    hashed_filename = f"sidebar.{digest}.json"
    hashed_path = sidebar_path.with_name(hashed_filename)
    hashed_path.write_text(content, encoding="utf-8")
    sidebar_path.unlink()

    old_rel = sidebar_path.relative_to(year_dir).as_posix()
    new_rel = hashed_path.relative_to(year_dir).as_posix()
    return hashed_filename, {old_rel: new_rel}


def rewrite_markdown_references(year_dir: Path, sidebar_hashed: str | None, markdown_name_map: dict[str, str]) -> None:
    for html_path in year_dir.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        original = text

        if sidebar_hashed:
            text = text.replace("fetch('markdown/sidebar.json')", f"fetch('markdown/{sidebar_hashed}')")
            text = text.replace('fetch("markdown/sidebar.json")', f'fetch("markdown/{sidebar_hashed}")')

        for original_name, hashed_name_value in markdown_name_map.items():
            text = text.replace(f"'{original_name}'", f"'{hashed_name_value}'")
            text = text.replace(f'"{original_name}"', f'"{hashed_name_value}"')

        if text != original:
            html_path.write_text(text, encoding="utf-8")


def hash_selected_files(scope_dir: Path, targets: list[str], skip_markdown_paths: bool) -> tuple[dict[str, str], str | None]:
    mapping: dict[str, str] = {}
    hashed_index_filename: str | None = None

    for path in sorted(resolve_target_files(scope_dir, targets)):
        rel = path.relative_to(scope_dir).as_posix()
        if rel == "file_hashing.txt":
            continue
        if skip_markdown_paths and rel.startswith("markdown/"):
            continue

        digest = file_hash(path)
        new_name = hashed_name(path.name, digest)
        new_path = path.with_name(new_name)
        path.rename(new_path)

        new_rel = new_path.relative_to(scope_dir).as_posix()
        mapping[rel] = new_rel

        if rel == "index.html":
            hashed_index_filename = new_name

    return mapping, hashed_index_filename


def rewrite_paths_in_text_files(scope_dir: Path, path_map: dict[str, str], recursive: bool) -> None:
    if not path_map:
        return

    ordered = sorted(path_map.items(), key=lambda item: len(item[0]), reverse=True)

    file_iter = scope_dir.rglob("*") if recursive else scope_dir.glob("*")

    for path in file_iter:
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if path.name == "file_hashing.txt":
            continue

        text = path.read_text(encoding="utf-8")
        original = text
        current_rel = path.relative_to(scope_dir).as_posix()
        current_dir = posixpath.dirname(current_rel)

        for old_rel, new_rel in ordered:
            candidate_pairs: dict[str, str] = {}

            old_norm = posixpath.normpath(old_rel)
            new_norm = posixpath.normpath(new_rel)
            candidate_pairs[old_rel] = new_rel
            candidate_pairs[old_norm] = new_norm

            old_from_current = posixpath.normpath(posixpath.relpath(old_norm, current_dir or "."))
            new_from_current = posixpath.normpath(posixpath.relpath(new_norm, current_dir or "."))
            candidate_pairs[old_from_current] = new_from_current

            if old_from_current not in {".", ".."} and not old_from_current.startswith("./") and not old_from_current.startswith("../"):
                candidate_pairs[f"./{old_from_current}"] = f"./{new_from_current}"

            for old_candidate, new_candidate in candidate_pairs.items():
                text = replace_path_token(text, old_candidate, new_candidate)

        if text != original:
            path.write_text(text, encoding="utf-8")


def build_parent_alias_map(path_map: dict[str, str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for old_rel, new_rel in path_map.items():
        if "/" in old_rel or "/" in new_rel:
            continue
        aliases[f"../{old_rel}"] = f"../{new_rel}"
    return aliases


def create_index_loader(scope_dir: Path, hashed_index_filename: str) -> None:
    loader = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\" />\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
        "  <script>\n"
        f"    window.location.replace('{hashed_index_filename}' + window.location.search + window.location.hash);\n"
        "  </script>\n"
        "</head>\n"
        "<body></body>\n"
        "</html>\n"
    )
    (scope_dir / "index.html").write_text(loader, encoding="utf-8")


def process_root() -> dict[str, str]:
    targets = read_hash_targets(ROOT / "file_hashing.txt", DEFAULT_ROOT_HASH_TARGETS)
    selected_map, hashed_index_filename = hash_selected_files(DIST, targets, skip_markdown_paths=False)
    rewrite_paths_in_text_files(DIST, selected_map, recursive=False)
    if hashed_index_filename:
        create_index_loader(DIST, hashed_index_filename)
    return selected_map


def process_year(year: str, root_map: dict[str, str]) -> None:
    year_dir = DIST / year
    if not year_dir.exists():
        return

    targets = read_hash_targets(ROOT / year / "file_hashing.txt", DEFAULT_YEAR_HASH_TARGETS)
    contains_markdown = any(is_markdown_target(target) for target in targets)

    global_map: dict[str, str] = {}
    markdown_name_map: dict[str, str] = {}
    sidebar_hashed: str | None = None

    if contains_markdown:
        markdown_name_map, markdown_path_map = hash_markdown_files(year_dir)
        sidebar_hashed, sidebar_map = hash_sidebar_json(year_dir, markdown_name_map)
        global_map.update(markdown_path_map)
        global_map.update(sidebar_map)

    selected_map, hashed_index_filename = hash_selected_files(
        year_dir,
        targets,
        skip_markdown_paths=contains_markdown,
    )
    global_map.update(selected_map)

    root_hashed_style = root_map.get("styles.css")
    if root_hashed_style:
        global_map["../styles.css"] = f"../{root_hashed_style}"

    if contains_markdown:
        rewrite_markdown_references(year_dir, sidebar_hashed, markdown_name_map)

    rewrite_paths_in_text_files(year_dir, global_map, recursive=True)

    if hashed_index_filename:
        create_index_loader(year_dir, hashed_index_filename)


def build_dist() -> None:
    create_default_hashing_config()
    copy_source_to_dist()
    root_map = process_root()
    for year in YEARS:
        process_year(year, root_map)


def main() -> None:
    build_dist()
    print(f"Built hashed dist at: {DIST}")


if __name__ == "__main__":
    main()
