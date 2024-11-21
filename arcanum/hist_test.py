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
    # dir_par=dir_par_list[0],
    # dir_per=dir_per_list[0],
    res="hi-res",
    loc=1,
    plot_thresh=True,
    plot_ver_thresh=False,
    save_fig=True,
    sim="wnd",
    plot_show=False,
    density=True,
    pcolormesh_kwargs={
        "norm": "log",
        "cmap": "cividis_r",
    },
)

# Create a random 1000x1 array centered at 1, varying between 1e-3 and 1e2 with a standard deviation
# of 150
x = np.random.normal(1, 150, 1000)
"""

"""
# Define a a random 1000x1 array
x = np.random.lognormal(mean=0, sigma=2, size=100000)
x = np.clip(x, 1e-3, 1e2)
y = np.random.lognormal(mean=0, sigma=2, size=100000)
y = np.clip(y, 1e-3, 1e2)

# Find the pdf
(_, _, _) = hp.hist_plots().joint_pdf(
    x,
    y,
    bins=100,
    save_fig=True,
    joint_pdf_kwargs={
        "bins": 1000,
        "cmap": "cividis_r",
        "norm": "log",
    },
    imshow_kwargs={
        "cmap": "Spectral",
        "norm": "log",
        "origin": "lower",
    },
)
"""

"""
# from arcanum.histogram_plots import hist_plots
bp = np.random.lognormal(mean=0, sigma=2, size=100000)
bp = np.clip(bp, 1e-3, 1e2)
rp = np.random.lognormal(mean=0, sigma=2, size=100000)
rp = np.clip(rp, 1e-1, 1e1)
ex, ey, hist, n_hist = hp.hist_plots().brazil_plots(
    bp=bp,
    rp=rp,
    xmin=1e-3,
    xmax=1e2,
    ymin=1e-1,
    ymax=1e1,
    # cmin=0,
    g_lim_1=2,
    g_lim_2=2,
    g_lim_3=2,
    g_lim_4=2,
    nbins=100,
    dir_par="0.001_4.000_0.000_00.00",
    dir_per="0.001_4.000_0.000",
    res="hi-res",
    loc=1,
    plot_thresh=True,
    plot_ver_thresh=False,
    save_fig=True,
    sim="wnd",
    plot_show=False,
    density=True,
    pcolormesh_kwargs={"norm": "log", "cmap": "cividis_r"},
)
"""

x = np.random.lognormal(mean=0, sigma=2, size=10000)
x = np.clip(x, 1e-3, 1e2)
y = np.random.lognormal(mean=0, sigma=2, size=10000)
y = np.clip(y, 1e-3, 1e2)

axs = hp.hist_plots().kde_plots(
    x_data=x,
    y_data=y,
    # bins=100,
    save_fig=True,
    sea_kwargs={
        "kind": "kde",
        "cbar": True,
        "thresh": 0.05,
        "fill": True,
        "levels": 10,
        "log_scale": True,
        "hue_norm": "log",
        "cmap": "Blues",
        "height": 6,
        "ratio": 8,
        "space": 0.01,
        "xlim": (1e-3, 1e2),
        "ylim": (1e-3, 1e2),
    },
)
