#!/usr/bin/env python3
"""
精修《星陨纪元》第161-200章
- 删除每章末尾的模板化重复段落
- 删除"扩写"部分
- 删除套话
- 保留正文骨架和"**本章完**"标记
"""

import re
import os
from pathlib import Path

BASE_DIR = Path("/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/src/volume2")

# 套话模式（按行处理）
CLICHES_LINES = [
    "星光在他们身上流转，见证着这一刻。",
    "星光在他们身上流转。",
    "见证着这一刻",
    "传奇的篇章正在书写",
    "他们的身影在星空中划过，如同两颗璀璨的流星，带着永恒的光芒，照亮着这片被黑暗笼罩的虚空。",
    "因为他们是守护者。",
    "这是他们的使命，也是他们的选择。",
    "直到永远。",
    "这就是守护者的使命。永远不会改变。",
    "这就是守护者的精神。\n\n永远传承。",
    "这就是星陨纪元的故事。永远不会结束。",
    "永远传承。",
    "永远不会结束。",
    "无论前方有什么在等待着他们，他们都会一起面对。",
    "这就是守护者的传承。",
    "这就是守护者的精神。永远与人民在一起。",
    "这就是守护者的力量。永远不会退缩。",
    "这就是守护者的成就。永远不会磨灭。",
    "这就是守护者的幸福。永远不会改变。",
    "这就是守护者的爱情。与星辰同在，与宇宙永恒。",
    "星光在窗外闪烁，见证着他们的爱情。",
    "星光在窗外闪烁，仿佛在为这对爱侣祝福。",
    "星光在飞船周围流转，见证着这对爱侣的旅程。",
    "这就是林夜和苏琳的爱情。与星辰同在，与宇宙永恒。",
    "这就是守护者的使命。永远不会改变。",
    "这就是守护者的精神。\n\n永远传承。",
    "星光在他们身上流转，见证着这个守护者家庭的幸福。",
    "星光在宇宙边缘流转，。",
]

# 扩写章节标题模式
KUO_XIE_PATTERN = re.compile(r'^## 【扩写\d+：[^】]+】', re.MULTILINE)

def count_chars(text):
    """统计字符数（不含空白）"""
    return len(re.sub(r'\s', '', text))

def count_words(text):
    """统计字数（按中文习惯，不含标点和空白）"""
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))
    english = len(re.findall(r'[a-zA-Z]+', text))
    return cjk + english

def process_content(content):
    """处理章节内容"""
    lines = content.split('\n')
    processed_lines = []
    in_kuo_xie = False

    for i, line in enumerate(lines):
        # 检测扩写章节开始
        if KUO_XIE_PATTERN.match(line):
            in_kuo_xie = True
            continue

        # 检测下一个扩写或正文开始
        if in_kuo_xie and (line.startswith('## 【扩写') or (line.startswith('# 第') and '章' in line)):
            in_kuo_xie = False

        # 跳过扩写内容
        if in_kuo_xie:
            continue

        # 删除套话
        for cliché in CLICHES_LINES:
            if cliché in line:
                line = line.replace(cliché, '')

        # 跳过完全为空的引用行
        if re.match(r'^""$', line.strip()):
            continue

        # 跳过只有标点的行
        if re.match(r'^[\s\.,，。、；；：：“”‘’（）【】《》!?！？]+$', line.strip()):
            continue

        processed_lines.append(line)

    content = '\n'.join(processed_lines)

    # 清理多余的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    return content

def process_chapter(filepath):
    """处理单个章节文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_chars = count_chars(content)
    original_words = count_words(content)

    # 找到第一个 **本章完** 的位置
    # 这标志着本章的结束，其后的内容是下一章的预览（应删除）
    first_end_match = re.search(r'\*\*本章完\*\*', content)

    if first_end_match:
        # 保留到第一个 **本章完** 之后
        end_pos = first_end_match.end()
        content = content[:end_pos]

    # 处理内容（删除扩写和套话）
    content = process_content(content)

    # 确保以 **本章完** 结尾
    if not content.rstrip().endswith('**本章完**'):
        content = content.rstrip() + '\n\n**本章完**'

    new_chars = count_chars(content)
    new_words = count_words(content)

    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return original_chars, original_words, new_chars, new_words

def main():
    files = []
    for i in range(161, 201):
        filepath = BASE_DIR / f"ch{i}.md"
        if filepath.exists():
            files.append(filepath)

    print(f"处理 {len(files)} 个文件: ch161.md - ch200.md")
    print("=" * 60)

    total_original_chars = 0
    total_original_words = 0
    total_new_chars = 0
    total_new_words = 0

    for filepath in sorted(files):
        orig_c, orig_w, new_c, new_w = process_chapter(filepath)
        total_original_chars += orig_c
        total_original_words += orig_w
        total_new_chars += new_c
        total_new_words += new_w

        chapter_num = filepath.stem[2:]
        print(f"ch{chapter_num}: {orig_c} -> {new_c} 字符 (删除 {orig_c - new_c})")

    print("=" * 60)
    print(f"总计:")
    print(f"  处理前: {total_original_chars} 字符, {total_original_words} 字")
    print(f"  处理后: {total_new_chars} 字符, {total_new_words} 字")
    print(f"  删除: {total_original_chars - total_new_chars} 字符 ({(total_original_chars - total_new_chars)/total_original_chars*100:.1f}%)")
    print(f"  删除: {total_original_words - total_new_words} 字 ({(total_original_words - total_new_words)/total_original_words*100:.1f}%)")

if __name__ == "__main__":
    main()
