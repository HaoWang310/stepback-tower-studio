# 单体塔楼生成器 · Unit Tower

Upload one unit as STL and the page stacks it into a tower with the logic of the Grasshopper file `建筑测试.gh`:

1. **Offset Mesh** – an open surface is thickened into a solid (closed solids are used as they are).
2. **Series + Move** – floors are stacked; floor pitch = unit height + clear height. A unit taller than 2.5 m counts as a whole storey, so its clear height defaults to 0 (otherwise 3.6, as in the gh).
3. **Scale NU** – XY waist scaling about each floor's centroid, 1 → minimum → 1 (linear like the gh, or smooth cosine). For an even floor count the linear values equal the gh's Series + Reverse List + Merge exactly.
4. **Rotate** – a constant twist per floor about the same centroid.

Defaults: 20 floors (the gh file has 40), clear height 3.6 m, minimum 0.62, 22.5° per floor, thickness 0.1 m.

Export: STL (merged), OBJ and 3DM (one object per floor), in the units of the uploaded file. 3DM export loads rhino3dm from jsDelivr on demand, so it needs a network connection.

`sample-unit.stl` (57.6 × 57.6 × 3.6 m open surface, with flipped and twisted patches) is the default example; the page repairs it live (unified normals, two-sided thickening), so the thickness slider stays available. `sample-unit-repaired.stl` is the same unit already repaired and thickened 0.1 m into a closed solid (200,192 triangles, no open edges), for direct use in Rhino or printing. Opened straight from disk the page falls back to a built-in floor plate, because browsers block reading the neighbouring file.

Single file, no build step; preview uses plain WebGL2 instancing.

**Waist scaling: Stepped / Continuous** (Waist section, under Curve).

- *Stepped* (逐层) is the gh's Scale NU: one scale per floor, so a floor's top edge and the next floor's bottom edge differ by one scale step (for 20 floors and minimum 0.62 that is 4.2 % of the radius — 0.31 m on catalogue surface 001).
- *Continuous* (连续) scales every point by the waist outline at its own height: `s(q) = 1 − (1 − min)·u` (linear) or `1 − (1 − min)·(1 − cos πu)/2` (smooth), with `u = 1 − |2q − 1|` and `q` = height / tower height. Bottom and top are 1, mid-height is the minimum, and a floor's top edge has the same scale as the next floor's bottom edge, so the seams line up. With fewer than 3 floors there is no waist, as before.
- The default is picked automatically when a unit is loaded, from the same measurement as the floor-joint ticks: a unit is **joining** when its top and bottom are cut edges (no horizontal faces on the top or bottom plane) and some twist angle brings ≥ 90 % of the top edge onto the bottom edge → Continuous. Everything else is a **separate** unit → Stepped (the sample unit and the sample slab are separate, so they stay exactly like the gh). A small tag next to the control shows the result (Auto · joining / Auto · separate).
- Choosing by hand turns the tag into *Manual* and is remembered per model; clicking the tag goes back to automatic. A note appears when Continuous cannot help (the twist is not at a joining angle, or the unit is separate and its vertical faces would slant) or when Stepped leaves a step on a joining unit.
- It applies everywhere: the view, waist colour and outline, Play, STL / OBJ / 3DM export, print pieces and plate packing. The print wall is still added after scaling, so it stays constant.

**Play** (▶ in the top-right of the view): a 12 s generation sequence — unit (Offset Mesh) → floors drop in one by one (Series + Move) → waist (Series + Reverse List + Merge → Scale NU, about each floor's centroid) → twist (Series → Rotate) — with captions naming the gh components, then a continuous orbit (20 s per turn, gentle up-and-down). Dragging pauses the camera for 2 s; changing a parameter stops it.

**Waist display**: the waist is easy to lose behind the twist (arm orientation changes the silhouette by up to ~29 % floor to floor), so the view draws a waist outline — orange profile lines facing the camera at radius = farthest point of the unit × floor scale, plus dashed rings at the bottom, narrowest and top floors (toggle in the Waist section). A second toggle colours floors by scale (white → orange, with legend). During Play the waist stage colours the tower and shows the outline, the colour fades back to white during the twist, and the orbit shows the white model with the outline. Display only; exports are unaffected.

**Opening model**: the page opens with the last STL you imported in this browser (kept in IndexedDB, with its parameters), otherwise straight with `sample-unit.stl` (a short "loading" note instead of the slab placeholder); parameters are remembered per model (last 6) in localStorage. "Forget saved model" clears the stored import. Nothing is uploaded anywhere — it stays in the browser.

**Language**: Chinese / English (中 | EN switch next to the title). The page follows the browser/system language on first visit and then remembers the last choice; exported ZIP folders, file names, `assembly.svg`/`组装图.svg` and the notes follow the interface language.

## Print parts (Bambu Lab A1, 256 × 256 × 256 mm)

Panel **打印分件** exports every floor as two printable pieces in one ZIP:

- Each floor is cut at the unit's mid-height: `N-1` = upper half, `N-2` = lower half. For the sample unit the unit's own top / bottom goes on the plate (upper half flipped), so both print as open troughs and the hollow arms need no internal supports (the estimated support volume drops by about 84 %).
- **Which face goes down is chosen automatically**, once per half: the page builds the widest floor both ways (unit top / bottom on the plate, or cut face on the plate) and compares the down-facing area steeper than 45° and the area lying on the plate. The cut face goes down only when that is clearly better (≥ 20 % less overhang, or similar overhang and ≥ 50 % more plate contact). The sample unit keeps its orientation; catalogue surfaces 003 and 005 turn over. The preview caption and the notes say which halves are flipped.
- Scale 1:300 / 1:500 (default) / 1:750 / 1:1000; print wall 1.2 mm by default. Each floor is scaled first and then thickened, so the wall stays 1.2 mm on the small waist floors too.
- A raised 7-segment floor label (`18-1`, `18-2`) sits on a flat, upward-facing floor inside the piece, hidden once assembled; file names match (`18-1.stl`, `18-2.stl`). Surfaces without such a floor (most minimal surfaces) get a **snap-off tag** instead: a 0.6 mm plate with the raised number beside the piece, held by a 0.8 × 0.4 mm link at plate level. Whether a half uses tags is decided from its widest and narrowest floor; the tag is part of the packing outline.
- **Plate packing**: pieces are packed onto 256 × 256 mm plates by their real outline (first-fit decreasing on a 1 mm raster, rotations 0°/45°, pieces from any floor may share a plate), plate margin 10 mm and 6 mm between pieces by default (both editable). The sample tower needs 7 plates at 1:500. **排盘预览** shows each plate in 3D.
- The ZIP has `按盘/` (one STL per plate, pieces already placed, named `盘01.stl`, `盘02.stl` … — the pieces on each plate are listed in the notes and the assembly drawing; long names broke the 260-character path limit on Windows), `单片/` (one STL per piece), `组装图.svg` (angle, scale and plate per floor) and `说明.txt`. Floors are glued; there are no alignment pins yet.
- Only open-surface units can be cut this way (closed solids are not supported yet).
- The cut is clean: mesh vertices lying exactly on the cut plane (the sample unit has a whole row at mid-height) are shared by both halves instead of being re-cut into near-duplicates, and the shell's offset at the cut slides along the wall onto the plane, so the glue faces are flat (no sawtooth, wall thickness kept). Anything the offset pushes past the cut plane (near-horizontal surface just below or above the cut) is clamped onto it, so both halves are exactly half a floor high and close without a gap.

- **Joining units** (see *Waist scaling*) get flat top and bottom rims: the offset of the unit's top / bottom edge slides along the wall onto the unit's own plane, exactly like the cut, and anything pushed past the plane is clamped onto it. Each half is then exactly half a floor high (it used to be up to 0.6 mm taller) and lies flat on the plate. The on-screen shell is built the same way, so the floor pitch equals the unit height (002: 3.6 m instead of 3.7 m). Separate units such as the sample unit are unchanged.

### Print in segments

For joining units with clear height 0, **Export segment STL** writes the tower itself at print scale with the print wall, standing upright: every floor is scaled (per height for a continuous waist), thickened to the constant print wall, given flat rims, twisted and lifted; the flat rims of neighbouring floors overlap by 0.02 mm so the slicer fuses them. A segment is at most 250 mm tall (A1 height 256 mm): the 20-floor tower at 1:500 is one 144 mm piece, at 1:200 two segments of 10 floors. One segment downloads as a single STL, several as a ZIP (`段01_1-10层.stl` …) in the tower's own orientation, so they stack without turning. Overhanging undersides need supports in the slicer. This is the practical way to print surface 002, whose single floor is a set of separate helical ramps.

### Keep the form (保形)

Thickening a thin minimal surface by a fixed wall closes its narrow openings and the slit between the sheets. With **保形 on** (default for catalogue / joining units, off for the sample unit) the page sets the scale from the wall instead:

- A form field is computed once per unit, twist and pitch (in the background, with progress; 001 about 1 s, 004 with 197k vertices about 17 s after clustering to ~20k). For every vertex and side it measures the room to the nearest *other* part of the surface (path along the surface > 1.6 × straight distance), including the floors above and below, and the fold limit from curvature. Outward sides are capped at half the wall.
- **Auto scale** = the largest scale at which 95 % of the tower (every floor, waist scale included) keeps at least 80 % of each opening: `den = floor5(1000 · unit · fit95 / wall)`. The tag beside the scale shows 自动 / 手动; typing a scale switches to manual, clicking the tag returns to auto. If the result no longer fits the A1 plate the page uses the largest scale that fits, says how thick the wall may be at most, and offers a button to set it.
- The remaining narrow spots are thinned to follow the form (each side gets at most its room, the other side takes the rest of the wall up to its own room) and are shown **orange** in the piece and plate previews; the panel lists their share and the thinnest wall.
- Wall 1.2 mm gives: 001 1:195 (369 mm), 002 1:160, 003 1:180, 005 1:300 (240 mm, one piece); the slender 004 (1:105) and 006 (1:85) are recommended as parts.
- Pieces, plates and segment STLs all use the variable wall; changing wall or scale afterwards is instant.

### Bambu check & repair

Bambu Studio reads an STL by merging points with identical coordinates and complains about edges that are not shared by exactly two faces ("non-manifold edges"); its own repair runs only on Windows, so on a Mac it points to an online fixer. The page now makes clean files and checks every export the same way:

- **At the source**: floor labels and snap-off tag numbers are one solid per text (union of the 7-segment bars on a grid), not touching boxes. **Tower STL** of a joining unit with clear height 0 is one closed solid: every floor's mid-surface is placed, the points where a floor's top edge meets the next floor's bottom edge are welded (a fifth of a boundary edge), and the whole tower is thickened once (wall scaled with each floor, as on screen). Towers above 1.5 M points (004) are still written floor by floor. In the catalogue, the side walls of the thickened unit follow the boundary direction and the solid faces outward.
- **Check on export** (`MeshFix`, same code in both pages): print ZIP, segment STL, tower STL and the catalogue STL are read back like the slicer does (bit-identical float32 points) and counted: open edges, non-manifold edges, faces wound against their neighbour, zero-area faces. A line under the export button shows the result; anything found is repaired before the file is written.
- **Repair**: drop degenerate / duplicate faces → pair the faces at a crowded edge (same separate piece, then same fan around its ends, then by angle so each pair encloses material) → split the points into fans → one winding per piece, closed pieces outward → close holes (up to 64 edges or half the model size) → move split copies 2 µm-scale apart so they stay separate when re-read. Two pairing strategies are tried and the cleaner result kept.
- **Repair STL…** (bottom of the print panel): any STL, binary or ASCII, processed in the browser and downloaded as `name_修复.stl`.
- Known leftovers: catalogue 005 keeps 8 edges at the four-tile corner where side walls pass through each other (reported, slicing works). 001's centre axis (six sheets meeting at one point) shows up on plates only (points merge at plate coordinates) and is split during export.
- `node unit-tower/test-meshfix.cjs` checks labels, repair and that both pages carry the same `MeshFix`.

## From the minimal surface catalogue

Both pages share a step bar: **‹ Catalogue · ① Unit ② Tower ③ Print**. In the catalogue (`../minimal-surfaces/`), **Use as tower unit →** stores the current unit (open mid-surface with its placement and mirror array, Z up, scaled so one unit = one 3.6 m floor) in this browser and opens this page, which loads it with clear height 0. The twist is set to the first angle where floors join, and a unit card shows its thumbnail and parameters with a link back.

**Floor joints**: for open-surface units the page measures how much of each floor's top edge meets the next floor's bottom edge (turned by the twist), for every angle from −180° to 180°. Angles with ≥ 90 % contact get cyan ticks under the twist slider, and the slider snaps to them; below 50 % a warning says the printed floors will not hold. Units whose top or bottom is a horizontal sheet (like the sample slab) skip this check. The twist slider now runs from −180° to 180°.

**② Tower / ③ Print**: Print parts is its own step; entering it previews the parts of the selected floor.

**Display colours**: Display is now White model / Catalogue colours / Waist colour. A unit sent from the catalogue opens with Catalogue colours — the front and back colours of the palette chosen there (including “Original”), the front colour on the side the catalogue's normals face, the back colour on the other, and a blend on the rims. The palette can only be changed in the catalogue. Imported STLs have no catalogue colours; print previews stay white.

## Sample unit download

The page loads `sample-unit.bin` (0.28 MB), a lossless repack of `sample-unit.stl` (4.9 MB): the same triangles in the same order, bit for bit. It is downloaded once, kept in the browser (IndexedDB key `sample-bin-v1`), and read locally afterwards. The loading text shows the download percentage. If the compact file cannot be fetched or the browser cannot decompress it, the page falls back to the original STL; if that fails too, it keeps the current model and says so.

Format (gzip of): `UTU1`, vertex count, triangle count (uint32 LE); vertex positions as float32, axis-major (all x, all y, all z), byte-shuffled; then one uint32 per triangle corner, byte-shuffled, holding `runningMax + 1 − index`. `pack-sample.py` rebuilds the file from `sample-unit.stl`.

**Print scale**: typed in as 1:N, any whole number from 1 to 1000 (default 1:500). It applies on Enter or when the box loses focus; out of range it is clamped to 1 or 1000, and anything that is not a number puts the old value back. − and + step by 10 (100 with Shift). Under the box: the smallest scale whose largest piece fits the A1, using the same room the plate packer needs (plate margin and part spacing). If the largest piece does not fit, Preview plates and Export ZIP are switched off and a button changes the scale to that smallest fitting one; below 10 mm a yellow note says the floor labels will not fit.
