import plotly
import numpy as np
from stl import mesh
import plotly.graph_objects as go
import urllib


def stl2mesh3d(stl_mesh):
    p, q, r = stl_mesh.vectors.shape #(p, 3, 3)
    vertices, ixr = np.unique(stl_mesh.vectors.reshape(p*q, r), return_inverse=True, axis=0)
    I = np.take(ixr, [3*k for k in range(p)])
    J = np.take(ixr, [3*k+1 for k in range(p)])
    K = np.take(ixr, [3*k+2 for k in range(p)])
    return vertices, I, J, K


def interpolation(t1, x1, t2, x2, x):
    t = (x - x1) * (t2 - t1) / (x2 - x1) + t1
    return t


def define_shell_temperature_by_interpolation(x, y, z):
    coords = (x, y, z)
    pre_arr_by_x = []
    for i in arr:
        if (coords[0] >= i[0][0] and coords[0] < i[1][0]) or (coords[0] >= i[1][0] and coords[0] < i[0][0]):
            pre_arr_by_x.append(i)
    pre_arr_by_y = []
    for i in pre_arr_by_x:
        if coords[1] >= i[0][1] and coords[1] < i[1][1]:
            pre_arr_by_y.append(i)
    pre_arr_by_z = []
    for i in pre_arr_by_y:
        if coords[2] >= i[0][2] and coords[2] < i[1][2]:
            pre_arr_by_z.append(i)
    t1 = pre_arr_by_z[0][2]
    t2 = pre_arr_by_z[0][3]
    y1 = pre_arr_by_z[0][0][1]
    y2 = pre_arr_by_z[0][1][1]
    y = coords[1]
    t = interpolation(t1, y1, t2, y2, y)
    return t


my_mesh = mesh.Mesh.from_file('sthe_stl_model_22606154.stl')
vertices, I, J, K = stl2mesh3d(my_mesh)
x, y, z = vertices.T
colorscale= [[0, '#555555'], [1, '#e5dee5']]
mesh3D = go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=I,
            j=J,
            k=K,
            flatshading=True,
            colorscale=colorscale,
            intensity=z,
            name='LOTUS STHE',
            showscale=False)
title = "Mesh3d LOTUS STHE"
layout = go.Layout(
    paper_bgcolor='rgb(1,1,1)',
    title_text=title,
    title_x=0.5,
    font_color='white',
    width=1600,
    height=800,
    scene_camera=dict(
        eye=dict(x=1.25, y=1.25, z=1)),
    scene_xaxis_visible=True,
    scene_yaxis_visible=True,
    scene_zaxis_visible=True,
    scene = dict(aspectratio = dict(
        x = 4,
        y = 1,
        z = 1
    )),
)
fig = go.Figure(data=[mesh3D], layout=layout)
fig.show()