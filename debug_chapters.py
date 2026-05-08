#!/usr/bin/env python3
"""Debug: Check what chapters exist in volume1_full.md."""

input_file = "/home/ailearn/projects/AI-Incursion/domains/IP创作/projects/XingYunJiYuan/volume1_full.md"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re

print("Looking for chapter headers...")
for i, line in enumerate(lines[:200]):
    if re.match(r'^# 第[零一二三四五六七八九十百]+章', line):
        print(f"Line {i+1}: {line.strip()}")
        match = re.search(r'^# 第([零一二三四五六七八九十百]+)章', line)
        if match:
            chinese_num = match.group(1)
            print(f"  → Extracted: {chinese_num}")

# Now find all chapter headers and report missing ones
print("\n\nAll chapter numbers in file:")
all_nums = []
for line in lines:
    match = re.search(r'^# 第([零一二三四五六七八九十百]+)章', line)
    if match:
        chinese_num = match.group(1)
        # Simple conversion
        result = 0
        temp = 0
        for char in chinese_num:
            if char == '十':
                result = result * 10 + (temp if temp > 0 else 1) * 10
                temp = 0
            elif char == '百':
                result = (result + temp) * 100
                temp = 0
            elif char.isdigit():
                temp = int(char)
        all_nums.append(result + temp)

print(f"Found {len(all_nums)} chapters")
print(f"Numbers: {all_nums}")

# Find missing chapters
missing = []
for i in range(1, 121):
    if i not in all_nums:
        missing.append(i)

print(f"\nMissing chapters (1-120): {missing}")