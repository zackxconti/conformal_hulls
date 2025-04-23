# pyhull

**Work in Progress**

`pyhull` is a Python package for interpolating surface pressure and shear stress on hull geometries. Designed for use in fluid mechanics and marine hydrodynamics applications, the software also includes utilities for visualisation and preprocessing of hull surface data for machine learning workflows.

## Features

- Load and parse mesh snapshots
- Extract surface geometry and scalar fields (e.g. pressure, wall shear stress)
- Compute UV mapping of complex surfaces
- Resample data onto structured UV-grids
- Perform Proper Orthogonal Decomposition (POD)
- Interpolate and reconstruct flow fields on arbitrary hull geometries

## Workflow Overview

1. **Load Mesh Snapshots**  
   Import mesh data from simulation or experiment.

2. **Extract Geometry & Scalar Fields**  
   Retrieve coordinates and surface variables like pressure and shear stress.

3. **Compute UV Mapping**  
   Generate a parameterized surface representation.

4. **Resample onto UV Grid**  
   Interpolate unstructured data onto a consistent 2D UV grid.

5. **Compute POD**  
   Decompose the dataset into dominant modes of variation.

6. **Interpolate & Reconstruct Fields**  
   Use POD modes to interpolate and reconstruct surface quantities.

## Installation

```bash
git clone https://github.com/zackxconti/conformal_hulls.git
cd pyhull
pip install -e .