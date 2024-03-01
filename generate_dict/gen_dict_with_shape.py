#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
r"""
Convert quanpin dictionary files to pinyin+shape for Rime input method.
"""

import csv
import re
import argparse
import opencc

opencc_t2s = opencc.OpenCC('t2s.json')


def lunapy2flypy(pinyin: str):
    r""" 全拼拼音转为小鹤双拼码, 如果转自然码等请自行替换双拼映射
    adapted from: https://github.com/boomker/rime-flypy-xhfast/blob/15664c597644bd41410ec4595cece88a6452a1bf/scripts/flypy_dict_generator_new.py
    """
    shengmu_dict = {"zh": "v", "ch": "i", "sh": "u"}
    yunmu_dict = {
        "ou": "z",
        "iao": "n",
        "uang": "l",
        "iang": "l",
        "en": "f",
        "eng": "g",
        "ang": "h",
        "an": "j",
        "ao": "c",
        "ai": "d",
        "ian": "m",
        "in": "b",
        "uo": "o",
        "un": "y",
        "iu": "q",
        "uan": "r",
        "van": "r",
        "iong": "s",
        "ong": "s",
        "ue": "t",
        "ve": "t",
        "ui": "v",
        "ua": "x",
        "ia": "x",
        "ie": "p",
        "uai": "k",
        "ing": "k",
        "ei": "w",
    }
    zero = {
        "a": "aa",
        "an": "an",
        "ai": "ai",
        "ang": "ah",
        "o": "oo",
        "ou": "ou",
        "e": "ee",
        "n": "en",
        "en": "en",
        "eng": "eg",
    }
    if pinyin in zero:
        return zero[pinyin]
    if pinyin[1] == "h" and len(pinyin) > 2:
        shengmu, yunmu = pinyin[:2], pinyin[2:]
        shengmu = shengmu_dict[shengmu]
    else:
        shengmu, yunmu = pinyin[:1], pinyin[1:]
    return shengmu + yunmu_dict.get(yunmu, yunmu)


def get_pinyin_fn(schema: str):
    schema = schema.lower()
    if schema in "quanpin lunapy luna_pinyin none".split():
        def do_nothing(pinyin: str):
            return pinyin
        return do_nothing
    if schema in "flypy xh xhup".split():
        return lunapy2flypy
    if schema in "zrm zrup".split():
        raise NotImplementedError("Pinyin schema 'zrm' not implemented.")


def get_shape_dict(schema: str):
    with open(f"{schema}.txt", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t", quotechar="`"))
    shape_dict = {row[0]: row[1] for row in rows if len(row) >= 2}
    return shape_dict


def rewrite_row(row: list, code_fn: callable):
    if len(row) < 2 or row[0][0] == "#":
        return row
    if len(row) == 2 and row[1][0].isnumeric():  # ['三觭龍', '1']
        return row
    # row == ['三觭龍', 'san ji long'] or ['三觭龍', 'san ji long', '1']
    zh_chars = row[0]
    # eg. '安娜·卡列尼娜' -> '安娜卡列尼娜'
    zh_chars = re.sub("[;·，。；：“”‘’《》（）！？、…—]", "", zh_chars)
    zh_chars = opencc_t2s.convert(zh_chars)  # '三觭龍' -> '三觭龙'
    pinyin_list = row[1].split()  # ['san', 'ji', 'long']
    if len(zh_chars) != len(pinyin_list):  # failure case
        print(row)
        row[0] = "#" + row[0]
        return row
    # ['sj[hh', 'ji[[', 'ls[yp']
    code_list = [code_fn(py, zi) for (py, zi) in zip(pinyin_list, zh_chars)]
    row[1] = " ".join(code_list)  # 'sj[hh ji[[ ls[yp'
    return row


def get_cli_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input_file", "-i", type=str,
                        default="luna_pinyin.dict.yaml",
                        help="input dictionary file")
    parser.add_argument("--output_file", "-o", type=str, default="",
                        help="output dictionary file")
    parser.add_argument("--pinyin", "-p", type=str, default="flypy",
                        choices=["flypy", "quanpin", "zrm"],
                        help="pinyin schema")
    parser.add_argument("--shape", "-x", type=str, default="zrmfast",
                        choices=["flypy", "zrmfast"], help="shape schema")
    parser.add_argument("--delimiter", "-d", type=str, default="[",
                        help="delimiter to seperate pinyin and shape")
    args = parser.parse_args()
    return args


def main():
    args = get_cli_args()
    pinyin_fn = get_pinyin_fn(args.pinyin)
    shape_dict = get_shape_dict(args.shape)
    delim = args.delimiter
    with open(args.input_file, newline="") as f:
        rows = list(csv.reader(f, delimiter="\t", quotechar="`"))

    def code_fn(pinyin, hanzi):
        if hanzi == "干" and pinyin == "qian":
            hanzi = "乾"
        return pinyin_fn(pinyin) + delim + shape_dict.get(hanzi, delim)
    out_rows = [rewrite_row(row, code_fn) for row in rows]

    output_file = args.output_file
    if output_file == "":
        _, input_postfix = args.input_file.split(".", maxsplit=1)
        output_file = f"{args.pinyin}_{args.shape}.{input_postfix}"
    with open(output_file, "w", newline="") as f:
        my_tsv = csv.writer(f, delimiter="\t",
                            quotechar="`", lineterminator="\n")
        my_tsv.writerows(out_rows)


if __name__ == "__main__":
    main()
