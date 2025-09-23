# 邦多利当期新卡期望抽数模拟（PyQT图形版）

## 介绍

本程序为邦多利（BanG Dream!）玩家提供新卡池抽卡期望模拟。通过多线程高效模拟，帮助玩家预测抽到心仪新卡所需的平均抽卡次数，辅助理性规划资源，提升游戏体验。

![ref](ref_image/ref.png)

本项目基于 [C++程序](https://gitee.com/handsome-druid/bangdream-gacha)（由 handsome-Druid 开发）进行图形界面化和功能扩展。使用 numba 将关键数值循环 JIT 编译为本机代码，通常能把大规模蒙特卡洛模拟加速约 20 倍；现在可以轻松计算1000万次以上的模拟。原项目为控制台版本，欢迎参考和对比。

## 安装教程

- 前往 [发行版页面](https://github.com/handsome-Druid/BanGDream-Gacha-pynb/releases) 下载最新版，解压后直接运行 `gacha_release.exe
`。
- 目前仅提供 Windows 发行版。
- Linux 用户推荐使用控制台原版 `bangdreamgacha_numba.py`，可通过仓库内的 `environment.yml` 快速创建运行环境并启动程序：

	1. 创建并激活 conda 环境（基于 `environment.yml`）：

```bash
conda env create -f environment.yml
conda activate gacha-env
```

	2. 运行控制台程序：

```bash
python bangdreamgacha_numba.py
```

	说明：`environment.yml` 已包含 `python=3.9`、`numpy`、`numba` 以及通过 `pip` 安装的 `pyqt5-tools`（仅在需要 GUI/Designer 时使用）。如不使用 conda，也可手动用 `pip install numpy numba` 安装依赖。

## 使用说明

1. 输入当期5星新卡的总数。
2. 输入想要的当期5星卡数量（可为0）。
3. 输入想要的当期4星卡数量（可为0）。
4. 选择是否为常驻池（是否有50抽保底）。
5. 设置模拟次数（建议100万次以上）。
6. 点击“开始模拟”，等待结果显示。

**示例1**：本期fes池有4张新5星，1张新4星，想抽其中2张5星和1张4星，则5星总数填4，想要5星填2，想要4星填1，不勾选常驻池。

**示例2**：本期普限池有5张新5星，想抽全5张，则5星总数填5，想要5星也填5，4星填0，不勾选常驻池。

## 特别说明

1. 本程序未区分fes池与普限池，因为这两种池子抽中某一张当期5星的概率均为0.5%，与常驻池一致。
2. fes池仅提升了非当期5星/4星的出货率，但对当期4/5星的概率无影响。
3. 需要输入当期5星新卡总数，是因为5星卡会分摊小保底概率。4星卡没有小保底，无需输入4星新卡总数。
4. 常驻池小保底不会出4星，因此常驻池只抽当期4星的期望次数会略高于限定池。

## 开源协议

BSD 3-Clause License

## 仓库地址

[https://github.com/handsome-Druid/BanGDream-Gacha-pynb](https://github.com/handsome-Druid/BanGDream-Gacha-pynb) 

## 致谢

- C++控制台版本：[https://gitee.com/handsome-druid/bangdream-gacha](https://gitee.com/handsome-druid/bangdream-gacha)
- VC++图形版本：[https://github.com/handsome-Druid/BanGDream-Gacha](https://github.com/handsome-Druid/BanGDream-Gacha)
