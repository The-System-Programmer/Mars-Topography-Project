import numpy as np
import pyvista as pv

# Load data
data = np.load("mola_elevation.npy")

pixel_km = 3.705
pixel_m  = 1000 * pixel_km

rows,cols = data.shape
x = np.arange(cols)*pixel_m
y = np.arange(rows)*pixel_m
x2d,y2d = np.meshgrid(x,y)

grid = pv.StructuredGrid(x2d,y2d,data)
grid.save("mola_topology.vts")
