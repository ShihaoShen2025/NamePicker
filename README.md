<div align="center">
<img src="assets\NamePicker.png" alt="icon" width="18%">
<h1>NamePicker</h1>
<h3>一款简洁的点名软件</h3>
</div>


## 功能清单/大饼
1. [x] 基础的点名功能
2. [x] 人性化（大嘘）的配置修改界面
3. [x] 从外部读取名单
4. [x] 特殊点名规则
5. [ ] 概率内定（疑似过于缺德了，短时间内不会加）
6. [ ] 悬浮窗（点击展开主界面）
7. [ ] 软件内更新
8. [x] 支持非二元性别
9. [x] 同时抽选多个
10. [ ] 播报抽选结果
11. [x] 与ClassIsland/Class Widgets联动（联动插件均已上架对应软件的插件商城）（目前已知ClassIsland在进行多次抽选时100%崩溃（真不是我菜在开发环境都没这破事），Class Widgets不受影响）
12. [ ] 手机遥控抽选
13. [ ] 改用PyQt（工作量约等于重写，大概率会拖到中考后，小概率直接忽视）

## 支持的平台
1. [x] Windows 10+
2. [x] Linux（国产化系统）
3. [ ] Windows 7-8.1 （尚未测试）
4. [ ] MacOS（理论上可以，但是~~作者是懒狗~~作者没有果子设备可供测试，Action也没有MacOS构建）
## 运行指南

### 运行指南（成品程序）
1. Windows：将Release中下载的压缩包解压到某个空文件夹中，随后运行main.exe
2. Linux（国产化系统）：将Release中下载的压缩包解压到某个空文件夹中，双击运行main.bin（如果不能执行请检查是否为其提供了运行权限）

### 运行指南（源码）

0. （可选）创建虚拟环境
1. 安装依赖项
`pip install -r requirements.txt`
2. 运行main.py

### 打包可执行文件指南（使用打包脚本）

1. 使用venv创建虚拟环境（如何创建请自行百度，并保证虚拟环境目录为./venv）
2. 安装依赖项
`pip install -r requirements.txt`
3. 运行build.bat

### 打包可执行文件指南（不使用打包脚本）

0. （可选）创建虚拟环境
1. 安装依赖项
`pip install -r requirements.txt`
2. 在虚拟环境中运行
`nuitka --standalone --onefile --enable-plugin=tk-inter --remove-output --windows-disable-console  main.py`

## FAQ
### Q:怎么配置名单

A:修改names.csv，第一行别改，第二行开始按照"学生名字,性别（0=男，1=女，2=非二元，不符合标准的性别代号理论上会被忽视）,学号"来填写，**务必使用英文符号**

就像这样：
```
name,sex,no
example,0,1
caixukun,2,2
sunxiaochuan,1,3
```
PS:不建议设置重复的学号和姓名，以免在使用时带来困扰

图形化的编辑界面见[NP-NameEditor](https://github.com/NamePickerOrg/NP-NameEditor)

当然，也没人拦着你用Excel或WPS Office编辑，但是请记住 _**务必使用UTF-8编码保存**_ ，否则会导致无法读取名单

### Q:杀毒软件认为这是病毒软件

A:将该软件添加至杀毒软件的白名单/信任区中，本软件保证不含病毒，您可以亲自审查代码，如果还是觉得不放心可以不使用

### Q:打开好慢

A:Python的运行效率不高，慢属于正常现象