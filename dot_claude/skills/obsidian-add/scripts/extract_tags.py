"""
Obsidian vault の Notes/ ディレクトリから全タグを抽出する。

対応形式:
  インライン:  tags: [foo, bar]
  複数行:      tags:
                 - foo
                 - bar

出力: ソート済みの一意なタグを1行1タグで stdout に出力。
"""

import os
import re
from typing import Optional


VAULT_NOTES = os.path.expanduser("~/Documents/vault/Notes/")


def extract_frontmatter(content: str) -> Optional[str]:
    """ファイル先頭の --- ... --- を抽出して返す。なければ None。"""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    return match.group(1) if match else None


def parse_tags(frontmatter: str) -> list[str]:
    """frontmatter 文字列からタグ一覧を返す。"""
    # インライン形式: tags: [foo, bar]
    inline = re.search(r"^tags:\s*\[([^\]]+)\]", frontmatter, re.MULTILINE)
    if inline:
        return [t.strip() for t in inline.group(1).split(",") if t.strip()]

    # 複数行形式: tags:\n  - foo\n  - bar
    if re.search(r"^tags:\s*$", frontmatter, re.MULTILINE):
        # tags: の次行以降の "  - value" を収集
        in_tags = False
        tags = []
        for line in frontmatter.splitlines():
            if re.match(r"^tags:\s*$", line):
                in_tags = True
                continue
            if in_tags:
                item = re.match(r"^\s+- (.+)$", line)
                if item:
                    tags.append(item.group(1).strip())
                else:
                    break  # インデントが切れたらタグブロック終了
        return tags

    return []


def main():
    all_tags: set[str] = set()

    for filename in os.listdir(VAULT_NOTES):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(VAULT_NOTES, filename)
        try:
            content = open(filepath, encoding="utf-8").read()
        except OSError:
            continue

        fm = extract_frontmatter(content)
        if fm:
            all_tags.update(parse_tags(fm))

    for tag in sorted(all_tags):
        print(tag)


if __name__ == "__main__":
    main()
