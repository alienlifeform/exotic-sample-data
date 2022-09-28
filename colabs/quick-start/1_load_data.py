#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8>Load telescope images</font>

##############################################################
%%capture step_capture --no-display

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
showProgress(.3) 

appendStepToContainer('.step_container_1a','(1/5) Bokeh.io')
import bokeh.io
from bokeh.io import output_notebook
showProgress(.3) 

appendStepToContainer('.step_container_1a','(2/5) EXOTIC <span class="comment">(This will take up to a minute, please wait...)</span>')
#!pip install exotic --upgrade
## !pip install git+https://github.com/alienlifeform/exotic-prototype.git --upgrade
# This suppresses the "RESTART RUNTIME" button
## hideWarning()
## from exotic.api.colab import *
## from exotic.api.plotting import plot_image


appendStepToContainer('.step_container_1a','(3/5) NASAExoplanetArchive, Astropy, Utils')
## from exotic.exotic import NASAExoplanetArchive, get_wcs, find_target
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

appendStepToContainer('.step_container_1a','(4/5) Matlab, SciPy')
#import matplotlib.pyplot as plt
#from scipy.stats import gaussian_kde
showProgress(.3) 

appendStepToContainer('.step_container_1a','(5/5) Google Utils')
from google.colab import drive, files
showProgress(.3) 

#expandableSection('<p>This is some expandable stuff</p>')
display(HTML('<p class="bookend">DONE: Importing necessary software libraries</p>'))


#########################################################

display(HTML('<p class="bookend">START: Loading telescope images</p>'))
display(HTML('<ul class="step_container_1b"></ul>'))
appendStepToContainer('.step_container_1b','Ensuring images are loaded...</li>')
appendStepToContainer('.step_container_1b','<div class="attention"><b>Attention:</b> Be sure to "Permit this notebook to access your Google Drive files" if prompted.</div>')
showProgress(1) 

# Mount the user's drive so we can access images
drive.mount('/content/drive', force_remount=True)

bokeh.io.output_notebook()
sample_data = False

#appendStepToContainer('.step_container_1b','Note: You can navigate your uploaded files by clicking the folder icon along the left nav.')

################# TEMPORARY #############################

def check_dir(p):
  p = p.replace("\\", "/")

  if not(os.path.isdir(p)):
    print(HTML(f'<p class="error">Problem: the directory {p} doesn\'t seem to exist on your Gdrive filesystem.</p>'))
    return("")
  return(p)

def clean_input_filepath(p):
  #display(HTML(f'<p class="output">cif.p1={p}'))
  #p = re.sub('^/drive', '', p)
  #p = re.sub('^/MyDrive', '', p)
  p = re.sub('^/', '', p)
  #display(HTML(f'<p class="output">cif.p4={p}</p>'))
  return(p)

######################################################


# Ask for inputs until we find .fits files
fits_files_found = False
while not fits_files_found:
  # Ask for inputs until we find ANY files
  any_files_found = False
  while not any_files_found:
    input_filepath = input("Enter a path to your files starting after /drive/MyDrive/ (i.e. 'EXOTIC/YourObservationFolder'). ")
    display(HTML(f'<p class="output">input_filepath={input_filepath}</p>'))
    cleaned_filepath = clean_input_filepath(input_filepath)
    display(HTML(f'<p class="output">cleaned_filepath={cleaned_filepath}</p>'))
    if cleaned_filepath:
      verified_filepath = check_dir(os.path.join("/content/drive/My Drive/", cleaned_filepath))
      display(HTML(f'<p class="output">verified_filepath={verified_filepath}</p>'))
      
      if verified_filepath:
        output_dir = os.path.join(verified_filepath, "EXOTIC_output/")      
        display(HTML(f'<p class="output">output_dir={output_dir}</p>'))

        sorted_files = sorted(os.listdir(verified_filepath)); 
        display(HTML(f'<p class="output">sortedFiles={sorted_files}</p>'))

        if sorted_files:
          any_files_found = True # exit inner loop and continue
        else:
          display(HTML(f'<p class="error">Failed to find files at {verified_filepath}</p>'))
      else:
        display(HTML(f'<p class="error">Failed to find a folder at /content/drive/My Drive/{cleaned_filepath}</p>'))
    else:
      display(HTML(f'<p class="error">Filepath doesn\'t seem right: /content/drive/My Drive/{input_filepath}</p>'))


  # Directory full of files found, look for .fits and inits.json
  files = [f for f in sorted_files if os.path.isfile(os.path.join(verified_filepath, f))]
  fits_count, first_image = 0, ""

  inits = []    # array of paths to any inits files found in the directory
  # Identify files in user-submitted folder
  for f in files:
    # Look for .fits images and keep count
    if re.search(r"\.f[itz]+s?\.?g?z?$", f, re.IGNORECASE):
      # Determine the first image
      if first_image == "":
        first_image = os.path.join(verified_filepath, f)
      fits_count += 1
    # Look for inits.json file(s)
    if re.search(r"\.json$", f, re.IGNORECASE):
      inits.append(os.path.join(verified_filepath, f))

  display(HTML(f'<p class="output">Found {fits_count} image files and {len(inits)} initialization files in the directory.</p>'))

  if fits_count >= 19:
    fits_files_found = True # exit outer loop and continue
  else: 
    display(HTML(f'<p class="error">Failed to find .FITS files at {input_filepath} {verified_filepath}</p>'))

display(HTML(f'<p class="output">Looking for inits.json file'))
if len(inits) == 1:                 # one inits file exists
  # Deal with inits.json file
  inits_path = os.path.join(verified_filepath, inits[0])
  display(HTML(f'<p class="output">Got an inits.json file here: {inits_path}</p>'))
  with open(inits_path) as i_file:
    display(HTML(f'<p class="output">Loading coordinates and input/output directories from inits file</p>'))
    inits_data = i_file.read()
    d = json.loads(inits_data)
    targ_coords = d["user_info"]["Target Star X & Y Pixel"]
    comp_coords = d["user_info"]["Comparison Star(s) X & Y Pixel"]
    input_dir = d["user_info"]["Directory with FITS files"]
    if input_dir != verified_filepath:
      display(HTML(f'<p class="output">The directory with fits files should be {verified_filepath} but your inits file says {input_dir}.</p>'))
      display(HTML('<p class="output">This may or may not cause problems.  Just letting you know.<p>'))
    display(HTML(f'<p class="output">Coordinates from your inits file:\ntarget: {targ_coords}\ncomps: {comp_coords}<p>'))
    output_dir = d["user_info"]["Directory to Save Plots"]
   
  # Prompt for AAVSO code
  aavso_obs_code = ""
  if not sample_data:
    aavso_obs_code = input("Enter your AAVSO Observer code or press enter to skip.")

  # Create output_dir
  if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

  # Make an inits file with the planetary params(?)
  #inits = [make_inits_file(planetary_params, p, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]
else:
  display(HTML(f'<p class="output">No inits.json file found, we\'ll create it<p>'))

# Make the output directory if it does not exist already.
if not os.path.isdir(output_dir):    
  os.mkdir(output_dir)
  display(HTML(f'Creating output_dir at {output_dir}'))
output_dir_for_shell = output_dir.replace(" ", "\ ")


#
# Show files found
#
#!du -hd0 --exclude ".*" /content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017
numfiles_fits = !ls {sample_data_target_child} | grep -ci FITS
numfiles_json = !ls {sample_data_target_child} | grep -ci json

display(HTML('<ul class="step_container_1c"></ul>'))

appendStepToContainer('.step_container_1b','<p class="step">You have ' + str(numfiles_fits[0]) + ' telescope image (.FITS) files</p>')
appendStepToContainer('.step_container_1b','<p class="step">You have ' + str(numfiles_json[0]) + ' inits (.json) files</p>')

display(HTML('<p class="bookend">DONE: Loading telescope images. <b>You may move on to the next step.</b></p>'))
