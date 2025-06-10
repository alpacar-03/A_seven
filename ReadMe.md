# A7-基于开源AI大模型的教学实训智能体软件

## 项目地址
https://github.com/yekater9420/A7---Teaching-Training-Intelligent-Agent-Software-Based-on-Open-Source-AI-Large-Model

## 项目简介
自行准备本地知识库资料(如本专业相关资料内容)作为大模型本地知识库的输入

教师侧：备课与设计：

       根据所提供的本地课程大纲、课程知识库文档等自动设计教学内容，包括知识讲解、实训练习与指导、时间分布等。

       · 考核内容生成：

      根据教学内容自动生成考核题目及参考答案，考核题目种类可多样化，根据学科设计，如计算机类可设计相关编程题和答案

       · 学情数据分析：

       对学生提交的答案进行自动化检测，提供错误定位与修正建议。对学生整体数据进行分析，总结知识掌握情况与教学建议。

学生侧：

       · 在线学习助手：

       对学生的提出的问题，结合教学内容进行解答;

       · 实时练习评测助手：

       根据学生历史练习情况，以及学生的练习要求，生成随练题目，并对练习纠错。

管理侧：

       用户管理：管理员/教师/学生等用户的基本管理

       课件资源管理：按学科列表教师备课产生的课件、练习等资源，可以导出。

       大屏概览：

       · 教师使用次数统计/活跃板块(当日/本周)

       · 学生使用次数统计/活跃板块(当日/本周)

       · 教学效率指数(备课与修正耗时、课后练习设计与修正耗时、课程优化方向(如：某学科通过率持续偏低)

       · 学生学习效果(平均正确率趋势、知识点掌握情况，高频错误知识点等)

## 实现目标
- 实现目标：
  本赛题旨在开发一个基于开源大模型的教学实训智能体软件，帮助教师生成课前备课设计、课后检测问答，提升效率与效果，提供学生全时在线练习与指导，实现教学相长。

## 功能特性
- 功能 1
  教师端
- 功能 2
  学生端
- 功能 3
  管理端

## 安装与运行
### 环境要求
- 操作系统：如 Windows 11 x64
- 依赖：Python 3.11 up

### 安装步骤
1. 下载项目源代码：
    ```bash
    downloade <URL> teaching_assistant_[version].zip
    ```
2. 解压：
    ```bash
    unzip
    ```
3. conda创建环境：
    ```bash
    conda activate
    conda create -n A7_Problem python=3.11 -y
    conda activate A7_Problem
    ```
4. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

### 安装步骤
微调大模型配置文件.jsonl

## 使用说明
It is easy to run the project by simply typing the following command in the terminal:

```
Python main_[version].py
```

## 微调数据集创建开源项目
https://github.com/ConardLi/easy-dataset

![https://github.com/ConardLi/easy-dataset](Image\Easy_DataSet.png)

## 文件结构
项目的目录结构：
```
/项目根目录
├── Config/              # 配置文件
├── Dataset/             # 微调数据集
├── Docs/                # 说明文档
├── GUI/                 # 存放GUI界面文件
├── example/             # 示例
├── Image/               # 存放图片
├── Large_Model/         # 大模型API接口
├── Pass_version/        # 过去版本
├── Results/             # 结果存放文件夹
├── utils/               # 附属工具包
├── ReadMe.md            # 项目说明
└── requirements.txt     # 环境需求
```
