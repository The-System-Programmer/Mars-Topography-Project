import numpy as np
import pyvista as pv
import colorcet as cc

# --------------------------------
# Load grid
# --------------------------------
grid = pv.read("mola_topology.vts")
points = grid.points
elev = points[:, 2]
grid["elevation_m"] = elev

# --------------------------------
# Parameters
# --------------------------------
N_PEAKS = 5
MIN_SEPARATION = 400_000  # meters

# --------------------------------
# Sort points by elevation (descending)
# --------------------------------
valid_idx = np.where(~np.isnan(elev))[0]
sorted_idx = valid_idx[np.argsort(elev[valid_idx])[::-1]]

# --------------------------------
# Select independent highest peaks
# --------------------------------
peak_indices = []

for idx in sorted_idx:
    candidate = points[idx]

    if all(
        np.linalg.norm(candidate[:2] - points[p][:2]) > MIN_SEPARATION
        for p in peak_indices
    ):
        peak_indices.append(idx)

    if len(peak_indices) == N_PEAKS:
        break

# --------------------------------
# Global lowest point
# --------------------------------
idx_min = np.nanargmin(elev)

# --------------------------------
# Create PolyData
# --------------------------------
peak_points = pv.PolyData(points[peak_indices])
low_point = pv.PolyData([points[idx_min]])

# --------------------------------
# Visual exaggeration (display only)
# --------------------------------
exag = 20.0
grid_vis = grid.warp_by_scalar("elevation_m", factor=exag)

peak_vis = peak_points.copy()
peak_vis.points[:, 2] *= exag

low_vis = low_point.copy()
low_vis.points[:, 2] *= exag

# --------------------------------
# Labels
# --------------------------------
peak_labels = [
    f"Peak {i+1}\n{elev[idx]/1000:.2f} km"
    for i, idx in enumerate(peak_indices)
]

low_label = f"Lowest Point\n{elev[idx_min]/1000:.2f} km"

# --------------------------------
# Plot
# --------------------------------
plotter = pv.Plotter()

plotter.add_mesh(
    grid_vis,
    scalars="elevation_m",
    cmap=cc.CET_L17,
    clim=(-8200, 21200),
    smooth_shading=True
)

# Highest peaks
plotter.add_mesh(
    peak_vis,
    color="red",
    point_size=5,
    render_points_as_spheres=False
)

plotter.add_point_labels(
    peak_vis,
    peak_labels,
    font_size=12,
    text_color="white",
    point_color="red"
)

# Lowest point
plotter.add_mesh(
    low_vis,
    color="blue",
    point_size=5,
    render_points_as_spheres=False
)

plotter.add_point_labels(
    low_vis,
    [low_label],
    font_size=12,
    text_color="white",
    point_color="blue"
)

plotter.add_text(
    f"Top {N_PEAKS} Highest Peaks and Global Lowest Point (MOLA)",
    font_size=14
)

plotter.show()
