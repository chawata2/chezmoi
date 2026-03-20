"""
Obsidian vault の Notes/ ディレクトリをキーワードとタグで検索する。

使い方:
  python3 search_notes.py <キーワード> [<キーワード> ...]

  キーワードはスペース区切りで複数指定可能。
  いずれか1つにマッチするノートを返す（OR検索）。

出力: マッチしたノートのパスを1行1ファイルで stdout に出力。
"""

import os
import re
import sys
from typing import Optional


VAULT_NOTES = os.path.expanduser("~/Documents/vault/Notes/")


def extract_frontmatter(content: str) -> Optional[str]:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    return match.group(1) if match else None


def get_tags(frontmatter: str) -> list[str]:
    # インライン形式: tags: [foo, bar]
    inline = re.search(r"^tags:\s*\[([^\]]+)\]", frontmatter, re.MULTILINE)
    if inline:
        return [t.strip().lower() for t in inline.group(1).split(",") if t.strip()]

    # 複数行形式: tags:\n  - foo
    if re.search(r"^tags:\s*$", frontmatter, re.MULTILINE):
        in_tags = False
        tags = []
        for line in frontmatter.splitlines():
            if re.match(r"^tags:\s*$", line):
                in_tags = True
                continue
            if in_tags:
                item = re.match(r"^\s+- (.+)$", line)
                if item:
                    tags.append(item.group(1).strip().lower())
                else:
                    break
        return tags

    return []


def search(keywords: list[str]) -> list[str]:
    """キーワードにマッチするノートのパスを返す（大文字小文字無視）。"""
    keywords_lower = [k.lower() for k in keywords]
    matched = []

    for filename in sorted(os.listdir(VAULT_NOTES)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(VAULT_NOTES, filename)
        try:
            content = open(filepath, encoding="utf-8").read()
        except OSError:
            continue

        content_lower = content.lower()
        title_lower = os.path.splitext(filename)[0].lower()
        fm = extract_frontmatter(content)
        tags = get_tags(fm) if fm else []

        for kw in keywords_lower:
            # タイトル・タグ・本文のいずれかにマッチすれば採用
            if kw in title_lower or kw in tags or kw in content_lower:
                matched.append(filepath)
                break  # 同じファイルを重複追加しない

    return matched


def main():
    if len(sys.argv) < 2:
        print("Usage: search_notes.py <keyword> [<keyword> ...]", file=sys.stderr)
        sys.exit(1)

    keywords = sys.argv[1:]
    results = search(keywords)
    for path in results:
        print(path)


if __name__ == "__main__":
    main()
