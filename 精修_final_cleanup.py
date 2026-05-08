#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终清理：删除本章完之前的多余分隔线"""

import os
import re

BASE_PATH = "/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/src/volume3"

def read_chapter(n):
    with open(os.path.join(BASE_PATH, f"ch{n}.md"), 'r', encoding='utf-8') as f:
        return f.read()

def write_chapter(n, content):
    with open(os.path.join(BASE_PATH, f"ch{n}.md"), 'w', encoding='utf-8') as f:
        f.write(content)

def cleanup(content):
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测到**本章完**
        if '**本章完**' in line:
            new_lines.append(line)
            # 跳过之后所有的---
            i = i + 1
            while i < len(lines):
                if lines[i].strip() == '---':
                    i = i + 1
                else:
                    break
            continue
        
        new_lines.append(line)
        i = i + 1
    
    content = '\n'.join(new_lines)
    
    # 清理：多个连续的---只保留一个
    content = re.sub(r'---{3,}', '---\n\n---', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

def main():
    total_before = 0
    total_after = 0
    
    for n in range(321, 361):
        content = read_chapter(n)
        before = len(content.replace('\n', ''))
        total_before += before
        
        content = cleanup(content)
        
        after = len(content.replace('\n', ''))
        total_after += after
        
        if before != after:
            print(f"ch{n}: {before} -> {after} ({after - before:+d})")
            write_chapter(n, content)
        else:
            print(f"ch{n}: {before} (无变化)")
    
    print(f"\n总计: {total_before} -> {total_after} ({total_after - total_before:+d})")

if __name__ == "__main__":
    main()
