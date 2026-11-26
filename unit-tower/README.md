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

**Play** (▶ in the top-right of the view): a 12 s generation sequence — unit (Offset Mesh) → floors drop in one by one (Series + Move) → waist (Series + Reverse List + Merge → Scale NU, about each floor's centroid) → twist (Series → Rotate) — with captions naming the gh components, then a continuous orbit (20 s per turn, gentle up-and-down). Dragging pauses the camera for 2 s; changing a parameter stops it.

**Waist display**: the waist is easy to lose behind the twist (arm orientation changes the silhouette by up to ~29 % floor to floor), so the view draws a waist outline — orange profile lines facing the camera at radius = farthest point of the unit × floor scale, plus dashed rings at the bottom, narrowest and top floors (toggle in the Waist section). A second toggle colours floors by scale (white → orange, with legend). During Play the waist stage colours the tower and shows the outline, the colour fades back to white during the twist, and the orbit shows the white model with the outline. Display only; exports are unaffected.

**Opening model**: the page opens with the last STL you imported in this browser (kept in IndexedDB, with its parameters), otherwise straight with `sample-unit.stl` (a short "loading" note instead of the slab placeholder); parameters are remembered per model (last 6) in localStorage. "Forget saved model" clears the stored import. Nothing is uploaded anywhere — it stays in the browser.

**Language**: Chinese / English (中 | EN switch next to the title). The page follows the browser/system language on first visit and then remembers the last choice; exported ZIP folders, file names, `assembly.svg`/`组装图.svg` and the notes follow the interface language.

## Print parts (Bambu Lab A1, 256 × 256 × 256 mm)

Panel **打印分件** exports every floor as two printable pieces in one ZIP:

- Each floor is cut at the unit's mid-height. `N-1` = upper half, flipped so its flat roof lies on the plate; `N-2` = lower half. Both print as open troughs, so the hollow arms need no internal supports (for the sample unit the estimated support volume drops by about 84 %).
- Scale 1:300 / 1:500 (default) / 1:750 / 1:1000; print wall 1.2 mm by default. Each floor is scaled first and then thickened, so the wall stays 1.2 mm on the small waist floors too.
- A raised 7-segment floor label (`18-1`, `18-2`) sits on the trough floor inside an arm, hidden once assembled; file names match (`18-1.stl`, `18-2.stl`).
- **Plate packing**: pieces are packed onto 256 × 256 mm plates by their real outline (first-fit decreasing on a 1 mm raster, rotations 0°/45°, pieces from any floor may share a plate), plate margin 10 mm and 6 mm between pieces by default (both editable). The sample tower needs 13 plates. **排盘预览** shows each plate in 3D.
- The ZIP has `按盘/` (one STL per plate, pieces already placed, named e.g. `盘01_1-2_2-2_17-2_39-2_40-2.stl`), `单片/` (one STL per piece), `组装图.svg` (angle, scale and plate per floor) and `说明.txt`. Floors are glued; there are no alignment pins yet.
- Only open-surface units can be cut this way (closed solids are not supported yet).
- The cut is clean: mesh vertices lying exactly on the cut plane (the sample unit has a whole row at mid-height) are shared by both halves instead of being re-cut into near-duplicates, and the shell's offset at the cut slides along the wall onto the plane, so the glue faces are flat (no sawtooth, wall thickness kept). Anything the offset pushes past the cut plane (near-horizontal surface just below or above the cut) is clamped onto it, so both halves are exactly half a floor high and close without a gap.

## From the minimal surface catalogue

Both pages share a step bar: **‹ Catalogue · ① Unit ② Tower ③ Print**. In the catalogue (`../minimal-surfaces/`), **Use as tower unit →** stores the current unit (open mid-surface with its placement and mirror array, Z up, scaled so one unit = one 3.6 m floor) in this browser and opens this page, which loads it with clear height 0. The twist is set to the first angle where floors join, and a unit card shows its thumbnail and parameters with a link back.

**Floor joints**: for open-surface units the page measures how much of each floor's top edge meets the next floor's bottom edge (turned by the twist), for every angle from −180° to 180°. Angles with ≥ 90 % contact get cyan ticks under the twist slider, and the slider snaps to them; below 50 % a warning says the printed floors will not hold. Units whose top or bottom is a horizontal sheet (like the sample slab) skip this check. The twist slider now runs from −180° to 180°.

**② Tower / ③ Print**: Print parts is its own step; entering it previews the parts of the selected floor.

**Display colours**: Display is now White model / Catalogue colours / Waist colour. A unit sent from the catalogue opens with Catalogue colours — the front and back colours of the palette chosen there (including “Original”), the front colour on the side the catalogue's normals face, the back colour on the other, and a blend on the rims. The palette can only be changed in the catalogue. Imported STLs have no catalogue colours; print previews stay white.

## Sample unit download

The page loads `sample-unit.bin` (0.28 MB), a lossless repack of `sample-unit.stl` (4.9 MB): the same triangles in the same order, bit for bit. It is downloaded once, kept in the browser (IndexedDB key `sample-bin-v1`), and read locally afterwards. The loading text shows the download percentage. If the compact file cannot be fetched or the browser cannot decompress it, the page falls back to the original STL; if that fails too, it keeps the current model and says so.

Format (gzip of): `UTU1`, vertex count, triangle count (uint32 LE); vertex positions as float32, axis-major (all x, all y, all z), byte-shuffled; then one uint32 per triangle corner, byte-shuffled, holding `runningMax + 1 − index`. `pack-sample.py` rebuilds the file from `sample-unit.stl`.

**Print scale**: typed in as 1:N, any whole number from 1 to 1000 (default 1:500). It applies on Enter or when the box loses focus; out of range it is clamped to 1 or 1000, and anything that is not a number puts the old value back. − and + step by 10 (100 with Shift). Under the box: the smallest scale whose largest piece fits the A1, using the same room the plate packer needs (plate margin and part spacing). If the largest piece does not fit, Preview plates and Export ZIP are switched off and a button changes the scale to that smallest fitting one; below 10 mm a yellow note says the floor labels will not fit.
