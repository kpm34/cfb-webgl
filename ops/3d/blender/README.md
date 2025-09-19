# Blender Stadium Exporter

Automates exporting a lightweight stadium slice using the Procedural Stadiums add-on.

## Requirements
- Blender (>= 3.6 recommended)
- Procedural Stadiums add-on installed and enabled

## Usage
From project root:
```bash
npm run 3d:blender:export -- \
  --output "/abs/path/stadium_slice_raw.glb" \
  --hide-audience --hide-upper-deck --keep-lower-bowl --texture-max 2048 \
  --camera-fov 35 --camera-height 1.6 --camera-dist 40 \
  --import-jumbotron "/abs/path/jumbotron_raw.glb"
```

Then optimize:
```bash
npm run 3d:opt:stadium -- "/abs/path/stadium_slice_raw.glb"
```

Notes:
- This script hides heavy collections (Audience/Upper/Exterior) by name and exports a GLB.
- KTX2 conversion is done in the follow-up optimization step.
