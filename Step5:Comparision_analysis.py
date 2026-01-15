import numpy as np
import matplotlib.pyplot as plt

# --------------------------------
# Load Mars elevation data
# --------------------------------
# Option A: from the original NumPy array
elev = np.load("mola_elevation.npy")

# If you prefer loading from the VTK grid instead, comment above and use:
# import pyvista as pv
# grid = pv.read("mola_topology.vts")
# elev = grid.points[:, 2]

# --------------------------------
# Clean elevation
# --------------------------------
e = elev[~np.isnan(elev)]

# --------------------------------
# Constants
# --------------------------------
EVEREST_KM = 8.85
OLYMPUS_KM = np.nanmax(e) / 1000
LOWEST_KM  = abs(np.nanmin(e)) / 1000

# --------------------------------
# Create plots
# --------------------------------
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# 1. Mars elevation histogram
axs[0, 0].hist(e / 1000, bins=200)
axs[0, 0].set_title("Mars Elevation Distribution")
axs[0, 0].set_xlabel("Elevation (km, areoid)")
axs[0, 0].set_ylabel("Area frequency")

# 2. Highest vs Lowest on Mars
axs[0, 1].bar(["Highest", "Lowest"], [OLYMPUS_KM, LOWEST_KM])
axs[0, 1].set_title("Mars Vertical Extremes")
axs[0, 1].set_ylabel("Distance from areoid (km)")

# 3. Earth vs Mars highest peak
axs[1, 0].bar(
    ["Everest (Earth)", "Olympus Mons (Mars)"],
    [EVEREST_KM, OLYMPUS_KM]
)
axs[1, 0].set_title("Highest Mountains: Earth vs Mars")
axs[1, 0].set_ylabel("Height above reference (km)")

# 4. Peak rank plot (top 20)
top_peaks = np.sort(e)[::-1][:20] / 1000
axs[1, 1].plot(top_peaks, marker="o")
axs[1, 1].set_title("Top 20 Highest Points on Mars")
axs[1, 1].set_xlabel("Peak rank")
axs[1, 1].set_ylabel("Elevation (km)")

plt.tight_layout()
plt.show()
