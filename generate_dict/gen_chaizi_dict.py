#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Generate chaizi dictionary."""
# Based on http://gerry.lamost.org/blog/?p=296003
# By Gerry @ 2019.12.28
# Usage: make chaizi dictionary for rime
# base on :
# https://github.com/mozillazg/python-pinyin
# https://github.com/kfcd/chaizi

import re
import argparse
from typing import List, Callable
from pypinyin import lazy_pinyin
from gen_dict_with_shape import get_pinyin_fn

yaml_head = """# Rime dictionary
# encoding: utf-8
## Based on http://gerry.lamost.org/blog/?p=296003
## 拆字模式字典，拆分组件使用小鹤双拼输入
---
name: <TOFILL:name>
version: "2019.12.28"
sort: by_weight
use_preset_vocabulary: true  # 導入八股文字頻
max_phrase_length: 1         # 不生成詞彙
...

"""

pianpang_dict = {
    "丶": "点",
    "乀": "捺",
    "㇆": "折",
    "㇉": "折",
    "𠃑": "折",
    "乛": "折",
    "𠃋": "折",
    "亅": "钩",
    "龴": "丝",
    "阝": "耳",
    "卩": "耳",
    "辶": "之",
    "⺆": "冂",
    "冖": "盖",
    "宀": "盖",
    "罒": "四",
    "龹": "春",
    "龷": "共",
    "": "衣",
}


def rewrite_chaizi(chaizi: str) -> str:
    # "阝东" -> ["耳", "东"] -> "耳东"
    return "".join([pianpang_dict.get(hanzi, hanzi) for hanzi in chaizi])


def process_row(line: str,
                delimiter: str,
                pinyin_fn: Callable[[str], str]) -> List[str]:
    data = line.strip().split("\t")
    hanzi = data[0].strip()
    if hanzi.startswith("#") or len(data) < 2:
        return line

    # ("阝 东",) -> ["阝东"]
    chaizi_list = [chaizi.replace(" ", "") for chaizi in data[1:]]
    # ["阝东"] -> ["阝东", "耳东"]
    chaizi_list.extend([rewrite_chaizi(chaizi) for chaizi in chaizi_list])
    pinyin_set = set()
    for chaizi in chaizi_list:
        pinyin_list = lazy_pinyin(chaizi)  # "阝东" -> ["fu", "dong"]
        if re.match('[A-Za-z]+$', "".join(pinyin_list)) is None:
            print(hanzi + "\t" + "|".join(pinyin_list))
            continue
        # ["fu", "dong"] -> ["fu", "ds"]
        pinyin_list = [pinyin_fn(pinyin) for pinyin in pinyin_list]
        # ["fu", "ds"] -> "fu!ds!"
        pinyin_set.add(delimiter.join(pinyin_list) + delimiter)

    return [f"{hanzi}\t{pinyin}\n" for pinyin in pinyin_set]


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input_file", "-i", type=str, default="chaizi.txt",
                        choices=["chaizi.txt", "chaizi_tr.txt"],
                        help="input dictionary file in the *.txt format")
    parser.add_argument("--output_file", "-o", type=str, default="",
                        help="output dictionary file")
    parser.add_argument("--pinyin", "-p", type=str, default="flypy",
                        choices=["flypy", "quanpin", "zrm"],
                        help="pinyin schema")
    parser.add_argument("--delimiter", "-d", type=str, default="!",
                        help="delimiter to seperate chaizi results")
    args = parser.parse_args()
    return args


def main() -> None:
    args = get_cli_args()
    pinyin_fn = get_pinyin_fn(args.pinyin)

    out_rows = []
    for line in open(args.input_file, encoding='UTF-8').readlines():
        out_rows.extend(process_row(line, args.delimiter, pinyin_fn))

    output_file = args.output_file
    if output_file == "":
        input_prefix, _ = args.input_file.split(".", maxsplit=1)
        output_file = f"{input_prefix}_{args.pinyin}"
    with open(output_file + ".dict.yaml", "w", encoding='UTF-8') as dfile:
        dfile.write(yaml_head.replace("<TOFILL:name>", output_file))
        dfile.writelines(out_rows)


if __name__ == "__main__":
    main()
