This repository (work in progress) hosts a software for interpolating hull surface pressure and shear stress. The package will also include a number of functions for visualisation and pre-processing hull geometry for machine learning purposes. 

The workflow so far: 

(1) Load mesh snapshots
(2) Extract geometry and scalar fields
(3) Compute UV mapping
(4) Resample onto UV-grid
(5) Compute POD
(6) Interpolate & reconstruct fields
