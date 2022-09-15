#@title <font face="Helvetica" color='#702020'>&lt;- Click to import required Python libraries</font> { vertical-output: true }

##############################################################
%%capture step_capture --no-display
import random
from IPython.display import display, HTML
def importCustomStyles():
  custom_stylesheet_url = 'https://exoplanets.nasa.gov/system/exotic/colab.css?i=' + str(random.random())
  display(HTML('<link rel="stylesheet" href="' + custom_stylesheet_url + '">'))
  #display(HTML('Getting stylesheet from ' + custom_stylesheet_url))

importCustomStyles()

display(HTML('<p class="bookend">START: Importing libraries</p>'))
display(HTML('<ul class="step1">'))

display(HTML('<li class="step1">IPython.display</li>'))

display(HTML('<li class="step1">Bokeh.io</li>'))
import bokeh.io

display(HTML('<li class="step1">EXOTIC <span class="comment">(This is large, please wait... and ignore any warning that may ask you to "RESTART RUNTIME")</span></li>'))
!pip install exotic --upgrade

# from exotic.api.plotting import plot_image
display(HTML('<li class="step1">NASAExoplanetArchive</li>'))
from exotic.exotic import NASAExoplanetArchive, get_wcs, find_target

display(HTML('<li class="step1">Astropy</li>'))
from astropy.time import Time

display(HTML('<li class="step1">Utils</li>'))
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

display(HTML('<li class="step1">Matlab</li>'))
import matplotlib.pyplot as plt

display(HTML('<li class="step1">Scipy</li>'))
from scipy.stats import gaussian_kde

display(HTML('<li class="step1">OS/RE/JSON</li>'))
import os
import re
import json
import subprocess

display(HTML('<li class="step1">GoogleDrive</li>'))
from google.colab import drive

display(HTML('</ul>'))

display(HTML('<p class="bookend">DONE: Importing libraries. <b>You may move on to the next step.</b></p>'))