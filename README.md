# STEPBACK · 多塔生长工作室


## 当前在线版本：STEPBACK STUDIO v4.1（2026-11-01）

- GitHub Pages: https://haowang310.github.io/stepback-tower-studio/
- 在线入口为根目录的 `index.html`，内含完整的 Rhino 三维工作室及模型资源，无需在浏览器中拼接九段 HTML。
- `assets/stepback-v4.1/chunk-00.txt` 至 `chunk-08.txt` 为 v4.1 的完整备份源文件。
- `python3 build_full_index.py` 将九个分块校验并合成为根目录 `index.html`；`.github/workflows/assemble.yml` 在 GitHub 上自动执行相同构建。
- 以下原有 v3.4 说明、`shell.html`、`build.py` 以及 `dist/index.html` 均保留，便于继续维护旧版。


参数化多塔建筑可视化工具，当前版本 **v3.4**。黑底白字中文界面，可直接打开 `index.html` 使用，全部运行依赖内嵌，无需安装。

- 默认双塔，支持 1–3 塔与独立楼层数。
- 层高、板厚、向参考线退台、吸引与逐层独立随机控制。
- 指定楼层整体桥接；连接楼层不受随机变形影响。
- 正方形初始底面，直线／圆滑曲线切换；双击边线增点、双击控制点删点。
- 主视图实时编辑，参考线遮挡处理；可移动、缩放的精确平面编辑器。
- 曲线退台楼板完整闭合平滑；生长动画与 OBJ、参数 JSON、图片导出。

## 修改与构建

编辑 `shell.html`，运行：

```bash
python build.py
node check.cjs
cp dist/index.html index.html
```

`index.html` 用于 GitHub Pages，`dist/index.html` 为相同的完整离线应用。

几何来源保存在 `curves.json`，单位为米；网页使用平面几何计算用于方案探索，不执行 RhinoCommon 或 Grasshopper。第三方代码沿用文件中的许可声明。
