def pinyin_to_zrm(pinyin: list[str]):
    def to_zrm(pinyin: str):
        shengmu_dict = {
            'zh': 'v',
            'ch': 'i',
            'sh': 'u'
        }
        yunmu_dict = {
            'ou': 'b',
            'iao': 'c',
            'uang': 'd',
            'iang': 'd',
            'en': 'f',
            'eng': 'g',
            'ang': 'h',
            'an': 'j',
            'ao': 'k',
            'ai': 'l',
            'ian': 'm',
            'in': 'n',
            'uo': 'o',
            'un': 'p',
            'iu': 'q',
            'uan': 'r',
            'er': 'r',
            'iong': 's',
            'ong': 's',
            'ue': 't',
            'ui': 'v',
            'ua': 'w',
            'ia': 'w',
            'ie': 'x',
            'uai': 'y',
            'ing': 'y',
            'ei': 'z'
        }
        zero = {
            'a': 'aa',
            'an': 'an',
            'ang': 'ah',
            'o': 'oo',
            'ou': 'ou',
            'e': 'ee',
            'en': 'en',
            'eng': 'eg'
        }
        if pinyin in zero.keys():
            return zero[pinyin]
        else:
            if pinyin[1] == 'h':
                shengmu = shengmu_dict[pinyin[:2]]
                yunmu = yunmu_dict[pinyin[2:]] if pinyin[2:] in yunmu_dict.keys() else pinyin[2:]
                return shengmu + yunmu
            else:
                shengmu = pinyin[:1]
                yunmu = yunmu_dict[pinyin[1:]] if pinyin[1:] in yunmu_dict.keys() else pinyin[1:]
                return shengmu + yunmu

    print("pinyin: ", pinyin)
    return [to_zrm(x) for x in pinyin]


is_simplified = False


def chai():
    from pypinyin import lazy_pinyin
    if is_simplified:
        lines = open("chaizi/chaizi-jt.txt").readlines()  # 载入简体拆字字典
        dfile = open("chaizi_zrm.yaml", "w")  # 打开待写入字库文件
    else:
        lines = open("chaizi/chaizi-ft.txt").readlines()  # 载入简体拆字字典
        dfile = open("chaizi_zrm.tr.yaml", "w")  # 打开待写入字库文件

    dfile.write(
        """
# Rime dictionary
# encoding: utf-8
## Based on http://gerry.lamost.org/blog/?p=296003
## 拆字模式字典，拆分组件使用自然码双拼输入
---
name: zrm_chaizi
version: "2023.1.7"
sort: by_weight
use_preset_vocabulary: true  # 導入八股文字頻
max_phrase_length: 1         # 不生成詞彙
import_tables:
  - chaizi_zrm.tr ## 注释掉后：停用繁体部分词典
...
        """ if is_simplified else (
            """
# Rime dictionary
# encoding: utf-8
## Based on http://gerry.lamost.org/blog/?p=296003
## 拆字繁体模式字典，拆分组件使用自然码双拼输入
---
name: zrm_chaizi
version: "2023.1.7"
sort: by_weight
use_preset_vocabulary: true  # 導入八股文字頻
max_phrase_length: 1         # 不生成詞彙
...
            """
        )
    )
    dfile.write("\n")
    for line in lines:
        data = line.strip().split("\t")
        for i in range(1, len(data)):
            # 笔画转拼音，以字母u开头
            pinyin = lazy_pinyin(data[i].replace(" ", ""))
            if all([x.isascii() for x in pinyin]):
                print("pinyin_raw: ", pinyin)
                zrm = pinyin_to_zrm(pinyin)
                print("zrm", zrm)
                py = "".join(zrm)
                # if py.isalpha():
                # 生成rime词库要求格式，默认词频为1
                item = data[0].strip() + "\t" + py + "\n"
                dfile.write(item)
            else:
                print(data[i])
    dfile.close()


if __name__ == '__main__':
    is_simplified = False
    chai()
    is_simplified = True
    chai()
