#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8>Load telescope images</font>

##############################################################
%%capture step_capture --no-display

from IPython.display import display, HTML, Javascript
display(HTML('<p class="bookend">START: Importing necessary software libraries</p>'))
display(HTML('<p class="hidden">Loading styles, please wait...</p>'))

# Install EXOTIC Colab interface code
!pip install git+https://github.com/alienlifeform/exotic-colab.git --upgrade

from exoticcolab.display import testImplementation, importCustomStyles, setupDisplay, displayStep, makeContainer, appendToContainer, expandableSection, showProgress,resize_colab_cell
#testImplementation()

# Set up custom Colab styles and interactions
importCustomStyles()
setupDisplay()
get_ipython().events.register('pre_run_cell', resize_colab_cell)

display(HTML('<ul class="step_container"></ul>'))
displayStep('Styles loaded, importing libraries...')

displayStep('(1/5) Bokeh.io')
import bokeh.io
from bokeh.io import output_notebook

displayStep('(2/5) EXOTIC <span class="comment">(This will take up to a minute, please wait...)</span>')

#!pip install exotic --upgrade
!pip install git+https://github.com/alienlifeform/exotic-prototype.git --upgrade
display(HTML('<br /><p>If there is a "RESTART RUNTIME" warning button above, you can ignore it (or you\'ll have to re-run this step).</p>'))
from exotic.api.colab import *
#from exotic.api.plotting import plot_image

displayStep('(3/5) NASAExoplanetArchive, Astropy, Utils')
from exotic.exotic import NASAExoplanetArchive, get_wcs, find_target
#from astropy.time import Time
#from barycorrpy import utc_tdb
#import numpy as np
#from io import BytesIO
#from astropy.io import fits
#from scipy.ndimage import label
#from bokeh.plotting import figure, output_file, show
#from bokeh.palettes import Viridis256
#from bokeh.models import ColorBar, LinearColorMapper, LogColorMapper, LogTicker
#from bokeh.models import BoxZoomTool,WheelZoomTool,ResetTool,HoverTool,PanTool,FreehandDrawTool
#from pprint import pprint
from IPython.display import Image
from ipywidgets import widgets, HBox
#from skimage.transform import rescale, resize, downscale_local_mean
#import copy
import os
import re
import json
#import subprocess

displayStep('(4/5) Matlab, SciPy')
#import matplotlib.pyplot as plt
#from scipy.stats import gaussian_kde

displayStep('(5/5) Google Utils')
from google.colab import drive, files

#expandableSection('<p>This is some expandable stuff</p>')
display(HTML('<p class="bookend">DONE: Importing necessary software libraries</p>'))


#########################################################

display(HTML('<p class="bookend">START: Loading telescope images</p>'))
display(HTML('<ul class="step_container"></ul>'))

display(HTML('<li class="step">Ensuring sample images are loaded...</li>'))

#
# Delete existing sample data by changing to `rebuild = "true"`
#
rebuild = "true"  
if rebuild == "true":
  if os.path.isdir("/content/EXOTIC/exotic-in-action"):
    %rm -rf /content/EXOTIC/exotic-in-action
    display(HTML('<p class="step">"Rebuild" flag is "true"... Removing old images at /content/EXOTIC/exotic-in-action</p>'))

#
# Download sample files if necessary
#
#sample_data_source = "https://github.com/rzellem/EXOTIC_sampledata.git" # goes into sample_data_target_folder
sample_data_source = "https://github.com/alienlifeform/exotic-sample-data.git" # goes into sample_data_target_parent
sample_data_target_parent = "/content/EXOTIC/exotic-in-action"
sample_data_target_folder = "/content/EXOTIC/exotic-in-action/sample-data"
sample_data_target_child = "/content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017"
sample_data_target_outputs = "/content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017/EXOTIC_output"
if os.path.isdir(sample_data_target_child):
  display(HTML('<li class="step">Skipping... Sample images already loaded</li>'))

else:
  display(HTML('<li class="step">Downloading images from ' + sample_data_source + '</li>'))
  #git_rv = !git clone {sample_data_source} {sample_data_target_folder}
  git_rv = !git clone {sample_data_source} {sample_data_target_parent}
  git_co_rv = !cd {sample_data_target_parent} && !git checkout beta1
  display(HTML('<li class="step">Telescope images successfully loaded for HAT-P-32 b</li>'))

#
# Show files found
#
#!du -hd0 --exclude ".*" /content/EXOTIC/exotic-in-action/sample-data/HatP32Dec202017
numfiles_fits = !ls {sample_data_target_child} | grep -ci FITS
numfiles_json = !ls {sample_data_target_child} | grep -ci json

display(HTML('<p class="step">You have ' + str(numfiles_fits[0]) + ' telescope image (.FITS) files.</p>'))
#display(HTML('<p class="step">You have ' + str(numfiles_json[0]) + ' inits (.json) files</p>'))

display(HTML('<p class="bookend">DONE: Loading telescope images. <b>You may move on to the next step.</b></p>'))