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

setupDisplay()

# Prepare user for loading of images
display(HTML('<p class="bookend">START: Loading telescope images</p>'))
display(HTML('<ul class="step_container_2a"></ul>'))
appendStepToContainer('.step_container_2a','Ensuring images are loaded...</li>')
appendStepToContainer('.step_container_2a','<div class="attention"><b>Attention:</b> Be sure to "Permit this notebook to access your Google Drive files" if prompted.</div>')
showProgress(1) 

# TODO Do we need this? Verify in Beta2
bokeh.io.output_notebook()
#appendStepToContainer('.step_container_2a','Note: You can navigate your uploaded files by clicking the folder icon along the left nav.')

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
  #appendStepToContainer('.step_container_2a','A valid Google Drive filepath should not include /drive/MyDrive/')
  while not any_files_found:
    input_filepath = input('Enter path to .FITS images in Google Drive (i.e. "EXOTIC/MyOwnImages")')
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


  #appendStepToContainer('.step_container_2a','<p class="output">Found ' + str(fits_count) + ' telescope image (.FITS) files</p>')
  #appendStepToContainer('.step_container_2a','<p class="output">Found ' + str(inits_count) + ' inits (.json) files</p>')

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

#display(HTML('<ul class="step_container_2b"></ul>'))

#appendStepToContainer('.step_container_2b','<p class="output">You have ' + str(fits_count) + ' telescope image (.FITS) files</p>')
#appendStepToContainer('.step_container_2b','<p class="output">You have ' + str(inits_count) + ' inits (.json) files</p>')

display(HTML('<p class="bookend">DONE: Loading telescope images.</p>'))


######################################################

# Load planetary params if inits.json file does not yet exist
if not inits_file_exists:

  display(HTML('<p class="bookend">START: Download planetary parameters</p>'))

  planetary_params = ""
  while not planetary_params:
    target=input('Please enter the name of your exoplanet target (i.e. "HAT-P-32 b"): ')
    #target="HAT-P-32 b"
    display(HTML('<ul class="step_container_2b"></ul>'))
    appendStepToContainer('.step_container_2b','Searching NASA Exoplanet Archive for "' + target + '"')
    targ = NASAExoplanetArchive(planet=target)
    #appendStepToContainer('.step_container_2','Loading planet info')
    target = targ.planet_info()[0]
    
    if not targ.resolve_name():
      appendStepToContainer('.step_container_2b','''
      Sorry, we can\'t find your target in the Exoplanet Archive.  Unfortunately, this
      isn't going to work until we can find it. Please try
      different formats for your target name, until the target is located.
      Looking it up in the NASA Exoplanet Archive at https://exoplanetarchive.ipac.caltech.edu/
      might help you know where to put the spaces and hyphens and such.
      ''')
      appendStepToContainer('.step_container_2b','''
      If your target is a candidate, you may need to create your own inits.json file in the
      <a href="https://exoplanets-5.client.mooreboeck.com/exoplanet-watch/exotic/advanced-guide/">advanced EXOTIC edition</a>
      ''')
    else:
      appendStepToContainer('.step_container_2b','Found target "' + target + '" in the NASA Exoplanet Archive')
      p_param_string = targ.planet_info(fancy=True)
      planetary_params = '"planetary_parameters": ' + p_param_string
      p_param_dict = json.loads(p_param_string)
      planetary_params = fix_planetary_params(p_param_dict)
      appendStepToContainer('.step_container_2b','Loading NASA Exoplanet Archive planetary parameters for ' + target)
      display(HTML(f'<pre class="output">{planetary_params}</pre>'))

      # appendStepToContainer('.step_container_2b','Planetary parameters generated, creating inits.json file')      
      # # Make the inits file
      # inits = [make_inits_file(planetary_params, verified_filepath, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]
      # appendStepToContainer('.step_container_2b','inits.json created')

  # Prompt for AAVSO code
  aavso_obs_code = input("Enter your AAVSO Observer code or press enter to skip: ")

  display(HTML('<p class="bookend">DONE: Download planetary parameters.</p>'))


  ######################################################


  display(HTML('<p class="bookend">START: Load starchart</p>'))

  display(HTML('<ul class="step_container_2c"></ul>'))
  appendStepToContainer('.step_container_2c','Finding StarChart: Visit <a href="https://app.aavso.org/vsp/?star=Enter%20Your%20Star%20Here&scale=E&orientation=reversed&type=chart&fov=30.0&maglimit=16.5&resolution=150&north=up&east=right">search for your star</a>, enter in the star name, and hit "plot chart". Click the image on the resulting page, and copy the URL from your browser to put in below.')
  
  appendStepToContainer('.step_container_2c','Please enter a valid AAVSO starchart image URL for your star (i.e. "https://app.aavso.org/vsp/chart/X28218AP.png") <span class="comment has_tooltip">(?)</span>')
  appendToContainer('.comment','<div class="tooltip" style="display: none">TEST</div>')

  starchart_url_is_legit = False
  while not starchart_url_is_legit:
    aavso_starchart_url = input("Enter starchart image URL: ")
    if aavso_starchart_url.startswith('https://') and aavso_starchart_url.endswith('png'):
      starchart_url_is_legit = True
      display(HTML(f'<p class="output">Starchart URL is valid.</p>'))
    else:
      display(HTML(f'<p class="error">Starchart URL must begin with https:// and end with .png</p>'))


  display(HTML('<p class="bookend">DONE: Find AAVSO StarChart. <b>You may move on to the next step.</b></p>'))


  ######################################################

else: 

  display(HTML('<p class="bookend">DONE: Inits.json file exists <b>You may move on to the next step.</b></p>'))
