#@title <font face="Helvetica" class="button" color='#702020'><b>&lt;- Click to load telescope images</b></font>
#%%capture step_capture --no-display

##############################################################
%%capture step_capture --no-display
print("Starting application...")

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
<li class="step">(1/4) Time, ProgressBar, Bokeh.io</li>
'''))

import time
import progressbar
import bokeh.io

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

display(HTML('<li class="step">(2/4) EXOTIC <span class="comment">(This will take up to a minute, please wait... and ignore any warning that may ask you to "RESTART RUNTIME")</span></li>'))
!pip install exotic --upgrade
display(HTML('<br /><br /><p class="step"><span class="comment">Reminder, if there is a "RESTART RUNTIME" warning button above, ignore it (or you\'ll have to re-run this step)!</span></p>'))

# from exotic.api.plotting import plot_image
display(HTML('<li class="step">(3/4) NASAExoplanetArchive, Astropy, Utils</li>'))
from exotic.exotic import NASAExoplanetArchive, get_wcs, find_target
from astropy.time import Time
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

display(HTML('<li class="step">(4/4) Matlab, Scipy, Google Utils</li>'))
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os
import re
import json
import subprocess
from google.colab import drive, files

display(HTML('<p class="bookend">DONE: Importing necessary software libraries</p>'))

##############################################################

# Find a field in the image fits header or prompt the user to enter the corresponding
# value.

def check_dir(p):
  p = p.replace("\\", "/")

  if not(os.path.isdir(p)):
    print(f"Problem: the directory {p} doesn't seem to exist")
    print("on your Gdrive filesystem.")
    return("")
  return(p)

#########################################################


display(HTML('''
<p class="bookend">START: Loading telescope images</p>
<li class="step">Ensuring images are loaded...</li>
<li class="step">Be sure to "Permit this notebook to access your Google Drive files" when prompted</li>
'''))

drive.mount('/content/drive', force_remount=True)


bokeh.io.output_notebook()
sample_data = False

p = input("Enter a path to your files as described above. (Likely 'EXOTIC/[your observation folder]')")

p = check_dir(os.path.join("/content/drive/My Drive/", p))
output_dir = os.path.join(p, "EXOTIC_output/")      
   
inits = []    # array of paths to any inits files found in the directory
files = [f for f in sorted(os.listdir(p)) if os.path.isfile(os.path.join(p, f))]
fits_count, first_image = 0, ""
for f in files:
  if re.search(r"\.f[itz]+s?\.?g?z?$", f, re.IGNORECASE):
    if first_image == "":
      first_image = os.path.join(p, f)
    fits_count += 1
  if re.search(r"\.json$", f, re.IGNORECASE):
    inits.append(os.path.join(p, f))

print(f"Found {fits_count} image files and {len(inits)} initialization files in the directory.")

if fits_count >= 19:                  # more than 20 images in the folder --> run EXOTIC on these images
  if len(inits) == 1:                 # one inits file exists
    inits_path = os.path.join(p, inits[0])
    with open(inits_path) as i_file:
      inits_data = i_file.read()
      d = json.loads(inits_data)
      targ_coords = d["user_info"]["Target Star X & Y Pixel"]
      comp_coords = d["user_info"]["Comparison Star(s) X & Y Pixel"]
      input_dir = d["user_info"]["Directory with FITS files"]
      if input_dir != p:
        print(f"The directory with fits files should be {p} but your inits file says {input_dir}.")
        print("This may or may not cause problems.  Just letting you know.")
      print(f"Coordinates from your inits file:\ntarget: {targ_coords}\ncomps: {comp_coords}")
      output_dir = d["user_info"]["Directory to Save Plots"]
     
    aavso_obs_code = ""
    if not sample_data:
      print("If you have an AAVSO Observer code, enter it here.")
      print("If not (or if you are not sure), just press enter.")
      aavso_obs_code = input()
#    print("If you want an alternate output directory, type it here.")
#    alt_out = input()
#    if (re.search(r"\w", alt_out)):
#      output_dir = alt_out
    if not os.path.isdir(output_dir):
      os.mkdir(output_dir)

    #inits = [make_inits_file(planetary_params, p, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]

  if not os.path.isdir(output_dir):    # Make the output directory if it does not exist already.
    os.mkdir(output_dir)
  output_dir_for_shell = output_dir.replace(" ", "\ ")


#
# Show files found
#
#!du -hd0 --exclude ".*" /content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017
numfiles_fits = !ls {sample_data_target_child} | grep -ci FITS
numfiles_json = !ls {sample_data_target_child} | grep -ci json

display(HTML('<p class="step">You have ' + str(numfiles_fits[0]) + ' telescope image (.FITS) files</p>'))
display(HTML('<p class="step">You have ' + str(numfiles_json[0]) + ' inits (.json) files</p>'))

display(HTML('<p class="bookend">DONE: Loading telescope images. <b>You may move on to the next step.</b></p>'))

# to mount the user's Google Drive... the original way
#drive.mount('/content/drive', force_remount=True)
