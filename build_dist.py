#!/usr/bin/env python3
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "docs"
YEARS = ["2024", "2025", "2026"]
DEFAULT_ROOT_HASH_TARGETS = ["*.html", "*.css"]
DEFAULT_YEAR_HASH_TARGETS = ["*.html", "*.css", "markdown"]
TEXT_EXTENSIONS = {".html", ".css", ".js", ".json", ".md", ".txt"}
RELEASE_STATE_FILENAME = "release_versions.json"
RELEASE_MANIFEST_FILENAME = "release_manifest.json"
RELEASE_CONFIG_FILENAME = "release.txt"
GITIGNORE_MANAGED_START = "# >>> OGC release-managed ignore (auto) >>>"
GITIGNORE_MANAGED_END = "# <<< OGC release-managed ignore (auto) <<<"
INITIAL_RELEASE_VERSION = "1.0.0"


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
    print("[config] Ensuring default file_hashing.txt files")
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
        print(f"[config] Created {root_config.relative_to(ROOT).as_posix()}")

    for year in YEARS:
        config_path = ROOT / year / "file_hashing.txt"
        if not config_path.exists():
            config_path.write_text(content, encoding="utf-8")
            print(f"[config] Created {config_path.relative_to(ROOT).as_posix()}")


def create_default_release_config() -> None:
    print("[release] Ensuring default release.txt files")
    for year in YEARS:
        config_path = ROOT / year / RELEASE_CONFIG_FILENAME
        if config_path.exists():
            continue
        config_path.write_text(
            "# GitHub Release에 업로드할 파일/폴더 목록\n"
            "# - 파일 예: instances/train/stage3_problems.zip\n"
            "# - 폴더 예: baselines\n"
            "# - 와일드카드 예: instances/test/*.zip\n"
            "# 주석/빈 줄은 무시됩니다.\n",
            encoding="utf-8",
        )
        print(f"[release] Created {config_path.relative_to(ROOT).as_posix()}")


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


def read_release_targets(config_path: Path) -> list[str]:
    if not config_path.exists():
        return []

    targets: list[str] = []
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        targets.append(stripped)
    return targets


def normalize_release_target_for_ignore(year: str, target: str) -> str:
    normalized = target.strip().replace("\\", "/").lstrip("/")
    return f"{year}/{normalized}"


def build_release_ignore_patterns() -> list[str]:
    patterns: list[str] = []
    for year in YEARS:
        config_path = ROOT / year / RELEASE_CONFIG_FILENAME
        for target in read_release_targets(config_path):
            patterns.append(normalize_release_target_for_ignore(year, target))
    return sorted(set(patterns))


def sync_release_gitignore() -> None:
    gitignore_path = ROOT / ".gitignore"
    existing = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""

    block_lines = [
        GITIGNORE_MANAGED_START,
        "# Generated from <year>/release.txt. Do not edit this block manually.",
        *build_release_ignore_patterns(),
        GITIGNORE_MANAGED_END,
    ]
    block = "\n".join(block_lines)

    pattern = re.compile(
        rf"\n?{re.escape(GITIGNORE_MANAGED_START)}[\s\S]*?{re.escape(GITIGNORE_MANAGED_END)}\n?",
        flags=re.MULTILINE,
    )
    base = re.sub(pattern, "\n", existing).rstrip()
    if base:
        new_content = f"{base}\n\n{block}\n"
    else:
        new_content = f"{block}\n"

    gitignore_path.write_text(new_content, encoding="utf-8")
    print(f"[release] Synced managed block in {gitignore_path.relative_to(ROOT).as_posix()}")


def remove_release_files_from_git_tracking() -> None:
    if shutil.which("git") is None:
        print("[release] git not found. Skipping index cleanup.")
        return

    all_files: set[Path] = set()
    for year in YEARS:
        year_dir = ROOT / year
        targets = read_release_targets(year_dir / RELEASE_CONFIG_FILENAME)
        all_files.update(resolve_release_files(year_dir, targets))

    if not all_files:
        print("[release] No release targets found to untrack.")
        return

    rel_paths = [path.relative_to(ROOT).as_posix() for path in sorted(all_files)]
    subprocess.run(
        ["git", "rm", "--cached", "--ignore-unmatch", "--", *rel_paths],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    print(f"[release] Requested untracking for {len(rel_paths)} release-target files")


def resolve_release_files(scope_dir: Path, targets: list[str]) -> set[Path]:
    files: set[Path] = set()
    for target in targets:
        normalized = target.replace("\\", "/")
        has_glob = any(ch in normalized for ch in "*?[")
        if has_glob:
            matched = scope_dir.glob(normalized)
        else:
            candidate = scope_dir / normalized
            matched = [candidate] if candidate.exists() else []

        for path in matched:
            if path.is_file():
                files.add(path)
            elif path.is_dir():
                for nested in path.rglob("*"):
                    if nested.is_file():
                        files.add(nested)
    return files


def build_release_copy_exclusions() -> tuple[set[str], set[str]]:
    excluded_dirs: set[str] = set()
    excluded_files: set[str] = set()

    for year in YEARS:
        year_dir = ROOT / year
        targets = read_release_targets(year_dir / RELEASE_CONFIG_FILENAME)

        for target in targets:
            normalized = target.replace("\\", "/").lstrip("/")
            has_glob = any(ch in normalized for ch in "*?[")
            if has_glob:
                prefix_parts: list[str] = []
                for part in normalized.split("/"):
                    if any(ch in part for ch in "*?["):
                        break
                    prefix_parts.append(part)
                if prefix_parts:
                    excluded_dirs.add(f"{year}/{'/'.join(prefix_parts)}")
                continue

            candidate = year_dir / normalized
            if candidate.is_dir():
                excluded_dirs.add(candidate.relative_to(ROOT).as_posix())

        matched_files = resolve_release_files(year_dir, targets)
        for path in matched_files:
            excluded_files.add(path.relative_to(ROOT).as_posix())

    return excluded_dirs, excluded_files


def parse_semver(version_text: str) -> tuple[int, int, int]:
    try:
        major, minor, patch = (int(part) for part in version_text.split("."))
        return major, minor, patch
    except Exception:
        return 0, 0, 0


def bump_patch(version_text: str) -> str:
    major, minor, patch = parse_semver(version_text)
    return f"{major}.{minor}.{patch + 1}"


def resolve_release_version(previous: dict[str, str], digest: str) -> tuple[str, str]:
    previous_version = str(previous.get("version", "")).strip()
    previous_digest = previous.get("sha256")

    if not previous_version:
        return INITIAL_RELEASE_VERSION, "initial"
    if previous_digest == digest:
        return previous_version, "unchanged"
    return bump_patch(previous_version), "changed"


def sanitize_release_asset_stem(stem: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", stem)
    return sanitized.strip("._") or "asset"


def build_release_asset_name(year: str, relative_path: str, version: str) -> str:
    src = Path(relative_path)
    stem = sanitize_release_asset_stem(f"{year}__{str(src.with_suffix('')).replace('/', '__')}")
    return f"{stem}_v{version}{src.suffix}"


def get_github_repo_slug() -> str | None:
    from_env = os.getenv("OGC_GITHUB_REPOSITORY") or os.getenv("GITHUB_REPOSITORY")
    if from_env and "/" in from_env:
        return from_env.strip()

    try:
        remote = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=ROOT,
            text=True,
        ).strip()
    except Exception:
        return None

    https_match = re.match(r"https://github\.com/([^/]+/[^/.]+)(?:\.git)?$", remote)
    if https_match:
        return https_match.group(1)

    ssh_match = re.match(r"git@github\.com:([^/]+/[^/.]+)(?:\.git)?$", remote)
    if ssh_match:
        return ssh_match.group(1)

    return None


def build_release_url(repo_slug: str, tag: str, asset_name: str) -> str:
    return f"https://github.com/{repo_slug}/releases/download/{quote(tag)}/{quote(asset_name)}"


def write_release_upload_script(year: str, repo_slug: str, tag: str, asset_names: list[str], assets_dir: Path) -> None:
    if not asset_names:
        return

    quoted_assets = " ".join(f'"{name}"' for name in sorted(asset_names))
    script = (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        f"REPO=\"${{1:-{repo_slug}}}\"\n"
        f"TAG=\"{tag}\"\n"
        f"TITLE=\"OGC {year} assets\"\n\n"
        "if ! gh release view \"$TAG\" -R \"$REPO\" >/dev/null 2>&1; then\n"
        "  gh release create \"$TAG\" -R \"$REPO\" -t \"$TITLE\" -n \"Automated asset upload\"\n"
        "fi\n\n"
        f"gh release upload \"$TAG\" -R \"$REPO\" --clobber {quoted_assets}\n"
    )
    script_path = assets_dir / "upload_release_assets.sh"
    script_path.write_text(script, encoding="utf-8")
    script_path.chmod(0o755)
    print(
        f"[release:{year}] Wrote upload helper: "
        f"{script_path.relative_to(ROOT).as_posix()} ({len(asset_names)} assets)"
    )


def try_publish_release_assets(year: str, repo_slug: str, tag: str, asset_names: list[str], assets_dir: Path) -> None:
    if not asset_names:
        return
    if shutil.which("gh") is None:
        print(f"[release:{year}] gh CLI not found. Skipping automatic publish.")
        return

    auth = subprocess.run(
        ["gh", "auth", "status", "-h", "github.com"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if auth.returncode != 0:
        print(f"[release:{year}] gh auth not configured. Skipping automatic publish.")
        return

    view = subprocess.run(
        ["gh", "release", "view", tag, "-R", repo_slug],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if view.returncode != 0:
        create = subprocess.run(
            [
                "gh",
                "release",
                "create",
                tag,
                "-R",
                repo_slug,
                "-t",
                f"OGC {year} assets",
                "-n",
                "Automated asset upload",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if create.returncode != 0:
            print(f"[release:{year}] Failed to create release tag {tag}: {create.stderr.strip()}")
            return

    asset_paths = [str(assets_dir / name) for name in sorted(asset_names)]
    upload = subprocess.run(
        ["gh", "release", "upload", tag, "-R", repo_slug, "--clobber", *asset_paths],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if upload.returncode != 0:
        print(f"[release:{year}] Failed to upload assets: {upload.stderr.strip()}")
        return

    print(f"[release:{year}] Uploaded {len(asset_names)} assets to {repo_slug}:{tag}")


def sync_release_assets(year: str, year_source_dir: Path, repo_slug: str | None) -> dict[str, str]:
    config_path = year_source_dir / RELEASE_CONFIG_FILENAME
    targets = read_release_targets(config_path)
    print(f"[release:{year}] Loaded {len(targets)} release targets from {config_path.relative_to(ROOT).as_posix()}")
    release_files = sorted(resolve_release_files(year_source_dir, targets))
    if not release_files:
        print(f"[release:{year}] No release files matched. Skipping release packaging.")
        return {}
    print(f"[release:{year}] Matched {len(release_files)} files for release packaging")

    state_path = year_source_dir / RELEASE_STATE_FILENAME
    previous_state = {
        "files": {}
    }
    if state_path.exists():
        try:
            previous_state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous_state = {"files": {}}

    previous_files: dict[str, dict[str, str]] = previous_state.get("files", {})

    tag = f"ogc-{year}-assets"
    assets_dir = ROOT / "release_assets" / year
    if assets_dir.exists():
        shutil.rmtree(assets_dir)
    assets_dir.mkdir(parents=True, exist_ok=True)
    print(f"[release:{year}] Prepared assets directory: {assets_dir.relative_to(ROOT).as_posix()}")

    next_files: dict[str, dict[str, str]] = {}
    markdown_url_map: dict[str, str] = {}
    changed_asset_names: list[str] = []

    for source_file in release_files:
        rel = source_file.relative_to(year_source_dir).as_posix()
        digest = hashlib.sha256(source_file.read_bytes()).hexdigest()
        previous = previous_files.get(rel, {})
        version, version_reason = resolve_release_version(previous, digest)

        asset_name = build_release_asset_name(year, rel, version)
        if version_reason != "unchanged":
            changed_asset_names.append(asset_name)
            shutil.copy2(source_file, assets_dir / asset_name)
            print(
                f"[release:{year}] {rel} -> {asset_name} | "
                f"version={version} ({version_reason}, upload=yes)"
            )
        else:
            print(
                f"[release:{year}] {rel} -> {asset_name} | "
                f"version={version} ({version_reason}, upload=no)"
            )

        url = build_release_url(repo_slug, tag, asset_name) if repo_slug else ""

        next_files[rel] = {
            "version": version,
            "sha256": digest,
            "asset": asset_name,
            "tag": tag,
            "url": url,
        }

        if url:
            markdown_url_map[rel] = url

    state_payload = {
        "schema": 1,
        "year": year,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "files": next_files,
    }
    state_path.write_text(json.dumps(state_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[release:{year}] Wrote state: {state_path.relative_to(ROOT).as_posix()}")

    manifest_path = year_source_dir / RELEASE_MANIFEST_FILENAME
    manifest_payload = {
        "schema": 1,
        "repo": repo_slug,
        "year": year,
        "tag": tag,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assets_dir": assets_dir.relative_to(ROOT).as_posix(),
        "changed_assets": changed_asset_names,
        "assets": list(next_files.values()),
    }
    manifest_path.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[release:{year}] Wrote manifest: {manifest_path.relative_to(ROOT).as_posix()}")

    if repo_slug:
        print(f"[release:{year}] Publishing enabled for repo: {repo_slug}")
        if changed_asset_names:
            write_release_upload_script(year, repo_slug, tag, changed_asset_names, assets_dir)
            try_publish_release_assets(year, repo_slug, tag, changed_asset_names, assets_dir)
        else:
            print(f"[release:{year}] No changed assets. Skipping upload.")
    else:
        print(f"[release:{year}] Repo slug not found. Skipping upload and URL mapping.")

    return markdown_url_map


def rewrite_release_links_in_markdown(text: str, markdown_rel_dir: str, release_url_map: dict[str, str]) -> str:
    if not release_url_map:
        return text

    updated = text
    replacements: dict[str, str] = {}

    for source_rel, release_url in release_url_map.items():
        source_norm = posixpath.normpath(source_rel)
        local_rel = posixpath.normpath(posixpath.relpath(source_norm, markdown_rel_dir or "."))

        candidates = {source_norm, local_rel}
        if not local_rel.startswith("../") and local_rel not in {".", ".."}:
            candidates.add(f"./{local_rel}")
        if not source_norm.startswith("../"):
            candidates.add(f"./{source_norm}")

        encoded_candidates = {quote(candidate, safe="/._-+") for candidate in candidates}
        candidates.update(encoded_candidates)
        candidates.update(unquote(candidate) for candidate in candidates)

        for candidate in candidates:
            if candidate:
                replacements[candidate] = release_url

    for old_path, new_url in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        updated = replace_path_token(updated, old_path, new_url)

    return updated


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
        print(f"[dist] Removed existing dist: {DIST.relative_to(ROOT).as_posix()}")

    excluded_dirs, excluded_files = build_release_copy_exclusions()
    print(
        f"[dist] Release-copy exclusions prepared | "
        f"dirs={len(excluded_dirs)} files={len(excluded_files)}"
    )

    def _ignore(_dir: str, names: list[str]) -> set[str]:
        current_dir = Path(_dir)
        current_rel = current_dir.relative_to(ROOT).as_posix() if current_dir != ROOT else ""
        ignored = set()
        for name in names:
            candidate_rel = f"{current_rel}/{name}" if current_rel else name
            if name in {
                "dist",
                "docs",
                ".git",
                ".vscode",
                "__pycache__",
                "release_assets",
                RELEASE_STATE_FILENAME,
                RELEASE_MANIFEST_FILENAME,
                RELEASE_CONFIG_FILENAME,
            }:
                ignored.add(name)
                continue

            if candidate_rel in excluded_dirs or candidate_rel in excluded_files:
                ignored.add(name)
        return ignored

    shutil.copytree(ROOT, DIST, ignore=_ignore)
    print(f"[dist] Copied source tree to dist: {DIST.relative_to(ROOT).as_posix()}")


def hash_markdown_files(year_dir: Path, release_url_map: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    markdown_dir = year_dir / "markdown"
    en_dir = markdown_dir / "en"
    ko_dir = markdown_dir / "ko"

    if not markdown_dir.exists():
        print(f"[hash:{year_dir.name}] markdown directory not found. Skipping markdown hashing.")
        return {}, {}

    filenames = set()
    for lang_dir in (en_dir, ko_dir):
        if lang_dir.exists():
            for path in lang_dir.glob("*.md"):
                filenames.add(path.name)

    transformed_content: dict[tuple[str, str], str] = {}

    for lang in ("en", "ko"):
        lang_dir = markdown_dir / lang
        if not lang_dir.exists():
            continue
        for filename in sorted(filenames):
            src = lang_dir / filename
            if not src.exists():
                continue
            text = src.read_text(encoding="utf-8")
            markdown_rel_dir = src.parent.relative_to(year_dir).as_posix()
            transformed = rewrite_release_links_in_markdown(text, markdown_rel_dir, release_url_map)
            transformed_content[(lang, filename)] = transformed
    print(f"[hash:{year_dir.name}] Prepared transformed markdown content for {len(filenames)} files")

    name_map: dict[str, str] = {}
    path_map: dict[str, str] = {}
    for filename in sorted(filenames):
        digest_source = b""
        for lang in ("en", "ko"):
            path = markdown_dir / lang / filename
            if path.exists():
                transformed = transformed_content.get((lang, filename), path.read_text(encoding="utf-8"))
                digest_source += transformed.encode("utf-8")
        digest = short_hash(digest_source)
        name_map[filename] = hashed_name(filename, digest)
    print(f"[hash:{year_dir.name}] Generated markdown hash names for {len(name_map)} files")

    for lang in ("en", "ko"):
        lang_dir = markdown_dir / lang
        if not lang_dir.exists():
            continue
        for original, hashed in name_map.items():
            src = lang_dir / original
            dst = lang_dir / hashed
            if src.exists():
                src.rename(dst)
                rewritten = transformed_content.get((lang, original), dst.read_text(encoding="utf-8"))
                dst.write_text(rewritten, encoding="utf-8")
                src_rel = src.relative_to(year_dir).as_posix()
                dst_rel = dst.relative_to(year_dir).as_posix()
                path_map[src_rel] = dst_rel

    print(f"[hash:{year_dir.name}] Renamed markdown files: {len(path_map)}")

    return name_map, path_map


def hash_contents_json(year_dir: Path, markdown_name_map: dict[str, str]) -> tuple[str | None, dict[str, str]]:
    contents_path = year_dir / "markdown" / "contents.json"
    if not contents_path.exists():
        print(f"[hash:{year_dir.name}] contents.json not found. Skipping sidebar hashing.")
        return None, {}

    config = json.loads(contents_path.read_text(encoding="utf-8"))
    for page in config.get("pages", []):
        file_name = page.get("file")
        if file_name in markdown_name_map:
            page["file"] = markdown_name_map[file_name]

    content = json.dumps(config, ensure_ascii=False, indent=2) + "\n"
    digest = short_hash(content.encode("utf-8"))
    hashed_filename = f"contents.{digest}.json"
    hashed_path = contents_path.with_name(hashed_filename)
    hashed_path.write_text(content, encoding="utf-8")
    contents_path.unlink()
    print(f"[hash:{year_dir.name}] Hashed sidebar config -> {hashed_filename}")

    old_rel = contents_path.relative_to(year_dir).as_posix()
    new_rel = hashed_path.relative_to(year_dir).as_posix()
    return hashed_filename, {old_rel: new_rel}


def rewrite_markdown_references(year_dir: Path, contents_hashed: str | None, markdown_name_map: dict[str, str]) -> None:
    for html_path in year_dir.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        original = text

        if contents_hashed:
            text = text.replace("fetch('markdown/contents.json')", f"fetch('markdown/{contents_hashed}')")
            text = text.replace('fetch("markdown/contents.json")', f'fetch("markdown/{contents_hashed}")')

        for original_name, hashed_name_value in markdown_name_map.items():
            text = text.replace(f"'{original_name}'", f"'{hashed_name_value}'")
            text = text.replace(f'"{original_name}"', f'"{hashed_name_value}"')

        if text != original:
            html_path.write_text(text, encoding="utf-8")


def hash_selected_files(scope_dir: Path, targets: list[str], skip_markdown_paths: bool) -> tuple[dict[str, str], str | None]:
    mapping: dict[str, str] = {}
    hashed_index_filename: str | None = None

    print(
        f"[hash:{scope_dir.name}] Hashing selected files | "
        f"targets={targets} skip_markdown_paths={skip_markdown_paths}"
    )

    for path in sorted(resolve_target_files(scope_dir, targets)):
        rel = path.relative_to(scope_dir).as_posix()
        if rel in {"file_hashing.txt", RELEASE_STATE_FILENAME, RELEASE_MANIFEST_FILENAME, RELEASE_CONFIG_FILENAME}:
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

    print(f"[hash:{scope_dir.name}] Hashed {len(mapping)} files")

    return mapping, hashed_index_filename


def rewrite_paths_in_text_files(scope_dir: Path, path_map: dict[str, str], recursive: bool) -> None:
    if not path_map:
        print(f"[rewrite:{scope_dir.name}] No path mappings. Skipping text rewrite.")
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
    print(f"[rewrite:{scope_dir.name}] Applied {len(path_map)} path mappings (recursive={recursive})")


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
    print(f"[loader:{scope_dir.name}] index.html now redirects to {hashed_index_filename}")


def process_root() -> dict[str, str]:
    print("[root] Processing root hashing and rewrites")
    targets = read_hash_targets(ROOT / "file_hashing.txt", DEFAULT_ROOT_HASH_TARGETS)
    selected_map, hashed_index_filename = hash_selected_files(DIST, targets, skip_markdown_paths=False)
    rewrite_paths_in_text_files(DIST, selected_map, recursive=False)
    if hashed_index_filename:
        create_index_loader(DIST, hashed_index_filename)
    print(f"[root] Completed with {len(selected_map)} mapped files")
    return selected_map


def process_year(year: str, root_map: dict[str, str]) -> None:
    year_dir = DIST / year
    if not year_dir.exists():
        print(f"[year:{year}] Directory not found in dist. Skipping.")
        return

    print(f"[year:{year}] Start processing")

    source_year_dir = ROOT / year
    repo_slug = get_github_repo_slug()
    release_url_map = sync_release_assets(year, source_year_dir, repo_slug)

    targets = read_hash_targets(ROOT / year / "file_hashing.txt", DEFAULT_YEAR_HASH_TARGETS)
    contains_markdown = any(is_markdown_target(target) for target in targets)

    global_map: dict[str, str] = {}
    markdown_name_map: dict[str, str] = {}
    contents_hashed: str | None = None

    if contains_markdown:
        markdown_name_map, markdown_path_map = hash_markdown_files(year_dir, release_url_map)
        contents_hashed, sidebar_map = hash_contents_json(year_dir, markdown_name_map)
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
        rewrite_markdown_references(year_dir, contents_hashed, markdown_name_map)

    rewrite_paths_in_text_files(year_dir, global_map, recursive=True)

    if hashed_index_filename:
        create_index_loader(year_dir, hashed_index_filename)
    print(f"[year:{year}] Completed | mapped_paths={len(global_map)}")


def build_dist() -> None:
    print("[build] Build started")
    create_default_hashing_config()
    create_default_release_config()
    sync_release_gitignore()
    remove_release_files_from_git_tracking()
    copy_source_to_dist()
    root_map = process_root()
    for year in YEARS:
        process_year(year, root_map)
    print("[build] Build finished")


def main() -> None:
    build_dist()
    print(f"Built hashed dist at: {DIST}")


if __name__ == "__main__":
    main()
