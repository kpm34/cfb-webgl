# 3D Asset Pipeline (Landing Page)

This documents the non-modeling pipeline to produce lightweight GLBs for the landing page.

## Stadium Slice (Blender → GLB)
1. Procedural Stadiums add-on.
2. Hide non-hero elements: upper decks, audience, corridors, far lights, extra ads.
3. Keep: field, nearby lower bowl, rail/fence hints.
4. Scene → Simplify → Max Subdivision = 0; enable "Use Simplify".
5. Export glTF 2.0 (.glb): Selected Collections only, Apply Modifiers, textures ≤ 2K.
   - Name: `stadium_slice_raw.glb`.
6. Run optimization script to produce KTX2 + reduced triangles.

## Jumbotron (Meshy → GLB)
1. Export as `jumbotron_raw.glb` (textures embedded).
2. Run optimization script to produce `jumbotron_ktx2.glb` under budgets.

## Backplate (Optional)
Render a 3840×2160 PNG from Blender aligned with hero camera; slight blur (σ=2–4). Use as background to sell scale with near-zero geometry.

## Budgets
- Jumbotron visible triangles ≤ 50k.
- Initial load ≤ 4–5 MB gz (JS+models+CSS; videos lazy).
- Textures KTX2; prefer 2K.

## Scripts
- `ops/3d/optimize-jumbotron.sh`
- `ops/3d/optimize-stadium-slice.sh`

Run from project root:
```bash
bash ops/3d/optimize-jumbotron.sh path/to/jumbotron_raw.glb
bash ops/3d/optimize-stadium-slice.sh path/to/stadium_slice_raw.glb
```
