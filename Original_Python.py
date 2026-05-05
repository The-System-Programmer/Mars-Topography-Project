import numpy as np
import pyvista as pv
import colorcet as cc
from pathlib import Path

# ----------------------------
# 1. Load MOLA DEM (PDS3 IMG)
# ----------------------------
rows, cols = 5760, 11520
img_path = Path("/home/linux/Code/Mars-Topography-Project/megt90n000fb.img")

# Read big-endian int16
data = np.fromfile(img_path, dtype=">i2", count=rows * cols)
assert data.size == rows * cols, "File size mismatch!"

# Reshape to (rows, cols)
data = data.reshape((rows, cols)).astype(np.float32)

# Mask invalid values (MOLA valid range ~[-8206, 21181] m)
data[data < -10000] = np.nan

# Save intermediate (optional)
np.save("mola_elevation.npy", data)

# ----------------------------
# 2. Build planar grid (no warp)
# ----------------------------
# From label: MAP_SCALE = 1.853 km/pixel
pixel_m = 1.853 * 1000.0

x = np.arange(cols) * pixel_m
y = np.arange(rows) * pixel_m
x2d, y2d = np.meshgrid(x, y)

# Z is the elevation itself (no exaggeration)
grid = pv.StructuredGrid(x2d, y2d, data)

# Store elevation explicitly for coloring
grid.point_data["elevation"] = data.ravel(order="C")

# Save VTK (optional)
grid.save("mola_topology.vts")

# ----------------------------
# 3. Visualization (no exaggeration)
# ----------------------------
plotter = pv.Plotter()
plotter.add_mesh(
    grid,
    scalars="elevation",
    cmap=cc.CET_L17,
    clim=(-8200, 21200),
    smooth_shading=True
)

plotter.show()
