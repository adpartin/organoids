#!/bin/bash

# Create env by running the line below, and then run this script.
# conda create -n pdx_lamina python=3.7 pip --yes

conda install -c bioconda salmon=v1.5.2
conda install -c conda-forge ipython=7.26.0
conda install -c conda-forge ipdb=0.11.0
conda install -c anaconda psutil=5.8.0
