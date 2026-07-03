#!/usr/bin/env python3
"""Deterministic bookkeeping for the task-triage skill. Stdlib only.

Handles what must be exact and reproducible: timestamp parsing, date math
(work weeks, months, years), detecting which notes/periods need analysis
(including mtime-based re-analysis of edited notes), assembling period
inputs with date labels, and mtime manifests for project-context change
detection. All judgment/analysis is done by Claude per the skill's
reference files.

Usage:
  triage.py scan          --notes-dir DIR [--notes-dir DIR2 ...]
  triage.py pending       --notes-dir DIR [--notes-dir DIR2 ...]
  triage.py collect-week  --notes-dir DIR YYYY-MM-DD
  triage.py collect-month --notes-dir DIR YYYY-MM
  triage.py collect-year  --notes-dir DIR YYYY
  triage.py context-scan  [--context-file F] [--context-dir D] [--force]
  triage.py context-mark  LABEL SOURCE_PATH [--context-dir D]

scan:    JSON list of daily notes needing analysis. Each entry: notes file,
         content file to read (.raw_notes.txt for images/PDFs), output path,
         formatted date, and reason (new | edited | needs_ocr). needs_ocr
         entries have no readable text yet — extract text from the image/PDF
         first, save it to raw_notes_path, then rerun scan.
pending: JSON of weeks/months/years whose auto-trigger conditions are met.
collect-*: prints the output path on line 1, then the combined, date-labeled
         source analyses for the period.
context-scan: JSON list of projects from task_context.md with a stale flag
         (true = needs (re-)summarization based on file mtimes).
context-mark: record the current mtime manifest after writing a summary.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

TEXT_EXTENSIONS = {".txt"}
VISUAL_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf"}

# --- project-context file collection rules (mirror original tool) ---
INCLUDED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".rb", ".java",
    ".c", ".h", ".cpp", ".hpp", ".cs", ".swift", ".kt", ".scala",
    ".sh", ".bash", ".zsh", ".fish", ".sql", ".r", ".R", ".jl", ".lua",
    ".pl", ".pm", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg",
    ".conf", ".md", ".rst", ".txt", ".html", ".css", ".scss", ".sass",
    ".less", ".lock", ".gradle", ".cmake",
}
KNOWN_EXTENSIONLESS = {
    "Makefile", "Dockerfile", "Containerfile", "Procfile", "Gemfile",
    "Rakefile", "Vagrantfile", "Justfile",
    ".gitignore", ".gitattributes", ".dockerignore", ".editorconfig",
    ".eslintrc", ".prettierrc", ".babelrc", ".env.example", ".env.template",
}
EXCLUDED_DIRS = {
    ".git", "__pycache__", "node_modules", "venv", ".venv", "env",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".eggs", ".next", ".nuxt", "target", "vendor",
    ".bundle", "coverage", ".coverage", "htmlcov", ".hypothesis", ".nox",
}
MAX_FILE_SIZE = 100_000  # bytes per file


# =========================== date / filename math ===========================

def extract_timestamp(filename: str) -> str | None:
    """Return YYYYMMDD_HHMMSS from a notes filename, or None.

    Strips optional _Page_N suffixes (multi-page scans share one timestamp).
    """
    stem = Path(filename).stem
    if "_Page_" in stem:
        stem = stem.split("_Page_")[0]
    if re.fullmatch(r"\d{8}_\d{6}", stem):
        return stem
    return None


def week_boundaries(date: datetime) -> tuple[datetime, datetime]:
    """Monday 00:00 .. Friday 23:59:59 of the work week containing date."""
    monday = (date - timedelta(days=date.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0)
    friday = (monday + timedelta(days=4)).replace(
        hour=23, minute=59, second=59, microsecond=999999)
    return monday, friday


def month_boundaries(date: datetime) -> tuple[datetime, datetime]:
    start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    nxt = (start.replace(year=start.year + 1, month=1) if start.month == 12
           else start.replace(month=start.month + 1))
    return start, (nxt - timedelta(days=1)).replace(
        hour=23, minute=59, second=59, microsecond=999999)


def parse_triaged_date(path: Path, fmt: str) -> datetime | None:
    try:
        return datetime.strptime(path.stem.split(".")[0], fmt)
    except ValueError:
        return None


# ================================== scan ==================================

def scan_daily(notes_dirs: list[Path]) -> list[dict]:
    """Find daily notes needing (re-)analysis, deduplicated by timestamp."""
    results, seen = [], set()
    for base in notes_dirs:
        if not base.is_dir():
            continue
        daily_dir = base / "daily"
        for notes_path in sorted(base.iterdir(), reverse=True):
            if not notes_path.is_file() or ".triaged." in notes_path.name:
                continue
            if ".raw_notes" in notes_path.name:
                continue  # derived file; its source drives the decision
            suffix = notes_path.suffix.lower()
            if suffix not in TEXT_EXTENSIONS | VISUAL_EXTENSIONS:
                continue
            ts = extract_timestamp(notes_path.name)
            if not ts or ts in seen:
                continue
            try:
                file_date = datetime.strptime(ts, "%Y%m%d_%H%M%S")
            except ValueError:
                continue

            analysis_path = daily_dir / f"{file_date.strftime('%d_%m_%Y')}.triaged.txt"
            raw_notes_path = base / f"{ts}.raw_notes.txt"
            is_visual = suffix in VISUAL_EXTENSIONS

            if analysis_path.exists():
                a_mtime = analysis_path.stat().st_mtime
                edited = notes_path.stat().st_mtime > a_mtime or (
                    raw_notes_path.exists()
                    and raw_notes_path.stat().st_mtime > a_mtime)
                if not edited:
                    seen.add(ts)
                    continue
                reason = "edited"
            else:
                reason = "new"

            content_path = None
            if is_visual:
                if raw_notes_path.exists():
                    content_path = raw_notes_path
                else:
                    reason = "needs_ocr"
            else:
                content_path = notes_path

            results.append({
                "notes_file": str(notes_path),
                "content_file": str(content_path) if content_path else None,
                "raw_notes_path": str(raw_notes_path) if is_visual else None,
                "analysis_path": str(analysis_path),
                "date": file_date.strftime("%A, %B %d, %Y"),
                "reason": reason,
            })
            seen.add(ts)
    return results


# ================================= pending =================================

def _collect_dates(directory: Path, fmt: str) -> list[datetime]:
    if not directory.is_dir():
        return []
    dates = []
    for f in directory.glob("*.triaged.txt"):
        d = parse_triaged_date(f, fmt)
        if d:
            dates.append(d)
    return dates


def pending(notes_dirs: list[Path]) -> dict:
    """Weeks/months/years whose auto-trigger conditions are met.

    Weekly:  5+ weekday daily analyses in a work week, OR week over with >=1.
    Monthly: 4+ weekly analyses in a month, OR month over with >=1.
    Annual:  12 monthly analyses in a year, OR year over with >=1.
    Skips periods whose analysis file already exists (never re-triggered).
    """
    primary = notes_dirs[0]
    now = datetime.now()

    daily_dates = []
    seen = set()
    for base in notes_dirs:
        for d in _collect_dates(base / "daily", "%d_%m_%Y"):
            if d not in seen:
                daily_dates.append(d)
                seen.add(d)

    weeks = {}
    for d in daily_dates:
        ws, we = week_boundaries(d)
        weeks.setdefault(ws, {"end": we, "dates": []})["dates"].append(d)
    weekly_out = []
    for ws, info in sorted(weeks.items()):
        out = primary / "weekly" / f"{ws.strftime('%d_%m_%Y')}.triaged.txt"
        if out.exists():
            continue
        weekdays = sum(1 for d in info["dates"] if d.weekday() < 5)
        if weekdays >= 5 or (now > info["end"] and info["dates"]):
            weekly_out.append({
                "week_start": ws.strftime("%Y-%m-%d"),
                "week_end": info["end"].strftime("%Y-%m-%d"),
                "analysis_path": str(out),
            })

    weekly_dates = _collect_dates(primary / "weekly", "%d_%m_%Y")
    months = {}
    for d in weekly_dates:
        ms, me = month_boundaries(d)
        months.setdefault(ms, {"end": me, "count": 0})
        months[ms]["count"] += 1
    monthly_out = []
    for ms, info in sorted(months.items()):
        out = primary / "monthly" / f"{ms.strftime('%m_%Y')}.triaged.txt"
        if out.exists():
            continue
        if info["count"] >= 4 or (now > info["end"] and info["count"]):
            monthly_out.append({
                "month_start": ms.strftime("%Y-%m-%d"),
                "month_end": info["end"].strftime("%Y-%m-%d"),
                "analysis_path": str(out),
            })

    monthly_dates = _collect_dates(primary / "monthly", "%m_%Y")
    years = {}
    for d in monthly_dates:
        years[d.year] = years.get(d.year, 0) + 1
    annual_out = []
    for year, count in sorted(years.items()):
        out = primary / "annual" / f"{year}.triaged.txt"
        if out.exists():
            continue
        if count >= 12 or (now > datetime(year, 12, 31, 23, 59, 59) and count):
            annual_out.append({"year": year, "analysis_path": str(out)})

    return {"weekly": weekly_out, "monthly": monthly_out, "annual": annual_out}


# ================================= collect =================================

def collect_week(primary: Path, any_date: datetime, notes_dirs: list[Path]) -> tuple[Path, str]:
    ws, we = week_boundaries(any_date)
    sections, seen = [], set()
    for base in notes_dirs:
        for f in sorted((base / "daily").glob("*.triaged.txt")) if (base / "daily").is_dir() else []:
            d = parse_triaged_date(f, "%d_%m_%Y")
            if d and ws <= d <= we and d not in seen:
                sections.append((d, f"## {d.strftime('%A, %B %d, %Y')}\n\n{f.read_text()}"))
                seen.add(d)
    if not sections:
        sys.exit(f"No daily analyses found for week {ws:%Y-%m-%d} .. {we:%Y-%m-%d}")
    sections.sort(key=lambda x: x[0])
    out = primary / "weekly" / f"{ws.strftime('%d_%m_%Y')}.triaged.txt"
    return out, "\n\n---\n\n".join(s for _, s in sections)


def collect_month(primary: Path, month_start: datetime) -> tuple[Path, str]:
    ms, me = month_boundaries(month_start)
    sections = []
    for f in sorted((primary / "weekly").glob("*.triaged.txt")):
        d = parse_triaged_date(f, "%d_%m_%Y")
        if d and ms <= d <= me:
            ws, we = week_boundaries(d)
            label = f"{ws.strftime('%B %d')} - {we.strftime('%B %d, %Y')}"
            sections.append((d, f"## Week of {label}\n\n{f.read_text()}"))
    if not sections:
        sys.exit(f"No weekly analyses found for {ms:%B %Y}")
    sections.sort(key=lambda x: x[0])
    out = primary / "monthly" / f"{ms.strftime('%m_%Y')}.triaged.txt"
    return out, "\n\n---\n\n".join(s for _, s in sections)


def collect_year(primary: Path, year: int) -> tuple[Path, str]:
    sections = []
    for f in sorted((primary / "monthly").glob("*.triaged.txt")):
        d = parse_triaged_date(f, "%m_%Y")
        if d and d.year == year:
            sections.append((d, f"## {d.strftime('%B')} {year}\n\n{f.read_text()}"))
    if not sections:
        sys.exit(f"No monthly analyses found for {year}")
    sections.sort(key=lambda x: x[0])
    return primary / "annual" / f"{year}.triaged.txt", "\n\n---\n\n".join(s for _, s in sections)


# ============================= project context =============================

def sanitize_label(label: str) -> str:
    label = re.sub(r'[/\\:*?"<>|]', "-", label)
    label = re.sub(r"\.\.+", ".", label).strip().lstrip(".")
    label = re.sub(r"\s+", "-", label)
    label = re.sub(r"-{2,}", "-", label).strip("-")
    return label or "unnamed"


def parse_context_file(path: Path) -> list[tuple[str, Path]]:
    """One directory path per line; '#' comments; optional 'label: /path'."""
    if not path.exists():
        return []
    entries = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ": " in line and not line.startswith(("/", "~")):
            label, path_str = (p.strip() for p in line.split(": ", 1))
        else:
            label, path_str = None, line
        p = Path(os.path.expanduser(path_str)).resolve()
        if p.is_dir():
            entries.append((sanitize_label(label or p.name), p))
    return entries


def file_mtimes(directory: Path) -> dict[str, float]:
    """mtimes of files matching the collection rules (skip binary/oversized)."""
    mtimes = {}
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs
                   if d not in EXCLUDED_DIRS and not d.endswith(".egg-info")]
        for name in filenames:
            fp = Path(root) / name
            if name not in KNOWN_EXTENSIONLESS and fp.suffix.lower() not in INCLUDED_EXTENSIONS:
                continue
            try:
                st = fp.stat()
                if st.st_size > MAX_FILE_SIZE:
                    continue
                with open(fp, "rb") as f:
                    f.read(512).decode("utf-8", errors="strict")
                mtimes[str(fp.relative_to(directory))] = st.st_mtime
            except (OSError, UnicodeDecodeError):
                continue
    return mtimes


def context_scan(context_file: Path, context_dir: Path, force: bool) -> list[dict]:
    out = []
    for label, source in parse_context_file(context_file):
        summary = context_dir / f"{label}.context.md"
        meta = context_dir / f"{label}.context.meta.json"
        stale = True
        if not force and summary.exists() and meta.exists():
            try:
                old = json.loads(meta.read_text()).get("file_mtimes", {})
                stale = old != file_mtimes(source)
            except (json.JSONDecodeError, OSError):
                stale = True
        out.append({
            "label": label,
            "source_path": str(source),
            "summary_path": str(summary),
            "stale": stale,
        })
    return out


def context_mark(label: str, source: Path, context_dir: Path) -> None:
    context_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        "source_path": str(source),
        "label": label,
        "summarized_at": datetime.now().isoformat(),
        "file_mtimes": file_mtimes(source),
    }
    (context_dir / f"{label}.context.meta.json").write_text(
        json.dumps(meta, indent=2))


# ================================== main ==================================

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=[
        "scan", "pending", "collect-week", "collect-month", "collect-year",
        "context-scan", "context-mark"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--notes-dir", action="append", type=Path, default=[],
                    help="Notes directory (repeatable; first is primary/output)")
    ap.add_argument("--context-file", type=Path, default=Path("task_context.md"))
    ap.add_argument("--context-dir", type=Path, default=Path("local_context"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_intermixed_args()

    if a.command in ("scan", "pending", "collect-week", "collect-month",
                     "collect-year") and not a.notes_dir:
        ap.error("--notes-dir is required for this command")

    if a.command == "scan":
        print(json.dumps(scan_daily(a.notes_dir), indent=2))
    elif a.command == "pending":
        print(json.dumps(pending(a.notes_dir), indent=2))
    elif a.command == "collect-week":
        date = datetime.strptime(a.args[0], "%Y-%m-%d")
        out, text = collect_week(a.notes_dir[0], date, a.notes_dir)
        print(out)
        print(text)
    elif a.command == "collect-month":
        date = datetime.strptime(a.args[0], "%Y-%m")
        out, text = collect_month(a.notes_dir[0], date)
        print(out)
        print(text)
    elif a.command == "collect-year":
        out, text = collect_year(a.notes_dir[0], int(a.args[0]))
        print(out)
        print(text)
    elif a.command == "context-scan":
        print(json.dumps(context_scan(a.context_file, a.context_dir, a.force),
                         indent=2))
    elif a.command == "context-mark":
        context_mark(a.args[0], Path(a.args[1]).resolve(), a.context_dir)
        print(f"Manifest saved for {a.args[0]}")


if __name__ == "__main__":
    main()
