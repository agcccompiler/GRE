import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS_DIR = ROOT / "words"
LIST_FILES = [WORDS_DIR / f"list{i}.txt" for i in range(11, 16)]

SUMMARY_DIR = WORDS_DIR / "list1-15"
CSV_PATH = SUMMARY_DIR / "list1-15summary-anki-en-zh.csv"
BLANK_MD_PATH = SUMMARY_DIR / "list1-15summary-blank.md"
SUMMARY_MD_PATH = SUMMARY_DIR / "list1-15summary.md"


def parse_list_words(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    words: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or re.match(r"^u\d+:", line):
            continue
        parts = [p.strip() for p in line.split(",")]
        for p in parts:
            if not p:
                continue
            # keep tildes and slashes as-is; strip stray trailing punctuation/spaces
            token = p.strip()
            # normalize internal multiple spaces
            token = re.sub(r"\s+", " ", token)
            words.append(token)
    return words


def load_existing_words_from_blank_md(path: Path) -> set[str]:
    existing: set[str] = set()
    if not path.exists():
        return existing
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.rstrip("\n")
        if not line.startswith("|"):
            continue
        if "---" in line:
            # header separator
            continue
        cols = [c.strip() for c in line.split("|")]
        # Expected: ['', word1, meaning1, word2, meaning2, '']
        if len(cols) >= 3 and cols[1] and cols[1] != "Word":
            existing.add(cols[1])
        if len(cols) >= 5 and cols[3]:
            existing.add(cols[3])
    return existing


def load_existing_words_from_csv(path: Path) -> set[str]:
    existing: set[str] = set()
    if not path.exists():
        return existing
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        word = line.split(",", 1)[0].strip()
        if word:
            existing.add(word)
    return existing


def load_existing_words_from_summary_md(path: Path) -> set[str]:
    existing: set[str] = set()
    if not path.exists():
        return existing
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        if "---" in line:
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) >= 3 and cols[1] and cols[1] not in {"单词", "Word"}:
            existing.add(cols[1])
        if len(cols) >= 5 and cols[3]:
            existing.add(cols[3])
    return existing


def append_rows_to_blank_md(path: Path, new_words: list[str]) -> None:
    if not new_words:
        return
    lines = []
    # Pair words into two per row
    it = iter(new_words)
    for w1 in it:
        w2 = next(it, "")
        lines.append(f"| {w1} |  | {w2} |  |")
    with path.open("a", encoding="utf-8") as f:
        f.write("\n")
        for line in lines:
            f.write(line + "\n")


def ensure_summary_md_section(path: Path) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if "## list11-15 待补充词表" in text:
        return
    with path.open("a", encoding="utf-8") as f:
        f.write("\n## list11-15 待补充词表\n\n")
        f.write("| 单词 | 释义 | 单词 | 释义 |\n")
        f.write("| --- | --- | --- | --- |\n")


def append_rows_to_summary_md(path: Path, new_words: list[str]) -> None:
    if not new_words:
        return
    ensure_summary_md_section(path)
    lines = []
    it = iter(new_words)
    for w1 in it:
        w2 = next(it, "")
        lines.append(f"| {w1} |  | {w2} |  |")
    with path.open("a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def append_to_csv(path: Path, new_words: list[str]) -> None:
    if not new_words:
        return
    with path.open("a", encoding="utf-8") as f:
        for w in new_words:
            f.write(f"{w},\n")


def main() -> None:
    # gather new words from list11-15
    all_new: list[str] = []
    seen: set[str] = set()
    for p in LIST_FILES:
        for w in parse_list_words(p):
            if w and w not in seen:
                seen.add(w)
                all_new.append(w)

    # existing entries
    existing_blank = load_existing_words_from_blank_md(BLANK_MD_PATH)
    existing_csv = load_existing_words_from_csv(CSV_PATH)
    existing_summary = load_existing_words_from_summary_md(SUMMARY_MD_PATH)

    # filter missing for each destination
    missing_for_blank = [w for w in all_new if w not in existing_blank]
    missing_for_csv = [w for w in all_new if w not in existing_csv]
    missing_for_summary = [w for w in all_new if w not in existing_summary]

    # append
    append_rows_to_blank_md(BLANK_MD_PATH, missing_for_blank)
    append_to_csv(CSV_PATH, missing_for_csv)
    append_rows_to_summary_md(SUMMARY_MD_PATH, missing_for_summary)

    # simple report
    print(f"New words parsed: {len(all_new)}")
    print(f"Added to blank.md: {len(missing_for_blank)}")
    print(f"Added to csv: {len(missing_for_csv)}")
    print(f"Added to summary.md: {len(missing_for_summary)}")


if __name__ == "__main__":
    main()


