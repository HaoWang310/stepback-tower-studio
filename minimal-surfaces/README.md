# 极小曲面目录 · Minimal Surface Catalogue

> **独立存储。** 这个文件夹专门存放极小曲面目录的全部资料，和本仓库的 STEPBACK 工作室互不引用、互不影响。
>
> **在线浏览**：https://haowang310.github.io/stepback-tower-studio/minimal-surfaces/
> （GitHub Pages 发布整个仓库，所以这个文件夹的 `index.html` 就是目录 app 的网址。导出 STL 需在 claude.ai 版本中使用。）

## 分类方式

- **一级：周期性**
  - B · 单周期（沿一个方向重复）
  - C · 双周期（沿一个平面重复）
  - D · 三周期 TPMS（沿空间三个方向重复）
- **二级：端的类型**（与原作者 M. Weber 的单周期分类一致）：环状端（鞍塔翼）、螺旋面端、平面端、悬链面端、周期 Enneper 端、混合端
- **三周期类（D）的二级**：按晶胞形状（立方 / 四方 / 六方棱柱 …）
- **双周期类（C）的二级**：按上下端是否平行（非平行端 / 平行端），并注明商曲面的亏格
- **建筑用途标签**：屋面 · 立面 · 结构 · 景观 · 可打印（方便从设计角度筛选，不改变数学分类）

## 文字清单

| 编号 | 名称 | 分类 | 端的类型 | 生成方法 | 来源 | 用途标签 | 收录日期 |
|---|---|---|---|---|---|---|---|
| 001 | Scherk–Enneper（带周期 Enneper 端的 Scherk 鞍塔） | B · 单周期 | 周期 Enneper 端 | Weierstrass 数值积分 | M. Weber · Minimal Surface Repository（Mathematica notebook） | 立面 · 结构 · 可打印 | 2026-11-25 |
| 002 | Helicoidal Karcher–Scherk（螺旋运动不变的 Karcher–Scherk 鞍塔） | B · 单周期 | 螺旋面端 | Weierstrass 数值积分 + 周期条件求解 | H. Karcher 1988 · M. Weber（Mathematica notebook） | 屋面 · 结构 · 可打印 | 2026-11-25 |
| 003 | Schoen T'–R'（中心体 + 六条侧向隧道） | D · 三周期 | 六方棱柱晶胞 | Surface Evolver 数值求解（Plateau 问题 + 伴随曲面） | A. Schoen · K. Brakke（TRadj.fe） | 结构 · 可打印 | 2026-11-25 |
| 004 | Schoen Manta（亏格 19 的蝠鲼面） | D · 三周期 | 立方晶胞 | Surface Evolver 数值求解（自由边 Plateau 问题 + 伴随曲面） | A. Schoen · K. Brakke（mantaadj.fe） | 结构 · 立面 · 可打印 | 2026-11-25 |
| 005 | Scherk 双周期曲面（Scherk 第一曲面） | C · 双周期 | 非平行端 · 亏格 0 | Weierstrass 闭式解 | H. F. Scherk · M. Weber（Doubly Scherk (g=0).nb） | 立面 · 结构 · 可打印 | 2026-11-25 |
| 006 | Karcher–Meeks–Rosenberg（KMR-1，a=0.1） | C · 双周期 | 平行端 · 亏格 1 | Weierstrass 数值积分 | H. Karcher · Meeks–Rosenberg · M. Weber（KMR-1/2/3.nb） | 结构 · 立面 · 可打印 | 2026-11-25 |

## 文件结构

```
minimal-surfaces/
├── README.md                     本文件：分类方式 + 文字清单
├── index.html                    目录 app（卡片 / 清单视图，点开即三维预览、调参、导出 STL）
├── 001-scherk-enneper/           B · 单周期 · 周期 Enneper 端
│   ├── README.md                 公式、参数、验证记录
│   ├── preview.jpg               app 渲染的预览图
│   ├── reference/                你给的原图截图（原图-1、原图-2、原图-3、名称）
│   └── source/                   原作者 Mathematica 文件（.nb / .cdf）
├── 002-helicoidal-karcher-scherk/ B · 单周期 · 螺旋面端
│   ├── README.md
│   ├── preview.jpg
│   ├── reference/                你给的原图截图（原图-16端、原图-4端、原图-6端）
│   └── source/
│       ├── *.nb / *.cdf          原作者 Mathematica 文件
│       └── povray/k{k}-a{a}/     原作 POV-Ray 场景、网格、渲染图（11 组）
├── 003-schoen-tr/                D · 三周期 · 六方棱柱晶胞
│   ├── reference/原图.png
│   ├── source/TRadj.fe           K. Brakke 的 Surface Evolver 脚本
│   └── solver/                   Python 复现（没有公式，离线数值求解）
├── 004-schoen-manta/             D · 三周期 · 立方晶胞
│   ├── reference/原图.png
│   ├── source/mantaadj-网页翻译版.fe.txt   K. Brakke 的 Evolver 脚本（网页翻译版）
│   └── solver/                   Python 复现 + 曲面片数据
├── 005-scherk-doubly-periodic/   C · 双周期 · 非平行端
│   ├── reference/原图-scherk2a.png
│   ├── source/                   原 notebook + povray/
│   └── solver/                   Python 复现 + 按原相机重渲染比对
└── 006-karcher-meeks-rosenberg/  C · 双周期 · 平行端
    ├── reference/                选定原图（KMR-1 a=0.1）+ 12 组原图对照
    ├── source/                   KMR-1/2/3.nb + povray/KMR-1、KMR-2、KMR-3
    └── solver/                   Python 复现 + 逐点比对
```

每个曲面文件夹都是同一结构：`reference/`（你发来的图）、`source/`（原作者文件）、`README.md`（公式与验证）、`preview.jpg`。

> 注意：本仓库是公开的。`source/` 和 `reference/` 里是原作者（M. Weber、K. Brakke 等）的文件和渲染图，各 README 已注明出处。

本地预览：直接用浏览器打开 `index.html`（需要联网加载 three.js）。

## 收录一个新曲面

1. 新建 `NNN-名称/` 文件夹：原图放 `reference/`，原作者文件放 `source/`，再写 `README.md`（公式、参数、来源）
2. 在上面的文字清单里加一行
3. 在 `index.html` 的 `SURFACES` 列表里加一条（有公式的再加三维生成器）
