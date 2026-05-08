#!/usr/bin/env python3
"""Chinese number converter - attempt 7."""

def chinese_to_arabic(num_str):
    chinese_map = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    }

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

# Test cases
tests = [
    ("零", 0),
    ("一", 1),
    ("十", 10),
    ("十一", 11),
    ("十二", 12),
    ("二十", 20),
    ("二十一", 21),
    ("一百", 100),
    ("一百零一", 101),
    ("一百一十", 110),
    ("一百一十一", 111),
    ("一百二十", 120),
    ("一百二十一", 121),
]

for chinese, expected in tests:
    result = chinese_to_arabic(chinese)
    status = "✓" if result == expected else "✗"
    print(f"{status} {chinese} → {result} (expected {expected})")
