# DarkLim

[![Build and upload to PyPI](https://github.com/spice-herald/DarkLim/actions/workflows/github-deploy.yml/badge.svg)](https://github.com/spice-herald/DarkLim/actions/workflows/github-deploy.yml) [![PyPI](https://img.shields.io/pypi/v/darklim)](https://pypi.org/project/darklim/) [![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

DarkLim provides statistical tools for calculating dark matter exclusion limits and sensitivity estimates.

To install the most recent release of DarkLim, type the following line into your command line

`pip install darklim --upgrade`

To install the most recent development version of DarkLim from source, clone this repo, then from the top-level directory of the repo, type the following line into your command line

`pip install .`

If using a shared Python installation, you may want to add the `--user` flag to the above line(s).

**NOTE:** This package also requires a Fortran compiler if installing from source (or a wheel is not available for your setup). We recommend installing `gfortran`, which can be done via `sudo apt-get install gfortran` on Linux or `brew install gcc` on macOS.
