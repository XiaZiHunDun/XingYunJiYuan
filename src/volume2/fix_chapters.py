#!/usr/bin/env python3
"""
精修《星陨纪元》第121-160章
1. 删除每章末尾200-400字的模板化重复套话
2. 修正ch122/123末尾"裂变境修炼者"→"黑洞境修炼者"
3. 保留正文骨架和"**本章完**"标记
4. 统计处理前后字数变化
"""

import os
import re

BASE_DIR = "/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/src/volume2"

# 需要修正境界名的文件
FIX_REALM_FILES = ["ch122.md", "ch123.md"]

# 模板化套话的典型开头模式
TEMPLETE_START_PATTERNS = [
    r"^漆黑的星空中",
    r"^夜色渐深，枢纽城",
    r"^浩瀚星海之中",
    r"^星海无垠，蕴含",
    r"^浩瀚的星海见证",
    r"^修炼之道漫长",
    r"^林夜的眼中闪烁",
    r"^而他们的故事，将永远流传",
]

def count_chars(content):
    """统计字符数（不含空白）"""
    return len(content.replace("\n", "").replace(" ", ""))

def find_template_start_index(lines):
    """找到模板化套话的开始行索引"""
    for i, line in enumerate(lines):
        stripped = line.strip()
        for pattern in TEMPLETE_START_PATTERNS:
            if re.search(pattern, stripped):
                return i
    return -1

def find_proper_end_marker(lines, before_index):
    """在指定索引之前找到最近的**本文完**标记"""
    for i in range(before_index - 1, -1, -1):
        if "**本章完**" in lines[i]:
            return i
    return -1

def process_chapter(filepath):
    """处理单章文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_char_count = count_chars(content)
    lines = content.split('\n')

    # 找到模板化套话的开始位置
    template_start = find_template_start_index(lines)

    chars_removed = 0
    modified = False

    if template_start >= 0:
        # 找到模板之前的**本章完**标记
        end_marker_before = find_proper_end_marker(lines, template_start)

        if end_marker_before >= 0:
            # 有本章完标记，以它为界
            content_end = end_marker_before + 1
        else:
            # 没有本章完标记，找合适的断点
            content_end = template_start

        # 删除模板化套话
        if content_end < len(lines):
            template_lines = lines[content_end:]
            template_content = '\n'.join(template_lines)
            chars_removed = count_chars(template_content)
            lines = lines[:content_end]
            modified = True

        # 清理末尾空行
        while lines and lines[-1].strip() == '':
            lines.pop()

        # 如果没有本章完，添加一个
        if lines and "**本章完**" not in lines[-1]:
            lines.append("**本章完**")

    # 修正境界名
    filename = os.path.basename(filepath)
    if filename in FIX_REALM_FILES:
        new_content = '\n'.join(lines)
        new_content = new_content.replace("裂变境修炼者", "黑洞境修炼者")
        lines = new_content.split('\n')
        if new_content != content:
            modified = True

    new_content = '\n'.join(lines)
    new_char_count = count_chars(new_content)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return original_char_count, new_char_count, chars_removed, modified

def main():
    files_to_process = []
    for i in range(121, 161):
        filepath = os.path.join(BASE_DIR, f"ch{i}.md")
        if os.path.exists(filepath):
            files_to_process.append(filepath)

    print(f"{'文件':<15} {'处理前':<10} {'处理后':<10} {'删除字数':<10} {'状态'}")
    print("-" * 60)

    total_original = 0
    total_new = 0
    total_removed = 0

    for filepath in sorted(files_to_process):
        filename = os.path.basename(filepath)
        orig, new, removed, modified = process_chapter(filepath)

        total_original += orig
        total_new += new
        total_removed += removed

        status = "已修改" if modified else "无需修改"
        print(f"{filename:<15} {orig:<10} {new:<10} {removed:<10} {status}")

    print("-" * 60)
    print(f"{'总计':<15} {total_original:<10} {total_new:<10} {total_removed:<10}")

if __name__ == "__main__":
    main()
