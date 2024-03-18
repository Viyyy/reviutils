<h1 align="center">reviutils</h1>
<p align="center">一个常用的Python库</p>
<p align="center">
<a href="./README.md">简体中文</a>｜
<a href="./README_EN.md">English</a> 
</p>

<div align='center'>
<a href="https://github.com/Viyyy/reviutils"><img src="https://img.shields.io/badge/github-reviutils-red?logo=github"></a>
  
<a href="https://utilsdemo.reviy.top/docs"><img src="https://img.shields.io/badge/fastapi-demo-green?logo=fastapi"></a>
  
<a href="https://pypi.org/project/reviutils/"><img src="https://img.shields.io/pypi/v/reviutils.svg"></a>
  
<a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-yellow"></a>
</div>

## 功能

### reviutils.common

  这个模块提供了一系列常用的方法，可以在各种应用中使用。这个包中的方法旨在简化常见的编程任务，增强代码的可重用性。

### reviutils.noisepollution

- #### reviutils.noisepollution.evaluation

  根据《城市地区环境噪声监测技术规范-城市声环境总体监测》（HJ640-2012）中的规定，提供城市区域环境噪声以及道路交通噪声的强度评估和分类。
- #### reviutils.noisepollution.funcarea

  根据声环境质量标准(GB 3096-2008)，提供声功能区相关信息。
- #### reviutils.noisepollution.hourhelper

  小时数据处理：可对小时数据进行处理，区分白天和夜晚时段。
- #### reviutils.noisepollution.splhelper

  声压级（SPL）计算：提供从数据计算声压级的功能。

### reviutils.audio

> 需要额外的安装

- #### reviutils.audio.clipper

  提供裁剪或填充音频文件的功能。您可以使用此功能来修剪音频片段或在音频的开头或结尾添加静音。
- #### reviutils.audio.reader

  提供读取音频文件的能力。此功能允许您将音频文件加载到应用程序中进行进一步处理或分析。

## 安装

#### 常规模块安装

```
pip install --upgrade pip
pip install reviutils
```

#### 额外安装

```
pip install reviutils[audio]
```

### 许可证

<div>
<a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-yellow"></a>
</div>
