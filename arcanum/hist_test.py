import pandas as pd
from pathlib import Path
import numpy as np
import importlib

import histogram_plots as hp

importlib.reload(hp)
"""
fnwnd = "/mnt/cephadrius/udel_research/pic/data/all_omnl_data/all_wind_data_v06.p"

df = pd.read_pickle(fnwnd)

dir_par_list = [None]
dir_per_list = [None]

ex, ey, hist, n_hist = hp.hist_plots().brazil_plots(
    bp=df.beta_par_p,
    rp=df.r_p_x,
    xmin=1e-3,
    xmax=1e2,
    ymin=1e-1,
    ymax=1e1,
    g_lim_1=2,
    g_lim_2=2,
    g_lim_3=2,
    g_lim_4=2,
    nbins=100,
    dir_par=dir_par_list[0],
    dir_per=dir_per_list[0],
    res="hi-res",
    loc=1,
    plot_thresh=True,
    plot_ver_thresh=False,
    save_fig=True,
    sim="wnd",
    plot_show=True,
    density=True,
)

"""
# Define a a random 1000x1 array
x = np.random.rand(10000)
y = np.random.rand(10000)
# Find the pdf
(_, _, _) = hp.hist_plots().joint_pdf(x, y, bins=100, save_fig=True)
