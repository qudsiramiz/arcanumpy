from typing import List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pathlib import Path


class hist_plots:
    """
    Class to plot histograms and brazil plots for the given data and thresholds respectively.
    It also contains a method to calculate the probability density function of a given array.
    Name of the functions contain the following:
    - calc_pdf: calculates the probability density function of a given array
    - joint_pdf: calculates the joint probability density function of two given arrays
    - brazil_plot_with_threshold: plots the brazil plot for the given data with thresholds
    - get_thresh: gets the threshold values for the given data
    - compute_rr: computes the threshold values for the given data
    """

    def __init__(self):
        pass

    def compute_rr(self, bb=None, gamma=-2, instab="cycl"):
        """
        Threshold calculation based on Verscharen and Chandran 2018
        """

        if instab == "cycl":
            if gamma == -2:
                a = 0.649
                b = 0.400
                c = 0
            elif gamma == -3:
                a = 0.437
                b = 0.428
                c = -0.003
            elif gamma == -4:
                a = 0.367
                b = 0.364
                c = 0.011
            else:
                print(r"Only values of $\gamma/\Omega$ = -2, -3 and -4 are supported")
        elif instab == "mirr":
            if gamma == -2:
                a = 1.040
                b = 0.633
                c = -0.012
            elif gamma == -3:
                a = 0.801
                b = 0.763
                c = -0.063
            elif gamma == -4:
                a = 0.702
                b = 0.674
                c = -0.009
            else:
                print(r"Only values of $\gamma/\Omega$ = -2, -3 and -4 are supported")
        elif instab == "fir1":
            if gamma == -2:
                a = -0.647
                b = 0.583
                c = 0.713
            elif gamma == -3:
                a = -0.497
                b = 0.566
                c = 0.543
            elif gamma == -4:
                a = -0.408
                b = 0.529
                c = 0.410
            else:
                print(r"Only values of $\gamma/\Omega$ = -2, -3 and -4 are supported")
        elif instab == "fir2":
            if gamma == -2:
                a = -1.447
                b = 1.000
                c = -0.148
            elif gamma == -3:
                a = -1.390
                b = 1.005
                c = -0.111
            elif gamma == -4:
                a = -1.454
                b = 1.023
                c = -0.178
            else:
                print(r"Only values of $\gamma/\Omega$ = -2, -3 and -4 are supported")

        return 1 + a / ((bb - c) ** b)

    def get_thresh(
        self, instab, gamma, verbose=False, parnt_drct=None, drct=None, res="hi-res"
    ):

        # Open the appropriate data files for the requested instability.  If a
        # valid instability was not specified, abort.

        if parnt_drct is None:
            parnt_drct = "../.arcanum_data/linear_instability_data/protn"
            # Expand the user
            parnt_drct = Path(parnt_drct).expanduser()

        if instab in ["fir1", "fir2"]:
            ohalf = -1
        elif instab in ["cycl", "mirr"]:
            ohalf = +1
        else:
            return np.array([]), np.array([])

        if drct is None:
            if instab in ["mirr", "fir2"]:
                drct = "0.001_4.000_0.000"
            elif instab in ["cycl", "fir1"]:
                drct = "0.001_4.000_0.000_00.00"

        if instab in ["mirr", "fir2"] and res == "lo-res":
            if instab == "fir2":
                res = "hi-res"
            new_drct = f".arcanum_data/linear_instability_data/protn/{instab}/0.001_4.000_0.000/{res}/"
        else:
            new_drct = f"{parnt_drct}/{instab}/{drct}/{res}/"

        fl_b = open(new_drct + "out_bj.dat")
        fl_r = open(new_drct + "out_ri.dat")
        fl_g = open(new_drct + "out_gij.dat")

        # Extract the values in the files.

        arr_b = np.array([[float(val) for val in ln.split()] for ln in fl_b])
        arr_r = np.array([[float(val) for val in ln.split()] for ln in fl_r])
        arr_g = np.array([[float(val) for val in ln.split()] for ln in fl_g])

        (n_r, n_b) = arr_g.shape

        # If requested, print out the shape of the arrays.

        if verbose:
            plt.contour(arr_b, arr_r, arr_g)
            plt.show()

        # Initialize the threshold arrays.

        crv_b = arr_b[0, :]
        crv_r = np.zeros_like(crv_b)

        # Extract the requested threshold level. For each beta-value, use
        # interpolation to estimate the anisotropy-value that has a gamma
        # value closest to the target "gamma".
        for j in np.arange(n_b):

            # If the target value "gamma" does not fall into the range of
            # gamma-values returned for this beta-value, skip to the next
            # beta-value.
            if (np.amin(arr_g[:, j]) >= gamma) or (np.amax(arr_g[:, j]) <= gamma):

                continue

            # Search through the anisotropy-values (beginning with R = 1)
            # until one is found with a gamma-value less than the target
            # "gamma" and that is followed by an anisotropy-value with a
            # gamma-value greater than the target "gamma".

            # NOTE: The "for"-statement immediately below may seem a bit
            #        odd, but it does work.  The "[::ohalf]" ensures that
            #        the loop begins with R = 1 and moves outward.  The
            #        "[:-1]" remove supresses the final anisotropy value.
            for i in np.arange(n_r)[::ohalf][:-1]:

                # If the gamma-value of the current anisotropy-value is
                # less than the target "gamma" and the gamma-value of
                # the next anisotropy-value is greater than the target
                # "gamma", interpolate between them.

                if (
                    (arr_g[i, j] > 0.0)
                    and (arr_g[i, j] <= gamma)
                    and (arr_g[i + ohalf, j] >= gamma)
                ):

                    # Extract the bounding anisotropy-values and the
                    # logs of their corresponding gamma-values.
                    r1 = arr_r[i, j]
                    r2 = arr_r[i + ohalf, j]

                    l1 = np.log10(arr_g[i, j])
                    l2 = np.log10(arr_g[i + ohalf, j])

                    # Store the interpolated value to the threshold
                    # array.
                    crv_r[j] = ((np.log10(gamma) - l1) * (r2 - r1) / (l2 - l1)) + r1

                    # If requested, print out the interpolation
                    # values.
                    # Move on to the next beta-value.

                    break

        # Remove elements from the threshold arrays corresponding to beta-values
        # for which no anisotropy-value could be found.

        tk = np.where(crv_r != 0)

        crv_b = crv_b[tk]
        crv_r = crv_r[tk]

        #    print min(crv_b), max( crv_b), min(crv_r), max(crv_r)
        # Return the threshold arrays.

        return crv_b, crv_r

    def brazil_plot_with_threshold(
        self,
        bp: List[float],
        rp: List[float],
        xmin: float = None,
        xmax: float = None,
        ymin: float = None,
        ymax: float = None,
        bins: List[float] = None,
        nbins: float = None,
        cmin: float = None,
        vmin=None,
        vmax=None,
        g_lim_1=None,
        g_lim_2=None,
        g_lim_3=None,
        g_lim_4=None,
        dir_par=None,
        dir_per=None,
        res="hi-res",
        loc=1,
        sim=None,
        density=False,
        plot_thresh=False,
        plot_ver_thresh=None,
        save_fig=True,
        plot_show=False,
        pcolormesh_kwargs=None,
    ):
        """
        The code to plot the brazil plot for any kind of data. The scale of both x- and y-axes is
        "log", this can be changed in the line which 65 or so where "bins" is defined and setting
        both scales of x- and y-axes to linear instead of log.

        bp : ion parallel beta (type:array)
        rp : ion anisotropy (type:array)
        xmin : minimum value of x-axis (type:float)
        xmax : maximum value of x-axis (type:float)
        ymin : minimum value of y-axis (type:float)
        ymax : maximum value of y-axis (type:float)
        bins : x and y bins (type:array)
        nbins : number of bins in each direction, defaults to 50 (type:float)
        cmin : minimum value in a bin to be plotted, defaults to 10 (type:float)
        vmin : minimum value of colorbar
        vmax : maximum value fo colorbar
        g_lim_1 to 4 : value of instability thresholds to be plotted
            1 => cyclotron instability
            2 => parallel firehose instability
            3 => mirror instability
            4 => oblique firehose instability
        dir_par : directory for parallel instabilities
        dir_per : directory for oblique instabilities
        res : resolution of thresholds to be plotted, defaults to "hi-res", other option is "lo-res"
        loc : location of legend
        sim : type of data, this is used while saving figure
        density : whether to plot probabilty density or somple histogram, defaults to false
        plot_thresh : whether to plot thresholds, defaults to false
        save_fig : to save the figure or not, defaults to true
        plot_show : display the plot, defaults to false
        pcolormesh_kwargs : additional arguments to be passed to pcolormesh

        Returns
        -------
        ex : x-axis bins
        ey : y-axis bins
        hist : histogram of the data
        n_hist : normalized histogram of the data

        Examples
        --------
        >>> import numpy as np
        >>> from arcanum.histogram_plots import hist_plots
        >>> bp = np.random.lognormal(mean=0, sigma=2, size=10000)
        >>> bp = np.clip(bp, 1e-3, 1e2)
        >>> rp = np.random.lognormal(mean=0, sigma=2, size=10000)
        >>> rp = np.clip(rp, 1e-1, 1e1)
        >>> ex, ey, hist, n_hist = hist_plots().brazil_plot_with_threshold(bp=bp, rp=rp, xmin=1e-3, xmax=1e2, ymin=1e-1, ymax=1e1, cmin=0, g_lim_1=2, g_lim_2=2, g_lim_3=2, g_lim_4=2, nbins=100, dir_par="0.001_4.000_0.000_00.00", dir_per="0.001_4.000_0.000", res="hi-res", loc=1, plot_thresh=True, plot_ver_thresh=False, save_fig=True, sim="wnd", plot_show=False, density=True, pcolormesh_kwargs={"norm": "log", "cmap": "cividis_r"})
        """

        # Define all the default values
        clabelpad = 10
        labelsize = 18
        ticklabelsize = 15
        clabelsize = 15
        ticklength = 3
        tickwidth = 1.5
        ticklength = 6
        mticklength = 4
        cticklength = 5
        mcticklength = 4
        labelrotation = 0

        # Extract the data
        # Anisotropy
        rp_arr = np.array(rp)

        # Beta values
        bp_arr = np.array(bp)

        if bins is None:
            if nbins is None:
                nbins = 50
            bins = (
                np.logspace(
                    np.log10(np.nanmin(bp_arr)), np.log10(np.nanmax(bp_arr)), nbins
                ),
                np.logspace(
                    np.log10(np.nanmin(rp_arr)), np.log10(np.nanmax(rp_arr)), nbins
                ),
            )

        if cmin is None:
            cmin = 10

        # Get the 2D histogram
        (hist, ex, ey) = np.histogram2d(bp_arr, rp_arr, bins=bins)

        # Set all the bins with less than cmin to nan
        hist[hist < cmin] = np.nan

        if density:
            n_hist = np.full((np.shape(hist)), np.nan)
            N = np.nansum(hist)

            for xx in np.arange(len(ex) - 1):
                for yy in np.arange(len(ey) - 1):
                    db = ex[xx + 1] - ex[xx]
                    dr = ey[yy + 1] - ey[yy]
                    n_hist[xx, yy] = hist[xx, yy] / (N * db * dr)
            hist = []
        else:
            n_hist = hist

        if None in [vmin, vmax]:
            vmin = np.nanmin(n_hist)
            vmax = np.nanmax(n_hist)

        if None in [xmin, xmax, ymin, ymax]:
            xmin = 0.9 * ex[0]
            xmax = 1.2 * ex[-1]
            ymin = 0.8 * ey[0]
            ymax = 1.2 * ey[-1]

        # Define the figure
        fig = plt.figure(
            num=None, figsize=(5, 6), dpi=200, facecolor="w", edgecolor="gray"
        )
        fig.subplots_adjust(
            left=0.01, right=0.95, top=0.99, bottom=0.01, wspace=0.02, hspace=0.0
        )

        # Define the axes in the figure
        axs1 = fig.add_subplot(1, 1, 1)

        im1 = axs1.pcolormesh(
            ex,
            ey,
            np.transpose(n_hist),
            alpha=0.9,
            shading="auto",
            # cmap=cmap,
            # norm=norm,
            **(pcolormesh_kwargs if pcolormesh_kwargs else {}),
        )

        axs1.axhline(1, lw=1.0, c="k")

        im1.axes.tick_params(
            which="major",
            axis="both",
            direction="in",
            labelbottom=True,
            bottom=True,
            labeltop=False,
            top=True,
            labelleft=True,
            left=True,
            labelright=False,
            right=True,
            width=tickwidth,
            length=ticklength,
            labelsize=ticklabelsize,
            labelrotation=labelrotation,
        )
        im1.axes.tick_params(
            which="minor",
            axis="both",
            direction="in",
            labelbottom=False,
            bottom=True,
            labeltop=False,
            top=True,
            labelleft=False,
            left=True,
            labelright=False,
            right=True,
            width=tickwidth,
            length=mticklength,
            labelsize=ticklabelsize,
            labelrotation=labelrotation,
        )

        axs_xlabel = (
            r"$\beta_{\parallel \mathrm{p}} = 2 \mu_0 n_\mathrm{p} k_\mathrm{B}$"
            + r"$T_{\parallel \mathrm{p}}/B^2$"
        )

        axs_ylabel = r"$R_{\mathrm{p}} = T_{\perp \mathrm{p}}/T_{\parallel \mathrm{p}}$"

        axs1.set_xlabel(axs_xlabel, fontsize=labelsize)
        axs1.set_ylabel(axs_ylabel, fontsize=labelsize)

        axs1.set_xlim(xmin, xmax)
        axs1.set_ylim(ymin, ymax)
        axs1.set_xscale("log")
        axs1.set_yscale("log")

        # Create a new axis for colorbar
        divider1 = make_axes_locatable(axs1)

        # Define the location of the colorbar, it"s size relative to main figure and the padding
        # between the colorbar and the figure, the orientation the colorbar
        cax1 = divider1.append_axes("top", size="5%", pad=0.01)
        cbar1 = plt.colorbar(
            im1, cax=cax1, orientation="horizontal", ticks=None, fraction=0.05, pad=0.01
        )

        # Define the parameters related to the label of tickmarks and their relative positioning, color
        # of the tickmarks, and where they appear on the colorbar
        cax1.axes.tick_params(
            which="major",
            axis="x",
            direction="in",
            pad=0,
            labeltop=True,
            labelbottom=False,
            top=True,
            bottom=True,
            length=cticklength,
            labelsize=clabelsize,
            color="k",
        )
        cax1.axes.tick_params(
            which="minor",
            axis="x",
            direction="in",
            pad=0,
            labeltop=False,
            labelbottom=False,
            top=True,
            bottom=True,
            length=mcticklength,
            labelsize=clabelsize,
            color="k",
        )

        cbar1.ax.xaxis.set_label_position("top")

        if density is True:
            cbar_label = "Probability Density"
        else:
            cbar_label = r"$N$"

        cbar1.set_label(cbar_label, fontsize=labelsize, labelpad=clabelpad)

        if plot_thresh is True:
            if None in [g_lim_1, g_lim_2, g_lim_3, g_lim_4]:
                g_lim_1 = 2
                g_lim_2 = 2
                g_lim_3 = 2
                g_lim_4 = 2

            if None in [dir_par, dir_per]:
                dir_par = "0.001_4.000_0.000_00.00"
                dir_per = "0.001_4.000_0.000"

            crv_b_1, crv_r_1 = self.get_thresh(
                "cycl", 10 ** (-g_lim_1), drct=dir_par, res=res, verbose=False
            )
            axs1.plot(
                crv_b_1, crv_r_1, color="k", ls="dashdot", lw=1.5, label="cyclotron"
            )

            crv_b_2, crv_r_2 = self.get_thresh(
                "fir1", 10 ** (-g_lim_2), drct=dir_par, res=res, verbose=False
            )
            axs1.plot(
                crv_b_2,
                crv_r_2,
                color="orange",
                ls="dashed",
                lw=1.5,
                label="parallel firehose",
            )

            crv_b_3, crv_r_3 = self.get_thresh(
                "mirr", 10 ** (-g_lim_3), drct=dir_per, res=res, verbose=False
            )
            axs1.plot(crv_b_3, crv_r_3, color="m", ls="dashdot", lw=1.5, label="mirror")

            crv_b_4, crv_r_4 = self.get_thresh(
                "fir2", 10 ** (-g_lim_4), drct=dir_per, res=res, verbose=False
            )
            axs1.plot(
                crv_b_4,
                crv_r_4,
                color="r",
                ls="dashed",
                lw=1.5,
                label="oblique firehose",
            )

            # Set the label colors of legend label
            labelcolor = ["k", "orange", "m", "r"]
            legend_handles = axs1.legend(fontsize=clabelsize, frameon=False, loc=loc)
            for i, text in enumerate(legend_handles.get_texts()):
                text.set_color(labelcolor[i])

            # Remove ther markers from legend
            for item in legend_handles.legendHandles:
                item.set_visible(False)

            axs1.text(
                0.98,
                0.05,
                f"$\gamma/\Omega_{{cp}} = 10^{{{-g_lim_1}}}$",
                verticalalignment="center",
                horizontalalignment="right",
                fontsize=clabelsize,
                transform=axs1.transAxes,
            )

        if plot_ver_thresh is True:
            bb = np.logspace(np.log10(xmin), np.log10(xmax), 100)
            # rr = np.logspace(ymin, ymax, 100)
            rr_cycl = self.compute_rr(bb=bb, gamma=-g_lim_1, instab="cycl")
            rr_mirr = self.compute_rr(bb=bb, gamma=-g_lim_1, instab="mirr")
            rr_fir1 = self.compute_rr(bb=bb, gamma=-g_lim_1, instab="fir1")
            rr_fir2 = self.compute_rr(bb=bb, gamma=-g_lim_1, instab="fir2")

            axs1.plot(bb, rr_cycl, color="k", ls="dashdot", lw=1.5, label="cyclotron")
            axs1.plot(
                bb,
                rr_fir1,
                color="orange",
                ls="dashed",
                lw=1.5,
                label="parallel firehose",
            )
            axs1.plot(bb, rr_mirr, color="m", ls="dashdot", lw=1.5, label="mirror")
            axs1.plot(
                bb, rr_fir2, color="r", ls="dashed", lw=1.5, label="oblique firehose"
            )

            # Set the label colors of legend label
            labelcolor = ["k", "orange", "m", "r", "b", "g", "c", "y", "m", "r"]
            legend_handles = axs1.legend(fontsize=clabelsize, frameon=False, loc=loc)
            for i, text in enumerate(legend_handles.get_texts()):
                text.set_color(labelcolor[i])

            # Remove ther markers from legend
            for item in legend_handles.legendHandles:
                item.set_visible(False)

            axs1.text(
                0.98,
                0.05,
                f"$\gamma/\Omega_{{cp}} = 10^{{{-g_lim_1}}}$",
                verticalalignment="center",
                horizontalalignment="right",
                fontsize=clabelsize,
                transform=axs1.transAxes,
            )

        if save_fig is True:
            if density is True:
                fig_name = f"figures/brazil_prob_{sim}.pdf"
            else:
                fig_name = f"figures/brazil_{sim}.pdf"
            # If the directory does not exist, create it
            Path("figures").mkdir(parents=True, exist_ok=True)
            plt.savefig(
                fig_name, bbox_inches="tight", pad_inches=0.05, format="pdf", dpi=300
            )
        if plot_show is True:
            plt.show()
        plt.close("all")

        return (ex, ey, hist, n_hist)

    # TODO: Add the get_brazil_hist function and the brazil_plotting_routine_3d function

    def calc_pdf(
        self,
        input_array: np.array,
        weight=100,
        inc=None,
        Normalize=False,
        plot_pdf=False,
        save_fig=False,
        fig_name=None,
    ):
        """
        Calculate the probability density function of a given array

        Parameters
        ----------
        input_array : np.array
            The array for which the pdf is to be calculated
        weight : int, optional
            The number of points in each bin, by default 100
        inc : int, optional
            The number of points to be shifted, by default None
        Normalize : bool, optional
            Normalize the input array by the rms value, by default False
        plot_pdf : bool, optional
            Plot the pdf, by default False
        save_fig : bool, optional
            Save the figure, by default False
        fig_name : str, optional
            The name of the figure, by default None

        Returns
        -------
        np.array
            The bins of the pdf
        np.array
            The pdf of the input array

        Examples
        --------
        >>> import numpy as np
        >>> from arcanum.histogram_plots import hist_plots
        >>> x = np.random.rand(100000)
        >>> bins, x_pdf = hist_plots().calc_pdf(input_array=x, inc=5000, Normalize=False, weight=100, plot_pdf=True, save_fig=True)
        """
        # Check is the array is to be shifted
        if inc is not None:
            # Find the difference between elements in the array separated by inc
            series = input_array[inc:] - input_array[:-inc]
        else:
            series = input_array

        if Normalize:
            rmsval = series.std()
            series = series / rmsval

        series = series[~np.isnan(series)]
        # Sort the series
        series.sort()

        length = int(len(series) / weight)

        pdf = np.zeros(length)
        bins = np.zeros(length)

        # For each bin, take the size, divide by the max-min of that bin, then add to pdf
        acc = 0
        for i in range(weight, len(series), weight):
            temp = series[i - weight : i]
            bins[acc] = temp.mean()
            pdf[acc] = weight / (temp.max() - temp.min())
            acc += 1

        if plot_pdf:
            plt.figure()
            plt.plot(bins, pdf / len(series))
            plt.xlabel("Bins")
            plt.ylabel("PDF")
            if save_fig:
                if fig_name is None:
                    fig_name = "pdf.png"
                plt.savefig(fig_name)

        return bins, pdf / len(series)

    def joint_pdf(
        self,
        x: np.array = None,
        y: np.array = None,
        bins: int = 100,
        x_label: str = None,
        y_label: str = None,
        save_fig: bool = False,
        fig_name: str = None,
        joint_pdf_kwargs=None,
        imshow_kwargs=None,
    ):
        """
        Calculate the joint probability density function of two given arrays

        Parameters
        ----------
        x : np.array
            The first array for which the pdf is to be calculated
        y : np.array
            The second array for which the pdf is to be calculated
        bins : int, optional
            The number of bins in the histogram, by default 100
        x_label : str, optional
            The label of the x-axis, by default None
        y_label : str, optional
            The label of the y-axis, by default None
        save_fig : bool, optional
            Save the figure, by default False
        fig_name : str, optional
            The name of the figure, by default None
        joint_pdf_kwargs : dict, optional
            Additional arguments to be passed to the joint pdf plot, by default None. These keyword arguments are passed to the plt.hist2d function

        Returns
        -------
        np.array
            The histogram of the joint pdf
        np.array
            The x data
        np.array
            The y data

        Examples
        --------
        >>> import numpy as np
        >>> from arcanum.histogram_plots import hist_plots
        >>> x = np.random.lognormal(mean=0, sigma=2, size=100000)
        >>> x = np.clip(x, 1e-3, 1e2)
        >>> y = np.random.lognormal(mean=0, sigma=2, size=100000)
        >>> y = np.clip(y, 1e-3, 1e2)
        >>> hst, x_s, y_s = hist_plots().joint_pdf(x=x, y=y, bins=100, save_fig=True, joint_pdf_kwargs={ "bins": 1000, "cmap": "cividis_r","norm": "log",}, imshow_kwargs={
        "cmap": "Spectral", "norm": "log", "origin": "lower",},)
        """

        if x is None:
            raise ValueError("x data not provided")
            return

        if y is None:
            raise ValueError("y data not provided")
            return

        x_s = x / np.nanstd(x)
        y_s = y / np.nanstd(y)

        xr = np.linspace(np.nanmin(x_s), np.nanmax(x_s), bins)
        yr = np.linspace(np.nanmin(y_s), np.nanmax(y_s), bins)

        # Plotting the histogram
        plt.close("all")
        fig1, axs1 = plt.subplots()
        hst = axs1.hist2d(
            x_s,
            y_s,
            range=[[np.nanmin(x_s), np.nanmax(x_s)], [np.nanmin(y_s), np.nanmax(y_s)]],
            **(joint_pdf_kwargs if joint_pdf_kwargs else {}),
        )

        plt.close("all")

        # Plotting the surface contour
        X, Y = np.meshgrid(xr, yr)

        fig2, axs2 = plt.subplots(constrained_layout=True)
        # cs = axs2.contourf( X, Y, np.transpose( hst[0] ), levels=25, norm=mpl.colors.LogNorm(),cmap=plt.cm.jet, origin='lower' )
        cs = axs2.imshow(
            np.transpose(hst[0]),
            extent=[np.nanmin(x_s), np.nanmax(x_s), np.nanmin(y_s), np.nanmax(y_s)],
            # norm=mpl.colors.LogNorm(),
            # cmap=plt.cm.Spectral,
            # origin="lower",
            **(imshow_kwargs if imshow_kwargs else {}),
        )

        if x_label is not None:
            axs2.set_xlabel(x_label, fontsize=20)
        if y_label is not None:
            axs2.set_ylabel(y_label, fontsize=20)
        axs2.set_title(f"Joint PDF between {x_label} and {y_label}", fontsize=22)

        divider = make_axes_locatable(axs2)

        # Define the location of the colorbar, it's size relative to main figure
        # and the padding between the colorbar and the figure, the orientation
        # the colorbar
        cax = divider.append_axes("top", size="10%", pad=0.05)

        cbar = plt.colorbar(
            cs, cax=cax, orientation="horizontal", ticks=None, fraction=0.05, pad=0.0
        )

        cbar.ax.tick_params(
            which="both",
            direction="in",
            labeltop=False,
            top=True,
            labelbottom=False,
            bottom=False,
            width=1.5,
            labelsize=20,
            labelrotation=0,
        )

        # Define the parameters related to the label of tickmarks and their relative
        # positioning, color of the tickmarks, and where they appear on the colorbar
        cbar.ax.tick_params(
            axis="x",
            direction="in",
            labeltop=True,
            labelbottom=False,
            color="b",
            top=True,
            bottom=False,
        )

        cbar.ax.xaxis.set_label_position("top")
        cbar.set_label("N", fontsize=20)

        if save_fig:
            if fig_name is None:
                fig_name = "figures/joint_pdf.png"
                # If the directory does not exist, create it
            Path("figures").mkdir(parents=True, exist_ok=True)
            plt.savefig(
                fig_name, bbox_inches="tight", pad_inches=0.05, format="png", dpi=300
            )
        return hst, x_s, y_s

    def kde_plots(
        self,
        x_data: np.array = None,
        y_data: np.array = None,
        x_label: str = None,
        y_label: str = None,
        save_fig: bool = False,
        fig_name: str = None,
        sea_kwargs=None,
    ):
        """
        The code to plot the kernel density estimate plot for any kind of data. The scale of both x-
        and y-axes is "linear", this can be changed in the line which 65 or so where "bins" is
        defined and setting both scales of x- and y-axes to log instead of linear.

        Parameters
        ----------
        x_data : np.array
            The x data for the kde plot
        y_data : np.array
            The y data for the kde plot
        x_label : str
            The label for the x-axis
        y_label : str
            The label for the y-axis
        save_fig : bool
            Whether to save the figure or not
        sea_kwargs : dict
            Additional arguments to be passed to the seaborn jointplot function. These keyword
            arguments are passed to the sns.jointplot function in the seaborn library

        Returns
        -------
        sns.axisgrid.JointGrid
            The seaborn jointplot object

        Examples
        --------
        >>> import numpy as np
        >>> from arcanum.histogram_plots import hist_plots
        >>> x = np.random.lognormal(mean=0, sigma=2, size=10000)
        >>> x = np.clip(x, 1e-3, 1e2)
        >>> y = np.random.lognormal(mean=0, sigma=2, size=10000)
        >>> y = np.clip(y, 1e-1, 1e1)
        >>> hist_plots().kde_plots(x_data=x, y_data=y, save_fig=True, sea_kwargs={ "kind": "kde", "cbar": True, "thresh": 0.05, "fill": True, "levels": 10, "log_scale": True, "hue_norm": "log", "cmap": "Blues", "height": 6, "ratio": 8, "space": 0.01, "xlim": (1e-3, 1e2), "ylim": (1e-3, 1e2), },
            )
        """

        # Check if Seaborn is installed, if not then raise an error and return
        try:
            import seaborn as sns
        except ImportError:
            raise ImportError(
                "Seaborn is not installed, please install it using pip install seaborn"
            )
            return

        labelsize = 28
        ticklabelsize = 20
        clabelsize = 15
        ticklength = 10

        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        axs1 = sns.jointplot(
            x=x_data,
            y=y_data,
            **(sea_kwargs if sea_kwargs else {}),
        )

        x0, x1 = axs1.ax_joint.get_xlim()
        y0, y1 = axs1.ax_joint.get_ylim()
        lims = [max(x0, y0), min(x1, y1)]
        axs1.ax_joint.plot(lims, lims, "--r", lw=2)

        pos_joint_ax = axs1.ax_joint.get_position()
        pos_marg_x_ax = axs1.ax_marg_x.get_position()
        axs1.ax_joint.set_position(
            [pos_joint_ax.x0, pos_joint_ax.y0, pos_marg_x_ax.width, pos_joint_ax.height]
        )
        axs1.figure.axes[-1].set_position(
            [1, pos_joint_ax.y0, 0.07, pos_joint_ax.height]
        )

        # get the current colorbar ticks
        cbar_ticks = axs1.figure.axes[-1].get_yticks()
        # get the maximum value of the colorbar
        _, cbar_max = axs1.figure.axes[-1].get_ylim()
        # change the labels (not the ticks themselves) to a percentage
        axs1.figure.axes[-1].set_yticklabels(
            [f"{t / cbar_max * 1:.3f}" for t in cbar_ticks], size=clabelsize
        )

        # Set the x-label at the center of the colorbar
        axs1.figure.axes[-1].text(
            0.5,
            0.5,
            "Density [%]",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=clabelsize,
            transform=axs1.figure.axes[-1].transAxes,
            color="w",
            rotation=270,
        )

        axs1.figure.axes[0].tick_params(
            axis="both",
            which="major",
            direction="in",
            labelbottom=True,
            bottom=True,
            labeltop=False,
            top=True,
            labelleft=True,
            left=True,
            labelright=False,
            right=True,
            width=1.5,
            length=ticklength,
            labelsize=ticklabelsize,
            labelrotation=0,
        )

        axs1.figure.axes[0].tick_params(
            axis="both",
            which="minor",
            direction="in",
            labelbottom=False,
            bottom=False,
            left=False,
            width=1.5,
            length=ticklength,
            labelsize=ticklabelsize,
            labelrotation=0,
        )

        axs1.figure.axes[1].tick_params(
            axis="both",
            which="both",
            direction="in",
            labelbottom=False,
            bottom=False,
            labelleft=False,
            left=False,
            width=1.5,
            length=ticklength,
            labelsize=ticklabelsize,
            labelrotation=0,
        )

        axs1.figure.axes[2].tick_params(
            axis="both",
            which="both",
            direction="in",
            labelbottom=False,
            bottom=False,
            labelleft=False,
            left=False,
            width=1.5,
            length=ticklength,
            labelsize=ticklabelsize,
            labelrotation=0,
        )

        try:
            axs1.figure.axes[3].tick_params(
                axis="y",
                which="major",
                direction="in",
                labelbottom=False,
                bottom=False,
                labelleft=False,
                left=False,
                labelright=True,
                right=True,
                width=1.5,
                length=ticklength,
                labelsize=clabelsize,
                labelrotation=0,
            )
        except IndexError:
            pass

        axs1.set_axis_labels("x", "y", fontsize=labelsize)
        if x_label is not None:
            axs1.ax_joint.set_xlabel(x_label, fontsize=labelsize)
        if y_label is not None:
            axs1.ax_joint.set_ylabel(y_label, fontsize=labelsize)

        if save_fig:
            if fig_name is None:
                fig_name = "figures/kdeplot.pdf"
            else:
                fig_name = f"figures/{fig_name}"
            # If the directory does not exist, create it
            Path("figures").mkdir(parents=True, exist_ok=True)
            axs1.savefig(fig_name, format="pdf", dpi=400)
        plt.close("all")
        return axs1
