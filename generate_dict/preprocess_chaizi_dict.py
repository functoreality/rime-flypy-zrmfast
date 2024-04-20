#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
r"""
Generate chaizi.txt, chaizi_tr.txt based on the dictionaries provided by
https://github.com/kfcd/chaizi. If users found the two files provided in this
repository already fit their need, it is not necessary to run this script.
"""
import os
import argparse
import opencc

opencc_t2s = opencc.OpenCC('t2s.json')
opencc_s2t = opencc.OpenCC('s2t.json')


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo_path", "-p", type=str, default="chaizi",
                        help="path of the repository cloned from "
                        "https://github.com/kfcd/chaizi.")
    args = parser.parse_args()
    return args


def main():
    args = get_cli_args()
    if not os.path.exists(args.repo_path):
        raise FileNotFoundError(
            f"I cannot find the path '{args.repo_path}'. Please first clone "
            "the repository from https://github.com/kfcd/chaizi, and then "
            "run this script as\n\n\t"
            "python3 chaizi-dict-reform.py -p path/to/your/cloned/repo")
    jt_lines = open(os.path.join(args.repo_path, "chaizi-jt.txt"),
                    encoding='UTF-8').readlines()
    ft_lines = open(os.path.join(args.repo_path, "chaizi-ft.txt"),
                    encoding='UTF-8').readlines()
    ft_lines_new = []

    for i in range(len(jt_lines)):
        jt_lines[i] = jt_lines[i].replace("\t\t", "\t")
        if jt_lines[i][0] == "□":
            jt_lines[i] = opencc_t2s.convert(ft_lines[i][0]) + jt_lines[i][1:]
            ft_lines_new.append(ft_lines[i])
        elif ft_lines[i][0] == "□":
            ft_lines_new.append(opencc_s2t.convert(
                jt_lines[i][0]) + ft_lines[i][1:])
        elif jt_lines[i][0] != ft_lines[i][0]:
            ft_lines_new.append(ft_lines[i])
        elif ft_lines[i].startswith(jt_lines[i][:-1]):
            jt_lines[i] = ft_lines[i]
        elif not jt_lines[i].startswith(ft_lines[i][:-1]):
            ft_lines_new.append(ft_lines[i])
            print(jt_lines[i], ft_lines[i])

    with open("chaizi.txt", "w", encoding='UTF-8') as f:
        f.writelines(jt_lines)
    with open("chaizi_tr.txt", "w", encoding='UTF-8') as f:
        f.writelines(ft_lines_new)


if __name__ == "__main__":
    main()
