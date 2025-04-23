import os, sys, math
import numpy as np
import pyvista as pv
import igl, vtk
from scipy.linalg import svd
from scipy.spatial import cKDTree

# -------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------

def extract_hull_mesh(foam_path: str, CLIP_TOP=True, clip_z_off=0.95) -> pv.PolyData:
    rdr = vtk.vtkOpenFOAMReader()
    rdr.SetFileName(foam_path)
    rdr.DecomposePolyhedraOn()

    rdr.DisableAllPatchArrays()
    rdr.SetPatchArrayStatus("internalMesh", 1)
    rdr.SetPatchArrayStatus("patch/hull", 1)
    rdr.SetPatchArrayStatus("patch/hull_hc", 1)
    rdr.Update()

    mblock = rdr.GetOutput()
    hull_blocks = mblock.GetBlock(1)
    pieces = []
    for i in range(hull_blocks.GetNumberOfBlocks()):
        sub = hull_blocks.GetBlock(i)
        poly = pv.wrap(sub).extract_surface().triangulate()
        if "p" in poly.cell_data:
            poly = poly.cell_data_to_point_data()
        pieces.append(poly)

    hull = pv.MultiBlock(pieces).combine().extract_surface().triangulate()

    # Optionally clip the top
    if CLIP_TOP:
        z_max = hull.points[:, 2].max()
        clip_z_max = z_max - clip_z_off  # user offset
        clip_plane = vtk.vtkPlane()
        clip_plane.SetOrigin(0, 0, clip_z_max)
        clip_plane.SetNormal(0, 0, -1)
        clipper = vtk.vtkClipPolyData()
        clipper.SetInputData(hull)
        clipper.SetClipFunction(clip_plane)
        clipper.Update()
        hull = pv.wrap(clipper.GetOutput())

    hull["Area"] = hull.compute_cell_sizes()["Area"]
    hull = hull.threshold(value=1e-8, scalars="Area").clean()
    
    # Check for non-manifold edges
    feature_edges = vtk.vtkFeatureEdges()
    feature_edges.SetInputData(hull)
    feature_edges.BoundaryEdgesOn()
    feature_edges.NonManifoldEdgesOn()
    feature_edges.ManifoldEdgesOff()
    feature_edges.FeatureEdgesOff()
    feature_edges.Update()
    nonmanifold_edges = feature_edges.GetOutput()
    print("Non-manifold edge count:", nonmanifold_edges.GetNumberOfCells())

    return hull


def map_vertices_to_square(V, b):
    B = V[b]
    seg = np.linalg.norm(B - np.roll(B, -1, axis=0), axis=1)
    cum = np.insert(np.cumsum(seg), 0, 0.0)[:-1]
    cum /= cum[-1] + seg[-1]
    t = 4*cum
    uv = np.zeros((len(b),2))
    for i,s in enumerate(t):
        if s<1: uv[i]=[s,0]
        elif s<2: uv[i]=[1,s-1]
        elif s<3: uv[i]=[3-s,1]
        else: uv[i]=[0,4-s]
    return uv


def harmonic_uv(V,F,to_square=False):
    b = igl.boundary_loop(F)
    if to_square:
        bnd_uv = map_vertices_to_square(V,b)
    else:
        bnd_uv = igl.map_vertices_to_circle(V,b)
    return igl.harmonic(V,F,b,bnd_uv.astype(V.dtype),1)
