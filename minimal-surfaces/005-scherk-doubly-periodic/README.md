# 005 · Scherk 双周期曲面（Scherk's first surface）

- **分类**：C · 双周期 · 非平行端 · 亏格 0
- **用途标签**：立面 · 结构 · 可打印
- **来源**：H. F. Scherk 1835；M. Weber，Minimal Surface Repository（`Doubly Scherk (g=0).nb` 与 PoVRay 场景）
- **隐式方程**：e^z cos y = cos x（原作 PoVRay 场景采用的形式）

## Weierstrass 数据（来自原 notebook）

- G = √((1+z)/(z−1))，dh = dz/z，ρ = 1
- 原 notebook 直接给出了闭式原函数：
  f(z) = ( −2 Re arctan(√(z−1)/√(z+1)) , −2 Im arcsinh(√(z−1)/√2) , Re log z )

## 构造

1. 在上半圆盘的极坐标网格上取点，r ∈ [x_min, 1)，θ ∈ (0, π)。
2. 拼接，顺序与 notebook 相同：
   - 单位圆的像是一条直线，绕它旋转 180°；
   - 关于平面 x=0 镜像；
   - 关于平面 y=0 镜像；
   - 沿 x、y 各平移 2π。
3. 原作 PoVRay 网格是另一种取法：交换 x 和 y，再截取窗口 |x|,|y| ≤ 1.5π、|z| ≤ 2。app 的"原图"预设和它一致。

## 验证

- **公式**：复现网格满足 e^z cos x = cos y，残差约 1e-15，交换 x、y 后就是原作的形式。
- **网格**：app（JS）生成的网格与原作 `dummy.pov` 的 252,204 个顶点对比：
  - 包围盒完全一致；
  - 点到面距离平均 3.6e-5（归一化单位）。
- **渲染**：用原 .pov 的相机（rotate <90,45,0>、<-30,0,0>，scal 0.9）重渲染，剪影与 `scherk2a.png` 的重合度 0.968，两侧颜色一致率 0.95。
  - 原图需要 translate <0,0.2,0> 才对得上，但 .pov 文件里写的是 0.1。估计渲染原图时用的值和保存的文件不同，app 按原图取 0.2。

## 文件

- `reference/原图-scherk2a.png`：原作渲染
- `source/Doubly Scherk (g=0).nb`：原 notebook
- `source/povray/`：原 PoVRay 场景和网格
- `solver/scherk.py`：Python 复现
- `solver/scherk_pov.py`、`solver/povcam.py`：按原相机重渲染并比对
