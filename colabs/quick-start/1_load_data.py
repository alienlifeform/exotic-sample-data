#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8><b>Load telescope images</b></font>

##############################################################
%%capture step_capture --no-display
# Comment the above statement out to see debugging information

# Import display libraries to allow html, css, and javascript for styling and interaction
from IPython.display import display, HTML, Javascript
display(HTML('<p class="bookend">START: Importing necessary software libraries</p>'))
display(HTML('<p class="hidden">Loading styles, please wait...</p>'))

# Install EXOTIC Colab interface code to provide styling and interaction features
!pip install git+https://github.com/alienlifeform/exotic-colab.git --upgrade
from exoticcolab.display import setupDisplay, testImplementation, displayStep, makeContainer, downloadButton, appendToContainer, appendStepToContainer, expandableSection, hideWarning, showProgress, resize_colab_cell

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
#!pip install exotic --upgrade
!pip install git+https://github.com/alienlifeform/exotic-prototype.git --upgrade
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

# Import matlab/stats (perhaps not necessary anymore)
appendStepToContainer('.step_container_1a','(4/5) Matlab, SciPy')
#import matplotlib.pyplot as plt
#from scipy.stats import gaussian_kde
showProgress(.3) 

# Import Google Utils
appendStepToContainer('.step_container_1a','(5/5) Google Utils')
from google.colab import drive, files
showProgress(.3) 

#expandableSection('<p>This is some expandable stuff</p>')
display(HTML('<p class="bookend">DONE: Importing necessary software libraries</p>'))


#########################################################

# Prepare user for loading of images
display(HTML('<p class="bookend">START: Loading telescope images</p>'))
display(HTML('<ul class="step_container_1b"></ul>'))
appendStepToContainer('.step_container_1b','Ensuring images are loaded...</li>')
appendStepToContainer('.step_container_1b','<div class="attention"><b>Attention:</b> Be sure to "Permit this notebook to access your Google Drive files" if prompted.</div>')
showProgress(1) 

# Mount the user's drive so we can access images
drive.mount('/content/drive', force_remount=True)

# TODO Do we need this? Verify in Beta2
bokeh.io.output_notebook()
#appendStepToContainer('.step_container_1b','Note: You can navigate your uploaded files by clicking the folder icon along the left nav.')

################# TEMPORARY #############################

# use this if you disable exotic for rapid development
# def check_dir(p):
#   p = p.replace("\\", "/")

#   if not(os.path.isdir(p)):
#     print(HTML(f'<p class="error">Problem: the directory {p} doesn\'t seem to exist on your Gdrive filesystem.</p>'))
#     return("")
#   return(p)

def clean_input_filepath(p):
  p = re.sub('^/', '', p)
  return(p)

######################################################


# Ask for inputs until we find .fits files
fits_files_found = False
while not fits_files_found:
  # Ask for inputs until we find ANY files
  any_files_found = False
  while not any_files_found:
    input_filepath = input("Enter a path to your files starting after /drive/MyDrive/ (i.e. 'EXOTIC/YourObservationFolder'). ")
    #display(HTML(f'<p class="output">input_filepath={input_filepath}</p>'))
    cleaned_filepath = clean_input_filepath(input_filepath)
    #display(HTML(f'<p class="output">cleaned_filepath={cleaned_filepath}</p>'))
    if cleaned_filepath:
      verified_filepath = check_dir(os.path.join("/content/drive/My Drive/", cleaned_filepath))
      #display(HTML(f'<p class="output">verified_filepath={verified_filepath}</p>'))
      
      if verified_filepath:
        output_dir = os.path.join(verified_filepath, "EXOTIC_output/")      
        #display(HTML(f'<p class="output">output_dir={output_dir}</p>'))

        sorted_files = sorted(os.listdir(verified_filepath)); 
        #display(HTML(f'<p class="output">sortedFiles={sorted_files}</p>'))

        if sorted_files:
          any_files_found = True # exit inner loop and continue
        else:
          display(HTML(f'<p class="error">Failed to find files at {verified_filepath}. You can click the folder icon in the left nav to browse your Google Drive directories.</p>'))
      else:
        display(HTML(f'<p class="error">Failed to find a folder at /content/drive/My Drive/{cleaned_filepath}. You can click the folder icon in the left nav to browse your Google Drive directories.</p>'))
    else:
      display(HTML(f'<p class="error">Filepath doesn\'t seem right: /content/drive/My Drive/{input_filepath}. You can click the folder icon in the left nav to browse your Google Drive directories.</p>'))


  # Directory full of files found, look for .fits and inits.json
  files = [f for f in sorted_files if os.path.isfile(os.path.join(verified_filepath, f))]
  fits_count, inits_count, first_image = 0, 0, ""


  # Identify .FITS and inits.json files in user-submitted folder
  inits = []    # array of paths to any inits files found in the directory
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
  
  inits_count = len(inits)
  display(HTML(f'<p class="output">Found {fits_count} image files and {inits_count} initialization files in the directory.</p>'))

  appendStepToContainer('.step_container_1c','<p class="step">Found ' + str(fits_count) + ' telescope image (.FITS) files</p>')
  appendStepToContainer('.step_container_1c','<p class="step">Found ' + str(inits_count) + ' inits (.json) files</p>')

  # Determine if folder has enough .FITS folders to move forward
  # TODO: Is 19 an important number?
  if fits_count >= 19:
    fits_files_found = True # exit outer loop and continue

    # Make the output directory if it does not exist already.
    if not os.path.isdir(output_dir):    
      os.mkdir(output_dir)
      display(HTML(f'Creating output_dir at {output_dir}'))
    output_dir_for_shell = output_dir.replace(" ", "\ ")
  else: 
    display(HTML(f'<p class="error">Failed to find a significant number of .FITS files at {verified_filepath}</p>'))

# Read configuration from inits.json, if available
if inits_count == 1:                 # one inits file exists
  # Deal with inits.json file
  inits_path = os.path.join(verified_filepath, inits[0])
  inits_file_exists = True
  #display(HTML(f'<p class="output">Got an inits.json file here: {inits_path}</p>'))
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
  aavso_obs_code = input("Enter your AAVSO Observer code or press enter to skip.")
else:
  display(HTML(f'<p class="output">No valid inits.json file was found, we\'ll create it in the next step.<p>'))
  # TODO something here? - bergen
  inits_file_exists = False
  #inits = [make_inits_file(planetary_params, verified_filepath, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]

#
# Show files found
#
#!du -hd0 --exclude ".*" /content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017
#numfiles_fits = !ls {sample_data_target_child} | grep -ci FITS
#numfiles_json = !ls {sample_data_target_child} | grep -ci json

display(HTML('<ul class="step_container_1c"></ul>'))

#appendStepToContainer('.step_container_1c','<p class="step">You have ' + str(fits_count) + ' telescope image (.FITS) files</p>')
#appendStepToContainer('.step_container_1c','<p class="step">You have ' + str(inits_count) + ' inits (.json) files</p>')

display(HTML('<p class="bookend">DONE: Loading telescope images.</p>'))


######################################################

# Load planetary params if inits.json file does not yet exist
if not inits_file_exists:

  display(HTML('<p class="bookend">START: Download planetary parameters</p>'))

  planetary_params = ""
  while not planetary_params:
    target=input("Please enter the name of your exoplanet target (i.e. HAT-P-32 b): ")
    #target="HAT-P-32 b"
    display(HTML('<ul class="step_container_2"></ul>'))
    appendStepToContainer('.step_container_2','Searching NASA Exoplanet Archive')
    targ = NASAExoplanetArchive(planet=target)
    #appendStepToContainer('.step_container_2','Loading planet info')
    target = targ.planet_info()[0]
    
    if not targ.resolve_name():
      appendStepToContainer('.step_container_2','''
      Sorry, we can\'t find your target in the Exoplanet Archive.  Unfortunately, this
      isn't going to work until we can find it. Please try
      different formats for your target name, until the target is located.
      Looking it up in the NASA Exoplanet Archive at https://exoplanetarchive.ipac.caltech.edu/
      might help you know where to put the spaces and hyphens and such.
      ''')
      appendStepToContainer('.step_container_2','''
      If your target is a candidate, you may need to create your own inits.json file in the
      <a href="https://exoplanets-5.client.mooreboeck.com/exoplanet-watch/exotic/advanced-guide/">advanced EXOTIC edition</a>
      ''')
    else:
      appendStepToContainer('.step_container_2','Found target "' + target + '" in the NASA Exoplanet Archive')
      p_param_string = targ.planet_info(fancy=True)
      planetary_params = '"planetary_parameters": ' + p_param_string
      p_param_dict = json.loads(p_param_string)
      planetary_params = fix_planetary_params(p_param_dict)
      appendStepToContainer('.step_container_2','Loading NASA Exoplanet Archive planetary parameters for ' + target)
      display(HTML(f'<pre class="output">{planetary_params}</pre>'))

      # appendStepToContainer('.step_container_2','Planetary parameters generated, creating inits.json file')      
      # # Make the inits file
      # inits = [make_inits_file(planetary_params, verified_filepath, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]
      # appendStepToContainer('.step_container_2','inits.json created')



  display(HTML('<p class="bookend">DONE: Download planetary parameters. <b>You may move on to the next step.</b></p>'))



display(HTML('<p class="bookend">START: Find AAVSO StarChart</p>'))

display(HTML('<ul class="step_container_3"></ul>'))
appendStepToContainer('.step_container_3','Finding StarChart: Visit <a href="https://app.aavso.org/vsp/?star=Enter%20Your%20Star%20Here&scale=E&orientation=reversed&type=chart&fov=30.0&maglimit=16.5&resolution=150&north=up&east=right">search for your star</a>, enter in the star name, and hit \"plot chart\". Click the image on the resulting page, and copy the URL from your browser to put in below.')
aavso_starchart_url = input("Enter the URL of the AAVSO starchart for your star (i.e. 'https://app.aavso.org/vsp/chart/X28218AP.png'). ")

display(HTML('<p class="bookend">DONE: Find AAVSO StarChart. <b>You may move on to the next step.</b></p>'))

