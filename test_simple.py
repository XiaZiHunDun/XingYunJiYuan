#!/usr/bin/env python3
"""Debug Chinese number conversion."""

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
            result = result * 10 + (temp if temp > 0 else 1)
            temp = 0
        elif char == '百':
            result = (result + temp) * 100
            temp = 0
        else:
            temp = temp * 10 + chinese_map.get(char, 0)

    return result + temp

print("Testing 十一:", chinese_to_arabic("十一"))
print("Testing 二十:", chinese_to_arabic("二十"))
print("Testing 一百零一:", chinese_to_arabic("一百零一"))
