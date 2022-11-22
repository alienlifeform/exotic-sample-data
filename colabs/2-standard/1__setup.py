#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8><b>Load EXOTIC libraries and mount Google Drive</b></font>

##############################################################
%%capture step_capture --no-display
# Comment the above statement out to see debugging information
##############################################################

##############################################################
#
# NOTE TO EXOTIC USER:
#
#   • To hide this code, double-click the title above ("Load telescope images"),
#     or click the arrow to the left of the title.
#
#   • Editing this code will only affect your local instance. 
#     Reload to revert your changes.
#
##############################################################

# Import display libraries to allow html, css, and javascript for styling and interaction
from IPython.display import display, HTML, Javascript
display(HTML('<p class="bookend">START: Importing necessary software libraries</p>'))
display(HTML('<p class="hidden">Loading styles, please wait...</p>'))

# Install EXOTIC Colab interface code to provide styling and interaction features
!pip install git+https://github.com/alienlifeform/exotic-colab.git --upgrade
from exoticcolab.display import setupDisplay, testImplementation, displayStep, makeContainer, downloadButton, appendToContainer, appendStepToContainer, expandableSection, expandableSectionCustom, hideWarning, showProgress, resize_colab_cell

# Set up custom Colab styles and interactions
setupDisplay()
# Improve how colab handles long code output fields
get_ipython().events.register('pre_run_cell', resize_colab_cell)

# Show progress
display(HTML('<ul class="step_container_1a"></ul>'))
appendStepToContainer('.step_container_1a','Styles loaded, importing libraries...')
showProgress(.3) 

# Import graphing libraries
appendStepToContainer('.step_container_1a','(1/5) Bokeh.io')
import bokeh.io
from bokeh.io import output_notebook
showProgress(.3) 

# Import EXOTIC
appendStepToContainer('.step_container_1a','(2/5) EXOTIC <span class="comment">(This will take up to a minute, please wait...)</span>')

!pip install exotic --upgrade
#!pip install git+https://github.com/alienlifeform/exotic-prototype.git --upgrade
# This suppresses the "RESTART RUNTIME" button
hideWarning()
from exotic.api.colab import *
from exotic.api.plotting import plot_image

# Import other utilities
appendStepToContainer('.step_container_1a','(3/5) NASAExoplanetArchive, Astropy, Utils')
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
import glob

# Import matlab/stats (perhaps not necessary anymore)
appendStepToContainer('.step_container_1a','(4/5) Matlab, SciPy')
#import matplotlib.pyplot as plt
#from scipy.stats import gaussian_kde
showProgress(.3) 

# Import Google Utils
appendStepToContainer('.step_container_1a','(5/5) Google Utils')
from google.colab import drive, files
showProgress(.3) 

display(HTML('<p class="bookend">DONE: Importing necessary software libraries</p>'))

# Prepare user for loading of images
display(HTML('<p class="bookend">START: Mounting Google Drive</p>'))
display(HTML('<ul class="step_container_1b"></ul>'))
appendStepToContainer('.step_container_1b','<div class="attention"><b>Attention:</b> Be sure to "Permit this notebook to access your Google Drive files" if prompted.</div>')
showProgress(1) 

# Mount the user's drive so we can access images
drive.mount('/content/drive', force_remount=True)

appendStepToContainer('.step_container_1b','Drive successfully mounted')

display(HTML('<p class="bookend">DONE: Mounting Google Drive.  <b>You may move on to the next step.</b></p>'))