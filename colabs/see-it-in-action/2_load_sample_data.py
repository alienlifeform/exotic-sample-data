#@title <font face="Helvetica" class="button" color='#702020'><b>&lt;- Click to load telescope images</b></font>
#%%capture step_capture --no-display

##############################################################
%%capture step_capture --no-display

from IPython.display import display, HTML, Javascript
import random

# Grabs a stylesheet, call this before any html output in cell
def importCustomStyles():
  custom_stylesheet_url = 'https://exoplanets.nasa.gov/system/exotic/colab.css?i=' + str(random.random())
  display(HTML('<link rel="stylesheet" href="' + custom_stylesheet_url + '">'))
  #display(HTML('Getting stylesheet from ' + custom_stylesheet_url))

importCustomStyles()

display(HTML('''
<p class="bookend">START: Importing necessary software libraries</p>
<li class="step">(1/10) Time, ProgressBar</li>
'''))

import time
import progressbar

# Creates a progress bar that just runs for `seconds` number of seconds
def showProgress(seconds):
  with progressbar.ProgressBar(max_value=100) as bar:
    for idx, val in enumerate(range(100)):
      time.sleep(seconds/100)
      bar.update(idx)

# Avoids scroll-in-the-scroll in the entire Notebook
def resize_colab_cell():
  display(Javascript('google.colab.output.setIframeHeight(0, true, {maxHeight: 5000})'))
get_ipython().events.register('pre_run_cell', resize_colab_cell)


display(HTML('<li class="step">(2/10) IPython.display</li>'))

display(HTML('<li class="step">(3/10) Bokeh.io</li>'))
import bokeh.io

display(HTML('<li class="step">(4/10) EXOTIC <span class="comment">(This will take up to a minute, please wait... and ignore any warning that may ask you to "RESTART RUNTIME")</span></li>'))
!pip install exotic --upgrade
display(HTML('<br /><br /><p class="step"><span class="comment">Reminder, if there is a "RESTART RUNTIME" warning button above, ignore it (or you\'ll have to re-run this step)!</span></p>'))

# from exotic.api.plotting import plot_image
display(HTML('<li class="step">(5/10) NASAExoplanetArchive</li>'))
from exotic.exotic import NASAExoplanetArchive, get_wcs, find_target

display(HTML('<li class="step">(6/10) Astropy</li>'))
from astropy.time import Time

display(HTML('<li class="step">(7/10) Utils</li>'))
from barycorrpy import utc_tdb
import numpy as np
from io import BytesIO
from astropy.io import fits
from scipy.ndimage import label
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Viridis256
from bokeh.models import ColorBar, LinearColorMapper, LogColorMapper, LogTicker
from bokeh.models import BoxZoomTool,WheelZoomTool,ResetTool,HoverTool,PanTool,FreehandDrawTool
from bokeh.io import output_notebook
from pprint import pprint
from IPython.display import Image
from ipywidgets import widgets, HBox
from skimage.transform import rescale, resize, downscale_local_mean
import copy

display(HTML('<li class="step">(8/10) Matlab</li>'))
import matplotlib.pyplot as plt

display(HTML('<li class="step">(9/10) Scipy</li>'))
from scipy.stats import gaussian_kde

import os
import re
import json
import subprocess

display(HTML('<li class="step">(10/10) Google Utils</li>'))
from google.colab import drive, files

display(HTML('<p class="bookend">DONE: Importing necessary software libraries</p>'))

##############################################################

display(HTML('''
<p class="bookend">START: Loading telescope images</p>
<li class="step">Ensuring sample images are loaded...</li>
'''))

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

display(HTML('<p class="step">You have ' + str(numfiles_fits[0]) + ' telescope image (.FITS) files</p>'))
display(HTML('<p class="step">You have ' + str(numfiles_json[0]) + ' inits (.json) files</p>'))

display(HTML('<p class="bookend">DONE: Loading telescope images. <b>You may move on to the next step.</b></p>'))

# to mount the user's Google Drive... the original way
#drive.mount('/content/drive', force_remount=True)
