#!/usr/bin/env python3
"""修复林夜（男性主角）的性别代词错误"""

import re
from pathlib import Path

BASE_DIR = Path("/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/src")

def is_in_dialogue(line, pos):
    quote_count = 0
    for i, c in enumerate(line):
        if c == '"':
            quote_count += 1
        if i == pos:
            return quote_count % 2 == 1
    return False

def get_sentence_range(line, pos):
    start = 0
    for i in range(pos - 1, -1, -1):
        if line[i] in '。！？':
            start = i + 1
            break
    end = len(line)
    for i in range(pos + 1, len(line)):
        if line[i] in '。！？':
            end = i
            break
    return start, end

def fix_linye_pronoun(line):
    linye_positions = [m.start() for m in re.finditer('林夜', line)]
    if not linye_positions:
        return line, 0

    result = []
    last_end = 0
    changes = 0

    for match in re.finditer('她', line):
        pos = match.start()
        should_fix = False

        for linye_pos in linye_positions:
            sent_start, sent_end = get_sentence_range(line, linye_pos)
            if sent_start <= pos <= sent_end:
                if not is_in_dialogue(line, pos):
                    sent_text = line[sent_start:sent_end]
                    linye_in_sent = linye_pos - sent_start
                    between = sent_text[linye_in_sent + 2 : pos - sent_start]

                    gan_zhi_patterns = ['感觉到', '感到', '意识到', '看到', '听到', '知道', '理解', '相信', '觉得']
                    for p in gan_zhi_patterns:
                        if p in between:
                            should_fix = True
                            break

                    if not should_fix:
                        zi_sheng_patterns = ['心中', '体内', '身体', '经脉', '灵力', '星尘', '能量', '力量', '眼中', '脸上']
                        for p in zi_sheng_patterns:
                            if p in between:
                                should_fix = True
                                break

        if should_fix:
            result.append(line[last_end:pos])
            result.append('他')
            last_end = pos + 1
            changes += 1
        else:
            result.append(line[last_end:pos+1])
            last_end = pos + 1

    if changes == 0:
        return line, 0

    result.append(line[last_end:])
    return ''.join(result), changes

def main():
    total_changes = 0
    fixed_files = 0

    for vol_dir in sorted(BASE_DIR.glob('volume*')):
        if not vol_dir.is_dir():
            continue

        for md_file in sorted(vol_dir.glob('*.md')):
            if md_file.name.endswith('.py'):
                continue

            content = md_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            new_lines = []
            file_changes = 0

            for line in lines:
                if '林夜' in line and '她' in line:
                    new_line, changes = fix_linye_pronoun(line)
                    new_lines.append(new_line)
                    file_changes += changes
                else:
                    new_lines.append(line)

            if file_changes > 0:
                md_file.write_text('\n'.join(new_lines), encoding='utf-8')
                print(f"[修复] {md_file.relative_to(BASE_DIR)}: {file_changes}处")
                total_changes += file_changes
                fixed_files += 1

    print(f"\n总计: 修复了{total_changes}处, 涉及{fixed_files}个文件")

if __name__ == "__main__":
    main()