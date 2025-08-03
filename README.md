<div align="center">
    <img src="https://raw.githubusercontent.com/qudsiramiz/arcanumpy/refs/heads/main/src/_static/arcanumpy_logo.png" alt="ArcanumPy Logo" width="200" height="131">
</div>

arcanumpy bundles utility functions for plotting (e.g., `histogram_plots`, `seaborn_plots`), file handling (`get_files_from_web`), and text styling (`text_color_fnc`).

## Features

- **Plotting**: `histogram_plots` produces quick histogram and density visualizations, while `seaborn_plots` offers convenient helpers for Seaborn charts.
- **File handling**: `get_files_from_web` downloads data sets and other resources with a single call.
- **Text styling**: `text_color_fnc` adds color to terminal output for clearer command-line interaction.
- **Media conversion**: `img_to_mp4` turns image sequences into MP4 videos.

# Installation

To install the package, run the following command:

```bash
pip install arcanumpy
```

## Example

```python
import numpy as np
from arcanumpy.histogram_plots import hist_plots

data = np.random.randn(1000)
bins, pdf = hist_plots().calc_pdf(input_array=data, plot_pdf=True)
```

Visit the [documentation](https://qudsiramiz.space/arcanumpy/) for more information on how to use the package.
