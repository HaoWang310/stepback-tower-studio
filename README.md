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

Optimizer uses 80-iteration simulated annealing over the setback increment, with Metropolis acceptance and exponential cooling (0.08 to 0.0005). Score balances normalized sunshine and estimated wind exposure; retained floor area is a hard constraint. Fixed baseline XY samples are evaluated hourly for the complete selected day; terrace sample heights follow the highest surface at that XY. The original is included as a feasible candidate, best-so-far is retained independently of the current state, and completion or stop applies the best feasible candidate found. This is not a guarantee of a global optimum. Restore returns to the pre-run setback.
