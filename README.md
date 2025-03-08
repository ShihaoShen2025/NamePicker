# NamePicker
> 一款非常 ~~简陋~~ 简洁的点名软件

## TODO
1. [x] 基础的点名功能
2. [x] 人性化（大嘘）的配置修改界面
3. [x] 从外部读取名单
4. [x] 特殊点名规则
5. [ ] 概率内定
6. [ ] 悬浮窗（点击展开主界面）

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
Q:配置界面和主界面风格不同

A:作者目前没找到怎么修，但不影响使用

Q:杀毒软件认为这是病毒软件

A:将该软件添加至杀毒软件的白名单/信任区中，本软件保证不含病毒，您可以亲自审查代码，如果还是觉得不放心可以不使用

Q:打开好慢

A:Python的运行效率不高，慢属于正常现象