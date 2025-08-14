import io
import os
import csv


MD_PATH = "/Users/jinchengguo/gre/words/list1-10/list1-10summary.md"
CSV_PATH = "/Users/jinchengguo/gre/words/list1-10/list1-10summary-anki-en-zh.csv"


def extract_en_zh_pairs_from_md(md_path):
    with io.open(md_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Find the CN table header "| 单词 | 释义 | 单词 | 释义 |"
    header_idx = None
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("| 单词") and ("释义" in s):
            header_idx = i
            break
    if header_idx is None:
        return []

    # Find end of the continuous table block (lines starting with '|')
    j = header_idx + 1
    while j < len(lines) and lines[j].strip().startswith("|"):
        j += 1
    end_idx = j

    # Parse pairs (word, meaning) from rows (skip the separator line right after header)
    pairs = []
    for k in range(header_idx + 2, end_idx):
        parts = [p.strip() for p in lines[k].split("|")]
        if len(parts) >= 5:
            w1, m1, w2, m2 = parts[1], parts[2], parts[3], parts[4]
            if w1:
                pairs.append((w1, m1))
            if w2:
                pairs.append((w2, m2))
    return pairs


def write_csv(csv_path, pairs):
    # CSV without header: Front (English), Back (Chinese)
    with io.open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for en, zh in pairs:
            writer.writerow([en, zh])


if __name__ == "__main__":
    pairs = extract_en_zh_pairs_from_md(MD_PATH)
    write_csv(CSV_PATH, pairs)
    print("Exported:", CSV_PATH, "items:", len(pairs))


