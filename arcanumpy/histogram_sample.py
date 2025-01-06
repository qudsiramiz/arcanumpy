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
# from arcanumpy.histogram_plots import hist_plots
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
"""

x = np.random.lognormal(mean=0, sigma=2, size=10000)
# x = np.clip(x, 1e-3, 1e2)
y = np.random.lognormal(mean=0, sigma=2, size=10000)
# y = np.clip(y, 1e-3, 1e2)
Z1 = np.random.lognormal(mean=0, sigma=2, size=10000)
# Z1 = np.clip(Z1, 1e-5, 1e0)
Z2 = np.random.lognormal(mean=0, sigma=2, size=10000)
# Z2 = np.clip(Z2, 1e-5, 1e0)

indx = np.where((Z1 > 1e-3) & (Z2 > 1e-3))[0]
z_ratio = Z1 / Z2

z1 = []
z2 = Z1
z3 = Z2
z4 = z_ratio

x_min = 1e-3
x_max = 1e2
y_min = 1e-3
y_max = 1e2

xlim = [x_min, x_max]
ylim = [y_min, y_max]
bins = 100
cmin = 10

(ex2, ey2, hst1, hst2) = hp.hist_plots().get_brzl_hist(
    x=x, y=y, z=z1, xlim=xlim, ylim=ylim, bins=bins, c_min=cmin
)
(ex4, ey4, hst3, hst4) = hp.hist_plots().get_brzl_hist(
    x=x, y=y, z=z2, xlim=xlim, ylim=ylim, bins=bins, c_min=cmin
)
(ex6, ey6, hst5, hst6) = hp.hist_plots().get_brzl_hist(
    x=x, y=y, z=z3, xlim=xlim, ylim=ylim, bins=bins, c_min=cmin
)
(ex8, ey8, hst7, hst8) = hp.hist_plots().get_brzl_hist(
    x=x, y=y, z=z4, xlim=xlim, ylim=ylim, bins=bins, c_min=cmin
)

data = [hst2, hst4, hst6, hst8]

ex = ex2
ey = ey2
fig = hp.hist_plots().brazil_plot_multiple(
    data=data,
    ex=ex,
    ey=ey,
    # xmin=1e-3,
    # xmax=1e2,
    # ymin=1e-3,
    # ymax=1e2,
    # bins=100,
    # nbins=10,
    # cmin=10,
    # cmax=1000,
    # norm="log",
    # cmap="cividis_r",
    # vmin=10,
    # vmax=1000,
    save_fig=True,
    plot_show=False,
)
