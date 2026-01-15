import numpy as np
from pathlib import Path

# Mola metadata
rows = 2880
cols = 5760

# Load raster
p = Path("/home/system/Code/Mars Topography project/megt90n000eb.img")
data = np.fromfile(p,dtype=">i2",count = rows*cols).reshape((rows,cols)).astype(np.float32)
<<<<<<< HEAD
=======
data[data <= -32768] = np.nan
>>>>>>> 7ce6d6d (Project)
# Flip data
data = np.flipud(data)
# Export data as a .npy file
np.save("mola_elevation.npy",data)
