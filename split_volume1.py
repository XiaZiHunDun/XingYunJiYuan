#!/usr/bin/env python3
"""Split volume1_full.md into individual chapter files."""

input_file = "/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/volume1_full.md"
output_dir = "/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/src/volume1/"

import os
import re

def chinese_to_arabic(num_str):
    chinese_map = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    }

    # Strip 第 and 章
    num_str = num_str.replace('第', '').replace('章', '')

    if num_str == '零':
        return 0

    result = 0
    temp = 0

    for char in num_str:
        if char == '十':
            result += max(temp, 1) * 10
            temp = 0
        elif char == '百':
            result += max(temp, 1) * 100
            temp = 0
        else:
            temp = temp * 10 + chinese_map.get(char, 0)

    return result + temp

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by chapter headers
chapters = re.split(r'(?=^# [第零一二三四五六七八九十百]+章)', content, flags=re.MULTILINE)

chapter_files = []
for chapter in chapters:
    if not chapter.strip():
        continue
    # Extract chapter number from header
    match = re.search(r'^# ([第零一二三四五六七八九十百]+章)\s+(.+?)$', chapter, re.MULTILINE)
    if match:
        chapter_num_str = match.group(1)
        chapter_title = match.group(2).strip()
        arabic_num = chinese_to_arabic(chapter_num_str)
        file_num = f"ch{arabic_num:03d}"
        filename = f"{file_num}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(chapter.strip())
            f.write('\n')

        chapter_files.append((filename, chapter_num_str, chapter_title, len(chapter)))

print(f"Created {len(chapter_files)} chapter files")
for f, num, title, length in chapter_files[:15]:
    print(f"  {f}: {num} {title} ({length} chars)")
print("...")
for f, num, title, length in chapter_files[-10:]:
    print(f"  {f}: {num} {title} ({length} chars)")

# Check file count
files = [f for f in os.listdir(output_dir) if f.endswith('.md')]
print(f"\nTotal .md files in {output_dir}: {len(files)}")
