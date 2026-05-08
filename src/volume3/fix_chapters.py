#!/usr/bin/env python3
"""
精修《星陨纪元》第三卷第241-280章
1. 删除每章末尾模板化重复段落
2. 删除套话
3. 修正林夜的人称代词：他→她（精确替换）
4. 保留正文骨架和"**本章完**"标记
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/src/volume3")

# 需要删除的模板段落起始关键词（用于识别模板块的开始）
TEMPLATE_STARTERS = [
    # 主要星海/修炼主题开头
    "虚无的星海蕴含着无穷的力量",
    "虚无的星海广阔",
    "星海无垠",
    "虚无的星海蕴含着无数奥秘",
    "星海浩瀚蕴含着无数奥秘",
    "星光在宇宙中流转，见证着这一切",
    "星光在星辰殿中流转",
    "虚无的星海见证了无数传奇的诞生",
    "虚无的星海见证了无数修炼者的崛起与陨落",
    "永恒的守望",

    # 林夜相关开头
    "林夜的意志如同星辰般璀璨",
    "林夜的脚步从未停歇",
    "林夜的眼中闪烁着坚定的光芒",
    "林夜的身影在星海中显得渺小",

    # 战斗/同伴相关开头
    "战斗的火花在虚空中迸发",
    "在生死与共的战斗中",
    "能量的波动在空间中回荡",

    # 书卷/篇章相关开头
    "虚无的星海如同一本无尽的书卷",
    "他们的身影在星海中并肩前行",
    "而这片星海，将见证他们的辉煌",

    # 其他套话开头
    "而他们的征途，才刚刚开始。",
    "而这一切，都只是开始。",
    "林夜的心中燃烧着不屈的斗志",
    "林夜的心中燃烧着不灭的斗志",
    "境界的提升不仅仅是力量的增强",
    "在追求力量的道路上，能有同行者相伴",
    "在追求大道的漫漫长路上",
    "而他们的故事，将在这片星海中继续流传。",
    "在这片充满未知的星海中",
    "修炼之路充满了挑战与危险",
    "守护者的使命，超越了时间和空间的限制",
    "星光在虚空中流转",
    "当他们踏入那片未知的星域时",
    "星海浩瀚，蕴含着无数奥秘。",
    "能量波动在虚空中扩散",
    "虚无的星海之中，危机与机遇并存。",
    "在这片星海之中",
    "修炼者攀登高峰的道路",
    "星海无垠，蕴含着无尽的力量与奥秘。",
    "每一次战斗都是对意志的考验",
    "同伴的存在，是修炼道路上最珍贵的财富。",
    "前方的路虽然漫长，但他们从未停止脚步。",
]


def is_template_line(line: str) -> bool:
    """检查一行是否是模板内容"""
    stripped = line.strip()
    for starter in TEMPLATE_STARTERS:
        if stripped.startswith(starter):
            return True
    return False


def replace_linye_pronouns(line: str) -> tuple[str, int]:
    """
    只替换明确属于林夜的"他"为"她"
    通过上下文判断：包含"林夜"且其后紧跟的"他"才替换
    返回: (替换后的行, 替换次数)
    """
    # 策略：只有当"林夜"和"他"在同一句中（中间无句号）时才替换
    # 即：林夜...他...这种情况的"他"替换为"她"

    count = 0
    # 查找所有"林夜...他..."的模式
    # 使用更精确的正则：林夜后直到句号/感叹号/问号之前的所有"他"

    # 分割成句子
    sentences = re.split(r'([。！？])', line)

    new_sentences = []
    for i, part in enumerate(sentences):
        if i % 2 == 0:  # 这是句子内容部分
            # 检查这个句子是否包含林夜
            if '林夜' in part:
                # 在这个句子中，将"他"替换为"她"
                # 使用词边界确保是完整的"他"
                new_part = re.sub(r'\b他\b', '她', part)
                count += part.count("他")
                new_sentences.append(new_part)
            else:
                new_sentences.append(part)
        else:
            # 这是标点符号，保留
            new_sentences.append(part)

    return ''.join(new_sentences), count


def process_chapter(content: str) -> tuple[str, int, int]:
    """
    处理单章内容
    返回: (处理后的内容, 删除的行数, 人称替换数)
    """
    lines = content.splitlines()
    original_line_count = len(lines)

    # Step 1: 删除**本章完**之后的所有模板化段落
    marker = "**本章完**"
    marker_idx = -1
    for i, line in enumerate(lines):
        if marker in line:
            marker_idx = i
            break

    new_lines = []
    if marker_idx >= 0:
        # 保留**本章完**及之前的内容
        new_lines = lines[:marker_idx + 1]

        # 找到marker之后的内容
        after_marker_lines = lines[marker_idx + 1:]

        # 收集非模板内容行（遇到模板块就跳过）
        skip_mode = False
        for line in after_marker_lines:
            stripped = line.strip()

            # 检查是否是模板块的开始
            if is_template_line(stripped):
                skip_mode = True
                continue

            if skip_mode:
                # 在跳过模式中
                if not stripped:  # 空行，继续跳过
                    continue
                else:
                    # 非空行且不是模板，说明遇到了新内容，退出跳过模式
                    skip_mode = False
                    new_lines.append(line)
            else:
                new_lines.append(line)

    else:
        new_lines = lines

    # Step 2: 删除残留的模板套话（在**本章完**之前的正文中也可能有）
    result_lines = []
    skip_mode = False
    for line in new_lines:
        stripped = line.strip()

        # 检查是否是模板块的开始
        if is_template_line(stripped):
            skip_mode = True
            continue

        if skip_mode:
            if not stripped:  # 空行，继续跳过
                continue
            else:
                skip_mode = False
                result_lines.append(line)
        else:
            result_lines.append(line)

    # Step 3: 修正林夜的人称代词 他→她
    # 只替换与林夜同句的"他"为"她"
    pronoun_count = 0
    final_lines = []

    for line in result_lines:
        new_line, count = replace_linye_pronouns(line)
        pronoun_count += count
        final_lines.append(new_line)

    content = "\n".join(final_lines)

    # Step 4: 清理多余的空行（超过2个连续空行的变成2个）
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    final_line_count = len(content.splitlines())

    return content, original_line_count - final_line_count, pronoun_count


def main():
    start_ch = 241
    end_ch = 280

    total_original_chars = 0
    total_new_chars = 0
    total_template_lines_removed = 0
    total_pronoun_changes = 0
    processed_files = 0

    print(f"{'='*60}")
    print(f"精修《星陨纪元》第三卷 第{start_ch}-{end_ch}章")
    print(f"{'='*60}\n")

    for ch_num in range(start_ch, end_ch + 1):
        filename = f"ch{ch_num}.md"
        filepath = BASE_DIR / filename

        if not filepath.exists():
            print(f"[跳过] {filename} - 文件不存在")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            original_content = f.read()

        original_chars = len(original_content)
        new_content, template_removed, pronoun_changes = process_chapter(original_content)
        new_chars = len(new_content)

        # 写回文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        total_original_chars += original_chars
        total_new_chars += new_chars
        total_template_lines_removed += template_removed
        total_pronoun_changes += pronoun_changes
        processed_files += 1

        char_diff = original_chars - new_chars
        print(f"[{filename}] {original_chars}→{new_chars}字 (删{char_diff}字, 替{pronoun_changes}处)")

    print(f"\n{'='*60}")
    print(f"统计结果：")
    print(f"{'='*60}")
    print(f"处理章节数：{processed_files} 章")
    print(f"处理前总字数：{total_original_chars:,} 字")
    print(f"处理后总字数：{total_new_chars:,} 字")
    print(f"删除总字数：{total_original_chars - total_new_chars:,} 字")
    print(f"删除模板段落：约 {total_template_lines_removed} 行")
    print(f"修正人称代词：{total_pronoun_changes} 处")


if __name__ == "__main__":
    main()
