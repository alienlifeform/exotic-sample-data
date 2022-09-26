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
#importCustomStyles()
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

display(HTML('''
<p class="bookend">START: Loading telescope images</p>
<li class="step">Ensuring images are loaded...</li>
<li class="step">Be sure to "Permit this notebook to access your Google Drive files" when prompted</li>
'''))

drive.mount('/content/drive', force_remount=True)


bokeh.io.output_notebook()
sample_data = False

p = input("Enter a path to your files as described above. (Likely 'EXOTIC/[your observation folder]') ")

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

display(HTML(f"Found {fits_count} image files and {len(inits)} initialization files in the directory."))

if fits_count >= 19:                  # more than 20 images in the folder --> run EXOTIC on these images
  if len(inits) == 1:                 # one inits file exists
    inits_path = os.path.join(p, inits[0])
    display(HTML(f"Got an inits.json file here: {inits_path}"))
    with open(inits_path) as i_file:
      inits_data = i_file.read()
      d = json.loads(inits_data)
      targ_coords = d["user_info"]["Target Star X & Y Pixel"]
      comp_coords = d["user_info"]["Comparison Star(s) X & Y Pixel"]
      input_dir = d["user_info"]["Directory with FITS files"]
      if input_dir != p:
        display(HTML(f"The directory with fits files should be {p} but your inits file says {input_dir}."))
        display(HTML("This may or may not cause problems.  Just letting you know."))
      display(HTML(f"Coordinates from your inits file:\ntarget: {targ_coords}\ncomps: {comp_coords}"))
      output_dir = d["user_info"]["Directory to Save Plots"]
     
    aavso_obs_code = ""
    if not sample_data:
      #display("If you have an AAVSO Observer code, enter it here.")
      #display("If not (or if you are not sure), just press enter.")
      aavso_obs_code = input("Enter your AAVSO Observer code or press enter to skip.")
#    display("If you want an alternate output directory, type it here.")
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
