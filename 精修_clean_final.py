#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

BASE_PATH = "/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/src/volume3"

def read_chapter(n):
    with open(os.path.join(BASE_PATH, f"ch{n}.md"), 'r', encoding='utf-8') as f:
        return f.read()

def write_chapter(n, content):
    with open(os.path.join(BASE_PATH, f"ch{n}.md"), 'w', encoding='utf-8') as f:
        f.write(content)

def fix_chapter339(content):
    """修复ch339: 删除本章完前的多余---"""
    lines = content.split('\n')
    new_lines = []
    
    # 找到**本章完**的位置
    end_idx = -1
    for i, line in enumerate(lines):
        if '**本章完**' in line:
            end_idx = i
            break
    
    if end_idx < 0:
        return content
    
    # 保留end_idx之前的内容（直到上一个有意义的行）
    # 找到end_idx之前最后一个非空非---的行
    last_meaningful = end_idx - 1
    while last_meaningful >= 0:
        stripped = lines[last_meaningful].strip()
        if stripped and stripped != '---':
            break
        last_meaningful -= 1
    
    # 复制到last_meaningful
    new_lines = lines[:last_meaningful + 1]
    
    # 添加一个---分隔
    new_lines.append('---')
    
    # 添加**本章完**
    new_lines.append('**本章完**')
    
    return '\n'.join(new_lines)

def main():
    for n in [336, 339, 358]:
        content = read_chapter(n)
        before = len(content.replace('\n', ''))
        
        if n == 339:
            content = fix_chapter339(content)
        
        # 通用清理
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        after = len(content.replace('\n', ''))
        if before != after:
            print(f"ch{n}: {before} -> {after} ({after - before:+d})")
            write_chapter(n, content)
        else:
            print(f"ch{n}: {before} (无变化)")

if __name__ == "__main__":
    main()
