# NamePicker
> 一款简洁的点名软件

## TODO
1. [x] 基础的点名功能
2. [x] 人性化（大嘘）的配置修改界面
3. [x] 从外部读取名单
4. [x] 特殊点名规则
5. [ ] 概率内定
6. [ ] 悬浮窗（点击展开主界面）
7. [ ] 软件内更新
8. [x] 支持非二元性别
9. [ ] 同时抽选多个
10. [ ] 播报抽选结果
11. [x] 与ClassIsland/Class Widgets联动（目前仅实现了Class Widgets联动，见[NamePicker4CW](https://github.com/NamePickerOrg/NamePicker4CW)）
12. [ ] 手机遥控抽选

## 运行指南（成品程序）
运行主程序即可

## 运行指南（源码）

0. （可选）创建虚拟环境
1. 安装依赖项
`pip install -r requirements.txt`
2. 运行main.py

## 打包可执行文件指南（使用打包脚本）

1. 使用venv创建虚拟环境（如何创建请自行百度，并保证虚拟环境目录为./venv）
2. 安装依赖项
`pip install -r requirements.txt`
3. 运行build.bat

## 打包可执行文件指南（不使用打包脚本）

0. （可选）创建虚拟环境
1. 安装依赖项
`pip install -r requirements.txt`
2. 在虚拟环境中运行
`nuitka --standalone --onefile --enable-plugin=tk-inter --remove-output --windows-disable-console  main.py`

## FAQ
Q:怎么配置名单

A:修改names.csv，第一行别改，第二行开始按照"学生名字,性别（0=男，1=女）,学号"来填写

务必使用英文符号，并严格按照标准填写，~~未来可能会推出图形化的编辑界面（这个界面保证不用tkinter搓了，也不会包含到本仓库中，而会单独开另一个仓库）~~

有了兄弟有了，见[NP-NameEditor](https://github.com/NamePickerOrg/NP-NameEditor)

Q:配置界面和主界面风格不同

A:~~作者目前没找到怎么修，但不影响使用~~

目前已经修复（Powered by 某AIGC）

Q:杀毒软件认为这是病毒软件

A:将该软件添加至杀毒软件的白名单/信任区中，本软件保证不含病毒，您可以亲自审查代码，如果还是觉得不放心可以不使用

Q:打开好慢

A:Python的运行效率不高，慢属于正常现象