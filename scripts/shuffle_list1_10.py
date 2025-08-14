import io
import os
import random
import csv

"""
通用单词表打乱脚本（无需 CLI，直接运行脚本）

支持两类表头：
- 中文表头：| 单词 | 释义 | 单词 | 释义 |
- 英文表头：| Word | Meaning | Word | Meaning |

脚本会：
1) 在 BASE_DIRS 下递归扫描 .md 文件；
2) 自动识别是否包含上述任一表格；
3) 打乱表格中的单词顺序并原地重写 markdown；
4) 生成 Anki CSV（无表头，Front=单词，Back=空），与原 md 同目录，文件名为 <md文件名>-anki.csv。

使用方式：
1) 配置 BASE_DIRS（可多个）；
2) 直接运行本脚本。
"""

# ========= 需按需配置的区域 =========
# 缺省：以脚本上级目录作为扫描根目录（通常是你的项目根目录）
_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
_DEFAULT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, ".."))
BASE_DIRS = [
    _DEFAULT_ROOT,
]

# 设置随机种子（固定顺序时设置一个整数；为 None 则每次不同）
RANDOM_SEED = None

# 是否为检测到的中文/英文表格生成 Anki CSV（Front=word, Back=空）
GENERATE_CSV_FOR_CN = True
GENERATE_CSV_FOR_EN = True

# 递归扫描子目录
SCAN_RECURSIVELY = True
# ====================================


def _find_table_block(lines, header_predicate):
    header_idx = None
    for i, line in enumerate(lines):
        if header_predicate(line.strip()):
            header_idx = i
            break
    if header_idx is None:
        return None, None
    j = header_idx + 1
    while j < len(lines) and lines[j].strip().startswith("|"):
        j += 1
    end_idx = j
    return header_idx, end_idx


def shuffle_cn_table(path):
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    def is_header(s):
        return s.startswith("| 单词") and ("释义" in s)

    header_idx, end_idx = _find_table_block(lines, is_header)
    if header_idx is None:
        return

    # parse pairs (word, meaning)
    pairs = []
    for k in range(header_idx + 2, end_idx):
        parts = [p.strip() for p in lines[k].split("|")]
        if len(parts) >= 5:
            w1, m1, w2, m2 = parts[1], parts[2], parts[3], parts[4]
            if w1:
                pairs.append((w1, m1))
            if w2:
                pairs.append((w2, m2))

    random.shuffle(pairs)

    # rebuild table (two columns of words per row)
    new_tbl = [
        "| 单词 | 释义 | 单词 | 释义 |",
        "| --- | --- | --- | --- |",
    ]
    for i in range(0, len(pairs), 2):
        a = pairs[i]
        b = pairs[i + 1] if i + 1 < len(pairs) else ("", "")
        new_tbl.append(f"| {a[0]} | {a[1]} | {b[0]} | {b[1]} |")

    new_lines = lines[:header_idx] + new_tbl + lines[end_idx:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    # return just the word list for CSV
    return [w for (w, _) in pairs]


def shuffle_en_blank_table_and_words(blank_md_path):
    with io.open(blank_md_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    def is_header(s):
        return s.startswith("| Word") and ("Meaning" in s)

    header_idx, end_idx = _find_table_block(lines, is_header)
    if header_idx is None:
        return []

    words = []
    for k in range(header_idx + 2, end_idx):
        parts = [p.strip() for p in lines[k].split("|")]
        if len(parts) >= 5:
            w1, w2 = parts[1], parts[3]
            if w1:
                words.append(w1)
            if w2:
                words.append(w2)

    random.shuffle(words)

    # Rebuild blank table with shuffled words
    new_tbl = [
        "| Word | Meaning | Word | Meaning |",
        "| --- | --- | --- | --- |",
    ]
    for i in range(0, len(words), 2):
        w1 = words[i]
        w2 = words[i + 1] if i + 1 < len(words) else ""
        new_tbl.append(f"| {w1} |  | {w2} |  |")

    new_lines = lines[:header_idx] + new_tbl + lines[end_idx:]
    with io.open(blank_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    return words


def write_anki_csv(csv_path, words):
    # Write Anki CSV (no header, Front,Back)
    with io.open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for w in words:
            writer.writerow([w, ""])  # Back left empty on purpose


def _process_md_file(md_path):
    # Try CN table first
    with io.open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Quick check for headers to avoid unnecessary parsing
    has_cn_header = ("| 单词" in content and "释义" in content)
    has_en_header = ("| Word" in content and "Meaning" in content)

    words_out = []
    kind = None

    if has_cn_header:
        words_out = shuffle_cn_table(md_path)
        kind = "CN"
    elif has_en_header:
        words_out = shuffle_en_blank_table_and_words(md_path)
        kind = "EN"
    else:
        return None  # not processed

    # Write CSV next to md
    csv_path = os.path.splitext(md_path)[0] + "-anki.csv"
    if kind == "CN" and GENERATE_CSV_FOR_CN and words_out:
        write_anki_csv(csv_path, words_out)
        return csv_path
    if kind == "EN" and GENERATE_CSV_FOR_EN and words_out:
        write_anki_csv(csv_path, words_out)
        return csv_path
    return None


def _iter_md_files(base_dir):
    if not os.path.isdir(base_dir):
        return
    if SCAN_RECURSIVELY:
        for root, _dirs, files in os.walk(base_dir):
            for name in files:
                if name.lower().endswith(".md"):
                    yield os.path.join(root, name)
    else:
        for name in os.listdir(base_dir):
            p = os.path.join(base_dir, name)
            if os.path.isfile(p) and name.lower().endswith(".md"):
                yield p


if __name__ == "__main__":
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    generated = []
    touched = 0
    for base in BASE_DIRS:
        for md in _iter_md_files(base):
            csv_path = _process_md_file(md)
            if csv_path:
                generated.append(csv_path)
                touched += 1

    print("Processed markdown files:", touched)
    if generated:
        print("Generated CSVs:")
        for p in generated:
            print("  ", p)
    else:
        print("No CSV generated (check GENERATE_CSV_FOR_* settings or tables).")


