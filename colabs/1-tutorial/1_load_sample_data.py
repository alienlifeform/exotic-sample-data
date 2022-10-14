#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8><b>Load telescope images</b></font>

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

from IPython.display import display, HTML, Javascript
display(HTML('<p class="bookend">START: Importing necessary software libraries</p>'))
display(HTML('<p class="hidden">Loading styles, please wait...</p>'))

# Install EXOTIC Colab interface code
!pip install git+https://github.com/alienlifeform/exotic-colab.git --upgrade

from exoticcolab.display import setupDisplay, testImplementation, displayStep, makeContainer, downloadButton, appendToContainer, appendStepToContainer, expandableSection, hideWarning, showProgress, resize_colab_cell

# Set up custom Colab styles and interactions
setupDisplay()
# Improve how colab handles long code output fields
get_ipython().events.register('pre_run_cell', resize_colab_cell)


display(HTML('<ul class="step_container_1a"></ul>'))
appendStepToContainer('.step_container_1a','Styles loaded, importing libraries...')
showProgress(1) # make it feel real

appendStepToContainer('.step_container_1a','(1/5) Bokeh.io')
import bokeh.io
from bokeh.io import output_notebook
showProgress(1) # make it feel real

appendStepToContainer('.step_container_1a','(2/5) EXOTIC <span class="comment">(This will take up to a minute, please wait...)</span>')
### We need only a subset of methods for the tutorial:
from astropy.io import fits
from bokeh.plotting import figure, output_file, show
from bokeh.models import BoxZoomTool,WheelZoomTool,ResetTool,HoverTool,PanTool,FreehandDrawTool
from bokeh.models import ColorBar, LinearColorMapper, LogColorMapper, LogTicker
import numpy as np
showProgress(5) # make it feel real

## rzellem version
#!pip install exotic --upgrade

## alienlifeform version
#!pip install git+https://github.com/alienlifeform/exotic-prototype.git --upgrade
#from exotic.api.colab import *

## plot_image not needed for the simulation
# from exotic.api.plotting import plot_image 

# This suppresses the "RESTART RUNTIME" button
hideWarning()
#display(HTML('<br /><p>If there is a "RESTART RUNTIME" warning button above, you can ignore it (or click it and then re-run this step).</p>'))

appendStepToContainer('.step_container_1a','(3/5) NASAExoplanetArchive, Astropy, Utils')
## Not needed for tutorial:
#from exotic.exotic import NASAExoplanetArchive, get_wcs, find_target

from IPython.display import Image
from ipywidgets import widgets, HBox
import os
import re
import json
showProgress(1) # make it feel real

appendStepToContainer('.step_container_1a','(4/5) Matlab, SciPy')
showProgress(2) # make it feel real

appendStepToContainer('.step_container_1a','(5/5) Google Utils')
from google.colab import files
showProgress(1) # make it feel real

#expandableSection('<p>This is some expandable stuff</p>')
display(HTML('<p class="bookend">DONE: Importing necessary software libraries</p>'))


#########################################################

display(HTML('<p class="bookend">START: Loading telescope images</p>'))
display(HTML('<ul class="step_container_1b"></ul>'))

appendStepToContainer('.step_container_1b','Ensuring sample images are loaded...')

#
# Delete existing sample data by changing to `rebuild = "true"`
#
rebuild = "false"  
if rebuild == "true":
  if os.path.isdir("/content/EXOTIC/tutorial"):
    %rm -rf /content/EXOTIC/tutorial
    display(HTML('<p class="step">"Rebuild" flag is "true"... Removing old images at /content/EXOTIC/tutorial</p>'))

#
# Download sample files if necessary
#
#sample_data_source = "https://github.com/rzellem/EXOTIC_sampledata.git" # goes into sample_data_target_folder
sample_data_source = "https://github.com/alienlifeform/exotic-sample-data.git" # goes into sample_data_target_parent
sample_data_target_parent = "/content/EXOTIC/tutorial"
sample_data_target_folder = "/content/EXOTIC/tutorial/sample-data"
sample_data_target_child = "/content/EXOTIC/tutorial/sample-data/HatP32Dec202017"
sample_data_target_outputs = "/content/EXOTIC/tutorial/sample-data/HatP32Dec202017_output"
if os.path.isdir(sample_data_target_child):
  appendStepToContainer('.step_container_1b','Skipping... Sample images already loaded')

else:
  appendStepToContainer('.step_container_1b','Downloading images from ' + sample_data_source)
  #git_rv = !git clone {sample_data_source} {sample_data_target_folder}
  git_rv = !git clone {sample_data_source} {sample_data_target_parent}
  git_co_rv = !cd {sample_data_target_parent} && !git checkout beta1
  appendStepToContainer('.step_container_1b','Telescope images successfully loaded for HAT-P-32 b')

#
# Show files found
#
#!du -hd0 --exclude ".*" /content/EXOTIC/tutorial/sample-data/HatP32Dec202017
numfiles_fits = !ls {sample_data_target_child} | grep -ci FITS
numfiles_json = !ls {sample_data_target_child} | grep -ci json

display(HTML('<p class="step">You have ' + str(numfiles_fits[0]) + ' telescope image (.FITS) files.</p>'))
#display(HTML('<p class="step">You have ' + str(numfiles_json[0]) + ' inits (.json) files</p>'))

display(HTML('<p class="bookend">DONE: Loading telescope images. <b>You may move on to the next step.</b></p>'))