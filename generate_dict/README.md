## 带辅助码字典文件生成
若已有基于全拼的字典文件，可将其转换为双拼双形的字典文件。
先安装 Python 依赖 OpenCC：
```shell
pip3 install opencc
```
使用时，需先将待转换的全拼字典文件（默认为 `luna_pinyin.dict.yaml`）放到当前目录下。
例如，若希望将雾凇拼音所提供的 [ext.dict.yaml](https://hub.nuaa.cf/iDvel/rime-ice/blob/main/cn_dicts/ext.dict.yaml) 字典文件转换为 小鹤双拼+自然快手双形 的字典，可将该文件下载到当前目录下，并运行命令
```shell
python3 gen_dict_with_shape.py -i ext.dict.yaml -x zrmfast
```
稍等片刻，生成结果会保存到同一目录下的 `flypy_zrmfast.dict.yaml` 文件中。可以根据自己的需要重命名这一文件。
可使用如下命令查看可选的命令行参数列表：
```shell
python3 gen_dict_with_shape.py -h
```
PS：针对小鹤原版辅助码，还有另一位用户也实现了一份 [Python 转换程序](https://github.com/boomker/rime-flypy-xhfast/blob/15664c597644bd41410ec4595cece88a6452a1bf/scripts/flypy_dict_generator_new.py)，需要配合相应的 [小鹤原版辅助码文件](https://github.com/boomker/rime-flypy-xhfast/blob/15664c597644bd41410ec4595cece88a6452a1bf/scripts/xhxm_map.py)。
