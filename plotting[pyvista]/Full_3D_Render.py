import numpy as np
import pyvista as pv
import colorcet as cc

# Load the structured grid
grid = pv.read("mola_topology.vts")

# Store true elevation as an explicit scalar
grid.point_data["elevation"]=grid.points[:,2]

# Apply vertical exaggeration (Visual only)
exag = 20.0
grid_vis = grid.warp_by_scalar(scalars="elevation",factor=exag)

# Colorcet visual settings
mars_cmap = cc.CET_L17
clim = (-8200 , 21200)     #Elevation limit

# Plotting

plotter = pv.Plotter()
plotter.add_mesh(grid_vis,scalars="elevation",cmap=mars_cmap,clim=clim,smooth_shading=True)

plotter.show()
