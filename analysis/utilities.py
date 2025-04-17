import os
import xarray as xr
from os.path import isdir
from os.path import join as pjoin
from plotly.subplots import make_subplots

def open_minian(dpath, post_process=None, return_dict=False):
    """
    Opens a file previously saved in minian handling the proper data format and chunks
    Args:
        dpath ([string]): contains the normalized absolutized version of the pathname path,which is the path to minian folder;
        Post_process (function): post processing function, parameters: dataset (xarray.DataArray), mpath (string, path to the raw backend files)
        return_dict ([boolean]): default False
    Returns:
        xarray.DataArray: [loaded data]
    """
    dslist = [
        xr.open_zarr(pjoin(dpath, d), consolidated=False)
        for d in os.listdir(dpath)
        if isdir(pjoin(dpath, d)) and d.endswith(".zarr")
    ]
    if return_dict:
        dslist = [list(d.values())[0] for d in dslist]
        ds = {d.name: d for d in dslist}
    else:
        ds = xr.merge(dslist, compat="no_conflicts")
    if (not return_dict) and post_process:
        ds = post_process(ds, dpath)
    return ds


def custom_graph_template(x_title, y_title, template='simple_white', height=500, width=500, linewidth=1.5,
                          titles=[''], rows=1, columns=1, shared_y=False, shared_x=False, font_size=22, font_family='Arial', **kwargs):
    """
    Used to make a cohesive graph type. In most functions, these arguments are supplied through **kwargs.
    """
    fig = make_subplots(rows=rows, cols=columns, subplot_titles=titles, shared_yaxes=shared_y, **kwargs)
    fig.update_yaxes(title=y_title, linewidth=linewidth)
    fig.update_xaxes(title=x_title, linewidth=linewidth)
    fig.update_layout(title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig.update_annotations(font_size=font_size)
    fig.update_layout(template=template, height=height, width=width, font=dict(size=font_size), font_family=font_family)
    if shared_x:
        fig.update_xaxes(matches='x')
    if shared_y:
        fig.update_yaxes(matches='y')
    return fig