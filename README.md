# STEPBACK · 多塔生长工作室

Self-contained architectural study app using three real closed NURBS contours and three reference curves sampled from the supplied Rhino file (metres). Browser geometry follows STEPBACK v25.50 concepts; this is not execution of Grasshopper/RhinoCommon, and exact Rhino geometry equivalence is not claimed.

- Independent floor counts, height, thickness, progressive setback, reference attraction and deterministic per-floor variation.
- Fixed connected floors use minimum spanning tree ribbons and real planar union; random seed and variation do not change those floors.
- Interactive 3D, timeline growth, top/front/perspective views, source lines, wireframe, OBJ/config/image export.
- WebGL rendering with automatic Canvas 2D perspective projection fallback using the same computed geometry.
- No runtime network dependencies; open `dist/index.html` directly in a browser.

Build: `python build.py`. Validate geometry and invariants: `node check.cjs`.

Original source geometry is embedded in `curves.json`. Web computations are suitable for design exploration; structural feasibility is not evaluated.


## Climate module (v4.9)
Embedded London–Stansted AP TMYx EPW: 8,760 hourly records at 51.885 N, 0.235 E, elevation 106.1 m. GMT standard time, no DST. Packed fields are dry-bulb temperature, GHI, DNI, DHI, wind direction and wind speed. No missing records in these fields.

Run `python build.py`, `node check.cjs`, and `node climate-check.cjs`. Climate source is in `climate.js`; `weather.json` stores lossless gzip of scaled integers from the supplied fields. Browser requires DecompressionStream.

Solar position uses NOAA fractional-year equations. Direct sunshine is hourly geometric solar visibility. Daily horizontal irradiation includes unobstructed-sky diffuse approximation; not a detailed sky model. Wind uses a heuristic height/shelter correction to the selected hourly station wind, not CFD or certified pedestrian comfort. Only current app slabs obstruct solar rays. No surrounding context buildings are supplied. Roof/terrace and ground samples are discrete and used for early design comparison, not regulatory evaluation.

Climate mode (default, v4.12) determines retreat direction independently of reference curves. Geographic retreat azimuth is rotated into model coordinates by the north-angle control. Reference-driven mode and editable reference curves remain available.

All 8,760 EPW records contribute to 12 x 24 monthly/hourly temperature and radiation averages and 32 seasonal 22.5-degree wind bins. Solar obstruction is evaluated using the 15th day of each month at hourly midpoints and weighted by month length. These are representative-year estimates, not a complete 8,760-ray sun trace. The solar score combines sunshine visibility with radiation gain below 20 C and reduced radiation preference above 20 C. Wind scoring uses exploratory design bands: cold-season upper target 3 m/s, warm-season 1–5 m/s. These are user-design assumptions, not regulatory thresholds or verified comfort criteria.

500-iteration simulated annealing jointly searches geographic azimuth (1-degree resolution) and base per-floor setback (0.01 m); reference mode searches setback only. Geometry-only evaluation avoids regenerating facade meshes each iteration. Existing floor count, base geometry, bridge floors, independent noise and extra setbacks remain fixed. Retained floor area is a hard constraint. The original is included as a feasible candidate, best-so-far is retained independently, and completion or stop applies the best feasible candidate found. No global optimum is guaranteed. Fixed baseline XY samples are used, with terrace heights tracking the highest surface. Restore returns to the pre-run mode, azimuth and setback.

V4.13: every annealing iteration applies and fully rebuilds its candidate (including cache hits), updates its heatmap and status, and yields two animation frames before the next candidate. The live card distinguishes accepted, rejected and infeasible candidates from the best-so-far state. Completion or early stop restores the historical best feasible model.
